"""ENTSO-E request execution helpers for the backend."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

from entsoe_core import build_config, parse_results, run_request, setup_directories

from backend.app.storage import RESULTS_DIR, ensure_storage


class EntsoeError(RuntimeError):
    """Raised when ENTSO-E execution fails."""


def run_requests(requests_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    api_key = os.getenv("ENTSOE_API_KEY")
    if not api_key:
        raise EntsoeError("ENTSOE_API_KEY is not set.")

    ensure_storage()
    config = build_config(
        api_key,
        project_root=Path(__file__).resolve().parents[2],
        output_dir=RESULTS_DIR,
    )
    setup_directories(config)

    results = [run_request(req["params"], req.get("name"), config) for req in requests_list]
    
    # If there are multiple successful results, create a combined CSV/JSON
    from entsoe_core.parser import merge_parsed_results, parsed_to_csv, parse_entsoe_xml
    import json

    successful_results = [r for r in results if r.get("success")]
    if len(successful_results) > 1:
        try:
            # Parse all successful results to get their dict representations
            all_parsed = []
            for res in successful_results:
                # Find the XML file in the result
                xml_path = next((f["path"] for f in res["files"] if f["type"] == "xml"), None)
                if xml_path:
                    all_parsed.append(parse_entsoe_xml(xml_path))
            
            if all_parsed:
                merged = merge_parsed_results(all_parsed)
                
                # Save combined files with unique name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                combined_name = f"combined_{timestamp}"
                json_path = config.json_dir / f"{combined_name}.json"
                csv_path = config.csv_dir / f"{combined_name}.csv"
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(merged, f, indent=2, default=str)
                
                csv_info = parsed_to_csv(merged, str(csv_path))
                
                # Add combined files to the execution summary
                combined_result = {
                    "name": "Combined Results",
                    "success": True,
                    "files": [
                        {"type": "json", "path": str(json_path)},
                        {"type": "csv", "path": str(csv_path)}
                    ],
                    "summary": {
                        "timeseries_count": merged.get("timeseriesCount", 0),
                        "data_points": merged.get("totalDataPoints", 0),
                    },
                    "csv_info": csv_info,
                    "is_combined": True
                }
                # Prepend to results so they appear first
                results.insert(0, combined_result)
        except Exception as e:
            print(f"⚠️ Error creating combined results: {e}")

    summary_payload = parse_results(results)

    return {"results": results, **summary_payload}
