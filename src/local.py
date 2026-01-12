"""
ENTSO-E Data Fetcher and Parser - Local Runner

This script fetches data from the ENTSO-E Transparency Platform API,
saves XML responses, and converts them to JSON format.

Usage:
    python -m src.local

Structure:
    1. Configuration (API key, folders, base URL)
    2. Request definitions (loaded from my_requests.json)
    3. Execution engine (makes requests, saves XML, parses to JSON)
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

from entsoe_core import (
    build_config,
    run_request,
    parse_results,
    setup_directories,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

load_dotenv()

API_KEY = os.getenv("ENTSOE_API_KEY")
PROJECT_ROOT = Path(__file__).parent.parent
REQUESTS_FILE = PROJECT_ROOT / "my_requests.json"

# =============================================================================
# REQUEST LOADING
# =============================================================================


def load_requests() -> List[Dict[str, Any]]:
    """
    Load LOCAL requests from my_requests.json file.

    Filters for requests with 'run': 'local' or no 'run' field.
    Requests with 'run': 'modal' are skipped (handled by the Modal API service).

    Returns:
        List of request definitions with 'name' and 'params'
    """
    if not REQUESTS_FILE.exists():
        print(f"❌ Requests file not found: {REQUESTS_FILE}")
        return []

    try:
        with open(REQUESTS_FILE, "r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
    except json.JSONDecodeError as exc:
        print(f"❌ Invalid JSON in {REQUESTS_FILE}: {exc}")
        return []

    requests = data.get("requests", [])

    valid_requests = [
        req
        for req in requests
        if isinstance(req, dict)
        and "name" in req
        and "params" in req
        and req.get("run", "local") == "local"
    ]

    return valid_requests


# =============================================================================
# SUMMARY OUTPUT
# =============================================================================


def print_summary(results: List[Dict[str, Any]], output_dirs: Dict[str, str]):
    """Print a summary of all results."""
    summary_payload = parse_results(results)
    summary = summary_payload["summary"]

    successful = [r for r in results if r.get("success")]
    with_data = [
        r
        for r in successful
        if r.get("summary", {}).get("data_points", 0) > 0
    ]
    no_data = [
        r
        for r in successful
        if r.get("summary", {}).get("data_points", 0) == 0
    ]
    failed = [r for r in results if not r.get("success")]
    historical = [r for r in results if r.get("is_historical")]

    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}\n")

    print(f"✅ Successful: {summary['successful']}/{summary['total_requests']}")
    print(f"   📈 With data: {summary['with_data']}")
    print(f"   ⚠️  No data: {summary['no_data']}")
    if historical:
        print(
            f"   📅 Historical: {summary['historical']} ({summary['total_chunks']} chunks)"
        )
    if failed:
        print(f"❌ Failed: {summary['failed']}")

    print(f"\n📊 Total TimeSeries: {summary['total_timeseries']}")
    print(f"📊 Total Data Points: {summary['total_data_points']}")

    print(f"\n📁 XML files: {output_dirs['xml']}")
    print(f"📁 JSON files: {output_dirs['json']}")

    if with_data:
        print("\n📄 Files with data:")
        for result in with_data:
            name = result.get("name")
            timeseries = result.get("summary", {}).get("timeseries_count", 0)
            points = result.get("summary", {}).get("data_points", 0)
            if result.get("is_historical"):
                chunks_info = (
                    f" ({result.get('chunks_with_data', 0)}/{result.get('chunks_total', 0)} chunks)"
                )
                print(f"   📅 {name}: {timeseries} series, {points} points{chunks_info}")
            else:
                print(f"   ✅ {name}: {timeseries} series, {points} points")

    if no_data:
        print("\n⚠️  Files without data:")
        for result in no_data:
            msg = (result.get("api_message") or "")[:50]
            print(f"   - {result.get('name')}: {msg}...")


# =============================================================================
# MAIN EXECUTION
# =============================================================================


def main():
    """Main execution function."""
    print("\n" + "=" * 60)
    print("🔌 ENTSO-E Data Fetcher")
    print("=" * 60)

    if not API_KEY:
        print("\n❌ Error: ENTSOE_API_KEY not found in environment variables!")
        print("   Please set it in your .env file or environment.")
        return

    print(f"\n🔑 API Key: {API_KEY[:8]}...{API_KEY[-4:]}")

    config = build_config(API_KEY, project_root=PROJECT_ROOT)
    output_dirs = setup_directories(config)

    print(f"📁 XML output: {output_dirs['xml']}")
    print(f"📁 JSON output: {output_dirs['json']}")
    print(f"📁 CSV output: {output_dirs['csv']}")

    print(f"\n📄 Loading requests from: {REQUESTS_FILE.name}")
    requests_list = load_requests()

    if not requests_list:
        print("\n⚠️  No requests defined!")
        print(f"   Add request definitions to: {REQUESTS_FILE}")
        print("   See the '_instructions' section in the JSON file for help.")
        return

    print(f"   Found {len(requests_list)} request(s)")

    results = []
    total = len(requests_list)

    for i, req in enumerate(requests_list, 1):
        print(f"\n[{i}/{total}] {req['name']}")
        print("-" * 40)
        result = run_request(req["params"], req.get("name"), config)
        results.append(result)

        if i < total:
            time.sleep(config.request_delay)

    print_summary(results, output_dirs)

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
