"""Reusable ENTSO-E request execution and parsing core."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import time

import requests

from src.parser import parse_entsoe_xml, parse_and_merge_xml_folder, parsed_to_csv

BASE_URL = "https://web-api.tp.entsoe.eu/api"
DEFAULT_REQUEST_TIMEOUT = 60
DEFAULT_REQUEST_DELAY = 0.5


@dataclass(frozen=True)
class EntsoeConfig:
    """Configuration for ENTSO-E requests."""

    api_key: str
    base_url: str
    project_root: Path
    output_dir: Path
    xml_dir: Path
    json_dir: Path
    csv_dir: Path
    request_timeout: int
    request_delay: float


def build_config(
    api_key: str,
    project_root: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    base_url: str = BASE_URL,
    request_timeout: int = DEFAULT_REQUEST_TIMEOUT,
    request_delay: float = DEFAULT_REQUEST_DELAY,
) -> EntsoeConfig:
    """Build a configuration object for ENTSO-E requests."""
    root = project_root or Path(__file__).resolve().parents[2]
    resolved_output = output_dir or root / "results"
    xml_dir = resolved_output / "xml"
    json_dir = resolved_output / "json"
    csv_dir = resolved_output / "csv"
    return EntsoeConfig(
        api_key=api_key,
        base_url=base_url,
        project_root=root,
        output_dir=resolved_output,
        xml_dir=xml_dir,
        json_dir=json_dir,
        csv_dir=csv_dir,
        request_timeout=request_timeout,
        request_delay=request_delay,
    )


def setup_directories(config: EntsoeConfig) -> Dict[str, str]:
    """Create output directories if they don't exist."""
    config.xml_dir.mkdir(parents=True, exist_ok=True)
    config.json_dir.mkdir(parents=True, exist_ok=True)
    config.csv_dir.mkdir(parents=True, exist_ok=True)
    return {
        "xml": str(config.xml_dir),
        "json": str(config.json_dir),
        "csv": str(config.csv_dir),
    }


def format_datetime(dt: datetime) -> str:
    """Format datetime for ENTSO-E API (yyyyMMddHHmm)."""
    return dt.strftime("%Y%m%d%H%M")


def get_time_range(days_back: int = 1, end_date: Optional[datetime] = None) -> tuple[str, str]:
    """Get a time range for API requests."""
    if end_date is None:
        end_date = datetime.now(timezone.utc)

    start_date = end_date - timedelta(days=days_back)
    return format_datetime(start_date), format_datetime(end_date)


def parse_api_datetime(date_str: str) -> datetime:
    """Parse ENTSO-E API datetime format (yyyyMMddHHmm) to datetime object."""
    return datetime.strptime(date_str, "%Y%m%d%H%M").replace(tzinfo=timezone.utc)


def calculate_years_in_range(start_str: str, end_str: str) -> float:
    """Calculate the number of years between two API datetime strings."""
    start = parse_api_datetime(start_str)
    end = parse_api_datetime(end_str)
    delta = end - start
    return delta.days / 365.25


def split_into_yearly_chunks(start_str: str, end_str: str) -> List[tuple[str, str, str]]:
    """Split a time range into yearly chunks."""
    start = parse_api_datetime(start_str)
    end = parse_api_datetime(end_str)

    chunks = []
    current = start

    while current < end:
        year_end = datetime(current.year + 1, 1, 1, 0, 0, tzinfo=timezone.utc)
        chunk_end = min(year_end, end)
        chunk_start_str = format_datetime(current)
        chunk_end_str = format_datetime(chunk_end)
        year_label = str(current.year)
        chunks.append((chunk_start_str, chunk_end_str, year_label))
        current = year_end

    return chunks


def is_historical_request(params: Dict[str, str]) -> bool:
    """Check if a request spans more than 1 year (requires splitting)."""
    start = params.get("periodStart", "")
    end = params.get("periodEnd", "")

    if not start or not end:
        return False

    try:
        years = calculate_years_in_range(start, end)
    except (ValueError, TypeError):
        return False

    return years > 1.0


def make_request(params: Dict[str, str], config: EntsoeConfig) -> Dict[str, Any]:
    """Make a single API request."""
    full_params = {"securityToken": config.api_key, **params}
    try:
        response = requests.get(
            config.base_url, params=full_params, timeout=config.request_timeout
        )
        return {"status_code": response.status_code, "content": response.content}
    except requests.exceptions.Timeout:
        return {"status_code": None, "content": None, "error": "timeout"}
    except requests.exceptions.RequestException as exc:
        return {"status_code": None, "content": None, "error": str(exc)}


def _base_result(name: str, params: Dict[str, str]) -> Dict[str, Any]:
    return {
        "name": name,
        "params": params,
        "success": False,
        "files": [],
        "summary": {
            "timeseries_count": 0,
            "data_points": 0,
        },
        "error": None,
        "api_message": None,
        "status_code": None,
    }


