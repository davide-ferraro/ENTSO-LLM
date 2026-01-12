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

import os
import json
import time
import requests
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

from src.parser import parse_entsoe_xml, parse_and_merge_xml_folder, parsed_to_csv

# =============================================================================
# CONFIGURATION
# =============================================================================

# Load environment variables
load_dotenv()

# API Configuration
API_KEY = os.getenv('ENTSOE_API_KEY')
BASE_URL = "https://web-api.tp.entsoe.eu/api"

# Output folders (relative to project root)
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "results"
XML_DIR = OUTPUT_DIR / "xml"
JSON_DIR = OUTPUT_DIR / "json"
CSV_DIR = OUTPUT_DIR / "csv"

# Request settings
REQUEST_TIMEOUT = 60  # seconds
REQUEST_DELAY = 0.5   # delay between requests (be nice to the API)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def setup_directories():
    """Create output directories if they don't exist."""
    XML_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 XML output: {XML_DIR}")
    print(f"📁 JSON output: {JSON_DIR}")
    print(f"📁 CSV output: {CSV_DIR}")


def format_datetime(dt: datetime) -> str:
    """Format datetime for ENTSO-E API (yyyyMMddHHmm)."""
    return dt.strftime("%Y%m%d%H%M")


def get_time_range(days_back: int = 1, end_date: datetime = None) -> tuple:
    """
    Get a time range for API requests.
    
    Args:
        days_back: Number of days back from end_date
        end_date: End date (defaults to now)
        
    Returns:
        Tuple of (periodStart, periodEnd) formatted strings
    """
    if end_date is None:
        end_date = datetime.now(timezone.utc)
    
    start_date = end_date - timedelta(days=days_back)
    
    return format_datetime(start_date), format_datetime(end_date)


# =============================================================================
# HISTORICAL DATA HELPERS
# =============================================================================

def parse_api_datetime(date_str: str) -> datetime:
    """
    Parse ENTSO-E API datetime format (yyyyMMddHHmm) to datetime object.
    
    Args:
        date_str: Date string in format 'yyyyMMddHHmm'
        
    Returns:
        datetime object (UTC)
    """
    return datetime.strptime(date_str, "%Y%m%d%H%M").replace(tzinfo=timezone.utc)


def calculate_years_in_range(start_str: str, end_str: str) -> float:
    """
    Calculate the number of years between two API datetime strings.
    
    Args:
        start_str: Start date in 'yyyyMMddHHmm' format
        end_str: End date in 'yyyyMMddHHmm' format
        
    Returns:
        Number of years (float)
    """
    start = parse_api_datetime(start_str)
    end = parse_api_datetime(end_str)
    delta = end - start
    return delta.days / 365.25


def split_into_yearly_chunks(start_str: str, end_str: str) -> List[tuple]:
    """
    Split a time range into yearly chunks.
    
    Args:
        start_str: Start date in 'yyyyMMddHHmm' format
        end_str: End date in 'yyyyMMddHHmm' format
        
    Returns:
        List of (chunk_start, chunk_end, year_label) tuples
    """
    start = parse_api_datetime(start_str)
    end = parse_api_datetime(end_str)
    
    chunks = []
    current = start
    
    while current < end:
        # Calculate end of current year
        year_end = datetime(current.year + 1, 1, 1, 0, 0, tzinfo=timezone.utc)
        
        # Chunk ends at either year boundary or final end date
        chunk_end = min(year_end, end)
        
        # Create chunk
        chunk_start_str = format_datetime(current)
        chunk_end_str = format_datetime(chunk_end)
        year_label = str(current.year)
        
        chunks.append((chunk_start_str, chunk_end_str, year_label))
        
        # Move to next year
        current = year_end
    
    return chunks


def is_historical_request(params: Dict[str, str]) -> bool:
    """
    Check if a request spans more than 1 year (requires splitting).
    
    Args:
        params: Request parameters dict with 'periodStart' and 'periodEnd'
        
    Returns:
        True if request spans > 1 year
    """
    start = params.get('periodStart', '')
    end = params.get('periodEnd', '')
    
    if not start or not end:
        return False
    
    try:
        years = calculate_years_in_range(start, end)
        return years > 1.0
    except (ValueError, TypeError):
        return False


