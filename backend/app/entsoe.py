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
    summary_payload = parse_results(results)

    return {"results": results, **summary_payload}