def process_request(params: Dict[str, str], name: str, config: EntsoeConfig) -> Dict[str, Any]:
    """Process a single request: fetch XML, save it, parse to JSON and CSV."""
    result = _base_result(name, params)

    response_data = make_request(params, config)
    result["status_code"] = response_data.get("status_code")

    response_content = response_data.get("content")
    if response_content is None:
        result["error"] = response_data.get("error") or "request_failed"
        return result

    xml_filename = f"{name}.xml"
    xml_path = config.xml_dir / xml_filename

    with open(xml_path, "wb") as file_handle:
        file_handle.write(response_content)

    result["files"].append({"type": "xml", "path": str(xml_path)})

    try:
        json_filename = f"{name}.json"
        json_path = config.json_dir / json_filename
        parsed = parse_entsoe_xml(str(xml_path), str(json_path))

        result["files"].append({"type": "json", "path": str(json_path)})
        result["summary"]["timeseries_count"] = parsed.get("timeseriesCount", 0)
        result["summary"]["data_points"] = parsed.get("totalDataPoints", 0)
        result["success"] = True

        if parsed.get("error"):
            result["api_message"] = parsed.get("error", {}).get("text", "")

        csv_filename = f"{name}.csv"
        csv_path = config.csv_dir / csv_filename
        csv_info = parsed_to_csv(parsed, str(csv_path))
        result["files"].append({"type": "csv", "path": str(csv_path)})
        result["csv_info"] = csv_info
    except Exception as exc:  # pragma: no cover - bubbled to caller
        result["error"] = f"parse_error: {exc}"

    return result


def process_historical_request(
    params: Dict[str, str],
    name: str,
    config: EntsoeConfig,
) -> Dict[str, Any]:
    """Process a historical request (>1 year) by splitting into yearly chunks."""
    result = _base_result(name, params)
    result.update(
        {
            "is_historical": True,
            "chunks_total": 0,
            "chunks_success": 0,
            "chunks_with_data": 0,
        }
    )

    start_str = params.get("periodStart", "")
    end_str = params.get("periodEnd", "")
    chunks = split_into_yearly_chunks(start_str, end_str)
    result["chunks_total"] = len(chunks)

    xml_subfolder = config.xml_dir / name
    xml_subfolder.mkdir(parents=True, exist_ok=True)
    result["files"].append({"type": "xml_folder", "path": str(xml_subfolder)})

    for i, (chunk_start, chunk_end, year_label) in enumerate(chunks, 1):
        chunk_params = params.copy()
        chunk_params["periodStart"] = chunk_start
        chunk_params["periodEnd"] = chunk_end

        response_data = make_request(chunk_params, config)
        response_content = response_data.get("content")

        if response_content is None:
            continue

        xml_path = xml_subfolder / f"{year_label}.xml"
        with open(xml_path, "wb") as file_handle:
            file_handle.write(response_content)

        result["chunks_success"] += 1

        if i < len(chunks):
            time.sleep(config.request_delay)

    if result["chunks_success"] == 0:
        result["error"] = "all_chunks_failed"
        return result

    try:
        json_path = config.json_dir / f"{name}.json"
        csv_path = config.csv_dir / f"{name}.csv"

        parsed = parse_and_merge_xml_folder(
            str(xml_subfolder), str(json_path), str(csv_path)
        )

        result["files"].append({"type": "json", "path": str(json_path)})
        result["files"].append({"type": "csv", "path": str(csv_path)})
        result["summary"]["timeseries_count"] = parsed.get("timeseriesCount", 0)
        result["summary"]["data_points"] = parsed.get("totalDataPoints", 0)
        result["chunks_with_data"] = parsed.get("chunksWithData", 0)
        result["csv_info"] = parsed.get("csvInfo", {})
        result["success"] = True
    except Exception as exc:  # pragma: no cover - bubbled to caller
        result["error"] = f"merge_error: {exc}"

    return result


def run_request(
    params: Dict[str, str],
    name: Optional[str] = None,
    config: Optional[EntsoeConfig] = None,
) -> Dict[str, Any]:
    """Run a single request and return a structured result."""
    if config is None:
        raise ValueError("config is required for run_request")
    request_name = name or params.get("name", "request")
    if is_historical_request(params):
        return process_historical_request(params, request_name, config)
    return process_request(params, request_name, config)


def run_batch(
    requests_list: List[Dict[str, Any]],
    config: Optional[EntsoeConfig] = None,
) -> Dict[str, Any]:
    """Run all requests in the list and return structured results."""
    if config is None:
        raise ValueError("config is required for run_batch")

    results = []
    total = len(requests_list)

    for i, req in enumerate(requests_list, 1):
        result = run_request(req["params"], req.get("name"), config)
        results.append(result)

        if i < total:
            time.sleep(config.request_delay)

    summary_payload = parse_results(results)
    return {"results": results, **summary_payload}


def parse_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a summary and file list from request results."""
    successful = [r for r in results if r.get("success")]
    with_data = [r for r in successful if r.get("summary", {}).get("data_points", 0) > 0]
    no_data = [r for r in successful if r.get("summary", {}).get("data_points", 0) == 0]
    failed = [r for r in results if not r.get("success")]
    historical = [r for r in results if r.get("is_historical")]

    total_series = sum(r.get("summary", {}).get("timeseries_count", 0) for r in successful)
    total_points = sum(r.get("summary", {}).get("data_points", 0) for r in successful)
    total_chunks = sum(r.get("chunks_total", 0) for r in historical)

    summary = {
        "total_requests": len(results),
        "successful": len(successful),
        "with_data": len(with_data),
        "no_data": len(no_data),
        "failed": len(failed),
        "historical": len(historical),
        "total_timeseries": total_series,
        "total_data_points": total_points,
        "total_chunks": total_chunks,
    }

    files: List[Dict[str, str]] = []
    for result in results:
        files.extend(result.get("files", []))

    return {"summary": summary, "files": files}