# =============================================================================
# REQUEST EXECUTION ENGINE
# =============================================================================

def make_request(params: Dict[str, str], name: str) -> Optional[bytes]:
    """
    Make a single API request.
    
    Args:
        params: Request parameters (excluding securityToken)
        name: Name for the request (used for logging and filenames)
        
    Returns:
        Response content as bytes (may be XML or ZIP) or None if failed
    """
    # Add security token
    full_params = {"securityToken": API_KEY, **params}
    
    try:
        print(f"  🌐 Requesting: {name}...")
        response = requests.get(BASE_URL, params=full_params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            print(f"  ✅ Success ({len(response.content)} bytes)")
            return response.content  # Return bytes, not text
        else:
            print(f"  ❌ HTTP {response.status_code}")
            return response.content  # Return anyway for error analysis
            
    except requests.exceptions.Timeout:
        print(f"  ⏱️ Timeout after {REQUEST_TIMEOUT}s")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request error: {e}")
        return None


def process_request(params: Dict[str, str], name: str) -> Dict[str, Any]:
    """
    Process a single request: fetch XML, save it, parse to JSON and CSV.
    
    Args:
        params: Request parameters
        name: Name for the request
        
    Returns:
        Result dictionary with status and paths
    """
    result = {
        "name": name,
        "params": params,
        "success": False,
        "xml_path": None,
        "json_path": None,
        "csv_path": None,
        "timeseries_count": 0,
        "data_points": 0,
        "error": None
    }
    
    # Make request
    response_content = make_request(params, name)
    
    if response_content is None:
        result["error"] = "Request failed"
        return result
    
    # Save response (could be XML or ZIP)
    # Use .xml extension regardless - parser handles both formats
    xml_filename = f"{name}.xml"
    xml_path = XML_DIR / xml_filename
    
    # Save as binary to preserve ZIP files correctly
    with open(xml_path, 'wb') as f:
        f.write(response_content)
    
    result["xml_path"] = str(xml_path)
    is_zip = response_content[:2] == b'PK'
    print(f"  💾 Saved {'ZIP' if is_zip else 'XML'}: {xml_filename}")
    
    # Parse to JSON
    try:
        json_filename = f"{name}.json"
        json_path = JSON_DIR / json_filename
        
        parsed = parse_entsoe_xml(str(xml_path), str(json_path))
        
        result["json_path"] = str(json_path)
        result["timeseries_count"] = parsed.get("timeseriesCount", 0)
        result["data_points"] = parsed.get("totalDataPoints", 0)
        result["success"] = True
        
        if parsed.get("error"):
            result["api_message"] = parsed["error"].get("text", "")
            print(f"  ⚠️ API: No data available")
        else:
            print(f"  📊 Parsed: {result['timeseries_count']} series, {result['data_points']} points")
        
        print(f"  💾 Saved JSON: {json_filename}")
        
        # Export to CSV
        csv_filename = f"{name}.csv"
        csv_path = CSV_DIR / csv_filename
        csv_info = parsed_to_csv(parsed, str(csv_path))
        result["csv_path"] = str(csv_path)
        print(f"  📄 Saved CSV: {csv_filename} ({csv_info['rows']} rows, {len(csv_info['columns'])} cols)")
        
    except Exception as e:
        result["error"] = f"Parse error: {e}"
        print(f"  ❌ Parse error: {e}")
    
    return result


def process_historical_request(params: Dict[str, str], name: str) -> Dict[str, Any]:
    """
    Process a historical request (>1 year) by splitting into yearly chunks.
    
    - Creates a subfolder for XMLs: results/xml/{name}/
    - Makes separate API calls for each year
    - Merges all results into a single JSON and CSV
    
    Args:
        params: Request parameters
        name: Name for the request
        
    Returns:
        Result dictionary with status and paths
    """
    result = {
        "name": name,
        "params": params,
        "success": False,
        "xml_folder": None,
        "json_path": None,
        "csv_path": None,
        "timeseries_count": 0,
        "data_points": 0,
        "chunks_total": 0,
        "chunks_success": 0,
        "chunks_with_data": 0,
        "error": None,
        "is_historical": True
    }
    
    # Get time range and split into chunks
    start_str = params.get('periodStart', '')
    end_str = params.get('periodEnd', '')
    chunks = split_into_yearly_chunks(start_str, end_str)
    result["chunks_total"] = len(chunks)
    
    years = calculate_years_in_range(start_str, end_str)
    print(f"  📅 Historical request: {years:.1f} years ({len(chunks)} chunks)")
    
    # Create subfolder for this request's XMLs
    xml_subfolder = XML_DIR / name
    xml_subfolder.mkdir(parents=True, exist_ok=True)
    result["xml_folder"] = str(xml_subfolder)
    print(f"  📁 XML subfolder: {xml_subfolder.name}/")
    
    # Process each chunk
    for i, (chunk_start, chunk_end, year_label) in enumerate(chunks, 1):
        print(f"\n  📆 Chunk {i}/{len(chunks)}: {year_label}")
        
        # Create chunk-specific params
        chunk_params = params.copy()
        chunk_params['periodStart'] = chunk_start
        chunk_params['periodEnd'] = chunk_end
        
        # Make request for this chunk
        chunk_name = f"{name}_{year_label}"
        response_content = make_request(chunk_params, chunk_name)
        
        if response_content is None:
            print(f"    ⚠️ Chunk {year_label} failed - skipping")
            continue
        
        # Save response in subfolder (binary to preserve ZIP)
        xml_path = xml_subfolder / f"{year_label}.xml"
        with open(xml_path, 'wb') as f:
            f.write(response_content)
        
        result["chunks_success"] += 1
        is_zip = response_content[:2] == b'PK'
        print(f"    💾 Saved: {year_label}.xml {'(ZIP)' if is_zip else ''}")
        
        # Delay between chunk requests
        if i < len(chunks):
            time.sleep(REQUEST_DELAY)
    
    # Check if we got any data
    if result["chunks_success"] == 0:
        result["error"] = "All chunks failed"
        print(f"\n  ❌ All {len(chunks)} chunks failed")
        return result
    
    print(f"\n  ✅ Retrieved {result['chunks_success']}/{len(chunks)} chunks")
    
    # Merge all XMLs into single JSON and CSV
    try:
        json_path = JSON_DIR / f"{name}.json"
        csv_path = CSV_DIR / f"{name}.csv"
        
        print(f"  🔄 Merging XMLs to JSON and CSV...")
        parsed = parse_and_merge_xml_folder(str(xml_subfolder), str(json_path), str(csv_path))
        
        result["json_path"] = str(json_path)
        result["csv_path"] = str(csv_path)
        result["timeseries_count"] = parsed.get("timeseriesCount", 0)
        result["data_points"] = parsed.get("totalDataPoints", 0)
        result["chunks_with_data"] = parsed.get("chunksWithData", 0)
        result["success"] = True
        
        csv_info = parsed.get("csvInfo", {})
        csv_rows = csv_info.get("rows", 0)
        csv_cols = len(csv_info.get("columns", []))
        
        print(f"  📊 Merged: {result['timeseries_count']} series, {result['data_points']} points")
        print(f"  💾 Saved JSON: {json_path.name}")
        print(f"  📄 Saved CSV: {csv_path.name} ({csv_rows} rows, {csv_cols} cols)")
        
    except Exception as e:
        result["error"] = f"Merge error: {e}"
        print(f"  ❌ Merge error: {e}")
    
    return result


def run_requests(requests_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Run all requests in the list.
    
    Args:
        requests_list: List of request definitions
        
    Returns:
        List of results
    """
    results = []
    total = len(requests_list)
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting {total} requests")
    print(f"{'='*60}\n")
    
    for i, req in enumerate(requests_list, 1):
        print(f"\n[{i}/{total}] {req['name']}")
        print("-" * 40)
        
        # Check if this is a historical request (>1 year)
        if is_historical_request(req["params"]):
            result = process_historical_request(req["params"], req["name"])
        else:
            result = process_request(req["params"], req["name"])
        
        results.append(result)
        
        # Delay between requests
        if i < total:
            time.sleep(REQUEST_DELAY)
    
    return results


def print_summary(results: List[Dict[str, Any]]):
    """Print a summary of all results."""
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}\n")
    
    successful = [r for r in results if r["success"]]
    with_data = [r for r in successful if r["data_points"] > 0]
    no_data = [r for r in successful if r["data_points"] == 0]
    failed = [r for r in results if not r["success"]]
    historical = [r for r in results if r.get("is_historical")]
    
    total_series = sum(r["timeseries_count"] for r in successful)
    total_points = sum(r["data_points"] for r in successful)
    total_chunks = sum(r.get("chunks_total", 0) for r in historical)
    
    print(f"✅ Successful: {len(successful)}/{len(results)}")
    print(f"   📈 With data: {len(with_data)}")
    print(f"   ⚠️  No data: {len(no_data)}")
    if historical:
        print(f"   📅 Historical: {len(historical)} ({total_chunks} chunks)")
    if failed:
        print(f"❌ Failed: {len(failed)}")
    
    print(f"\n📊 Total TimeSeries: {total_series}")
    print(f"📊 Total Data Points: {total_points}")
    
    print(f"\n📁 XML files: {XML_DIR}")
    print(f"📁 JSON files: {JSON_DIR}")
    
    # List files with data
    if with_data:
        print(f"\n📄 Files with data:")
        for r in with_data:
            if r.get("is_historical"):
                chunks_info = f" ({r.get('chunks_with_data', 0)}/{r.get('chunks_total', 0)} chunks)"
                print(f"   📅 {r['name']}: {r['timeseries_count']} series, {r['data_points']} points{chunks_info}")
            else:
                print(f"   ✅ {r['name']}: {r['timeseries_count']} series, {r['data_points']} points")
    
    # List files without data
    if no_data:
        print(f"\n⚠️  Files without data:")
        for r in no_data:
            msg = r.get("api_message", "")[:50]
            print(f"   - {r['name']}: {msg}...")


# =============================================================================
# REQUEST LOADING
# =============================================================================

REQUESTS_FILE = PROJECT_ROOT / "my_requests.json"


def load_requests() -> List[Dict[str, Any]]:
    """
    Load LOCAL requests from my_requests.json file.
    
    Filters for requests with 'run': 'local' or no 'run' field.
    Requests with 'run': 'modal' are skipped (handled by modal_runner.py).
    
    Returns:
        List of request definitions with 'name' and 'params'
    """
    if not REQUESTS_FILE.exists():
        print(f"❌ Requests file not found: {REQUESTS_FILE}")
        return []
    
    try:
        with open(REQUESTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {REQUESTS_FILE}: {e}")
        return []
    
    # Get requests array
    requests = data.get("requests", [])
    
    # Filter valid LOCAL requests only
    # Include if: has name + params AND (run is 'local' OR run is missing)
    valid_requests = [
        req for req in requests 
        if isinstance(req, dict) 
        and "name" in req 
        and "params" in req
        and req.get("run", "local") == "local"  # Default to local if not specified
    ]
    
    return valid_requests

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("🔌 ENTSO-E Data Fetcher")
    print("="*60)
    
    # Check API key
    if not API_KEY:
        print("\n❌ Error: ENTSOE_API_KEY not found in environment variables!")
        print("   Please set it in your .env file or environment.")
        return
    
    print(f"\n🔑 API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
    
    # Setup directories
    setup_directories()
    
    # Load requests from JSON file
    print(f"\n📄 Loading requests from: {REQUESTS_FILE.name}")
    requests_list = load_requests()
    
    # Check if there are requests to run
    if not requests_list:
        print("\n⚠️  No requests defined!")
        print(f"   Add request definitions to: {REQUESTS_FILE}")
        print("   See the '_instructions' section in the JSON file for help.")
        return
    
    print(f"   Found {len(requests_list)} request(s)")
    
    # Run requests
    results = run_requests(requests_list)
    
    # Print summary
    print_summary(results)
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()

