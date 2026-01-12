"""
ENTSO-E Data Fetcher - Modal Cron Job Version

This script runs scheduled data fetching on Modal with:
- Automatic historical data collection (20 years, one-time)
- Recurring operational data fetching (cron scheduled)
- JSON/CSV merging (append new data to historical files)
- Volume-based storage

Usage:
    modal deploy src/modal_runner.py     # Deploy cron jobs
    modal run src/modal_runner.py        # Run once manually

Prerequisites:
    1. Install Modal: pip install modal
    2. Authenticate: modal token new
    3. Set up secret: modal secret create ENTSOE_API_KEY ENTSOE_API_KEY=<your_key>
"""

import os
import json
import time
import io
import zipfile
import modal
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional

# =============================================================================
# MODAL APP CONFIGURATION
# =============================================================================

# Create Modal app
app = modal.App("entsoe-fetcher")

# Create persistent volume for data storage
volume = modal.Volume.from_name("entsoe-fetch", create_if_missing=True)

# Volume mount path inside container
VOLUME_PATH = Path("/data")

# Local path for reading requests (project root)
LOCAL_PATH = Path(__file__).parent.parent

# Define the image with required dependencies
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "requests",
    "python-dotenv"
)

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_URL = "https://web-api.tp.entsoe.eu/api"
REQUEST_TIMEOUT = 60
REQUEST_DELAY = 0.5
HISTORICAL_YEARS = 20
OPERATIONAL_OVERLAP_HOURS = 1

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_datetime(dt: datetime) -> str:
    """Format datetime for ENTSO-E API (yyyyMMddHHmm)."""
    return dt.strftime("%Y%m%d%H%M")


def parse_api_datetime(date_str: str) -> datetime:
    """Parse ENTSO-E API datetime format to datetime object."""
    return datetime.strptime(date_str, "%Y%m%d%H%M").replace(tzinfo=timezone.utc)


def get_historical_time_range() -> tuple:
    """Get 20-year historical time range ending now."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date.replace(year=end_date.year - HISTORICAL_YEARS)
    return format_datetime(start_date), format_datetime(end_date)


def get_operational_time_range(hours_back: int = 3) -> tuple:
    """Get operational time range with overlap for safety."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(hours=hours_back + OPERATIONAL_OVERLAP_HOURS)
    return format_datetime(start_date), format_datetime(end_date)


def split_into_yearly_chunks(start_str: str, end_str: str) -> List[tuple]:
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


def load_modal_requests_local() -> List[Dict[str, Any]]:
    """Load requests from local my_requests.json (for sync/local entrypoint)."""
    requests_file = LOCAL_PATH / "my_requests.json"
    
    if not requests_file.exists():
        print(f"❌ my_requests.json not found at {requests_file}")
        return []
    
    with open(requests_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    requests = data.get("requests", [])
    
    # Filter for Modal requests only
    modal_requests = [
        req for req in requests
        if req.get("run") == "modal" and "name" in req and "params" in req
    ]
    
    return modal_requests


def load_modal_requests_from_volume() -> List[Dict[str, Any]]:
    """Load requests from Modal volume (for scheduled runs)."""
    requests_file = VOLUME_PATH / "my_requests.json"
    
    if not requests_file.exists():
        print("❌ my_requests.json not found in volume")
        print("   Run 'modal run src/modal_runner.py::sync_requests' first to upload your requests")
        return []
    
    print(f"📄 Loading requests from volume: {requests_file}")
    
    with open(requests_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    requests = data.get("requests", [])
    
    # Filter for Modal requests only
    modal_requests = [
        req for req in requests
        if req.get("run") == "modal" and "name" in req and "params" in req
    ]
    
    return modal_requests


# =============================================================================
# XML PARSING (embedded for Modal - simplified version)
# =============================================================================

import xml.etree.ElementTree as ET


def is_zip_content(content: bytes) -> bool:
    """Check if content is a ZIP file (starts with PK magic bytes)."""
    return len(content) >= 2 and content[:2] == b'PK'


def extract_xml_from_zip(zip_content: bytes) -> str:
    """Extract XML content from a ZIP file."""
    with zipfile.ZipFile(io.BytesIO(zip_content)) as zf:
        xml_files = [f for f in zf.namelist() if f.endswith('.xml')]
        if not xml_files:
            raise ValueError("No XML file found in ZIP archive")
        with zf.open(xml_files[0]) as xml_file:
            return xml_file.read().decode('utf-8')


def get_xml_content(response_content: bytes) -> str:
    """Get XML content from response, handling both raw XML and ZIP."""
    if is_zip_content(response_content):
        return extract_xml_from_zip(response_content)
    return response_content.decode('utf-8')


def parse_xml_to_dict(xml_content: str) -> Dict[str, Any]:
    """Parse ENTSO-E XML response to dictionary."""
    root = ET.fromstring(xml_content)
    
    # Detect namespace
    ns = ''
    if '{' in root.tag:
        ns = root.tag.split('}')[0] + '}'
    
    def get_text(elem, path, default=''):
        child = elem.find(f'{ns}{path}')
        if child is None:
            child = elem.find(path)
        return child.text if child is not None and child.text else default
    
    def find_all(elem, path):
        result = elem.findall(f'{ns}{path}')
        if not result:
            result = elem.findall(path)
        return result
    
    # Check for no data response
    if 'Acknowledgement_MarketDocument' in root.tag:
        reason = root.find(f'{ns}Reason') or root.find('Reason')
        return {
            'documentInfo': {'documentType': 'Acknowledgement_MarketDocument'},
            'timeInterval': {'start': '', 'end': ''},
            'error': {
                'code': get_text(reason, 'code') if reason else '',
                'text': get_text(reason, 'text') if reason else ''
            },
            'timeseries': [],
            'timeseriesCount': 0,
            'totalDataPoints': 0
        }
    
    # Parse document info
    result = {
        'documentInfo': {
            'documentType': root.tag.split('}')[-1] if '}' in root.tag else root.tag,
            'mRID': get_text(root, 'mRID'),
            'type': get_text(root, 'type'),
            'processType': get_text(root, 'process.processType'),
            'createdDateTime': get_text(root, 'createdDateTime'),
        },
        'timeInterval': {'start': '', 'end': ''},
        'timeseries': [],
        'timeseriesCount': 0,
        'totalDataPoints': 0
    }
    
    # Parse time interval
    for path in ['time_Period.timeInterval', 'period.timeInterval']:
        interval = root.find(f'{ns}{path}') or root.find(path)
        if interval:
            result['timeInterval'] = {
                'start': get_text(interval, 'start'),
                'end': get_text(interval, 'end')
            }
            break
    
    # Resolution mapping
    resolution_map = {
        'PT1M': timedelta(minutes=1),
        'PT15M': timedelta(minutes=15),
        'PT30M': timedelta(minutes=30),
        'PT60M': timedelta(hours=1),
        'P1D': timedelta(days=1),
    }
    
    # Parse timeseries
    for ts in find_all(root, 'TimeSeries'):
        ts_data = {
            'mRID': get_text(ts, 'mRID'),
            'businessType': get_text(ts, 'businessType'),
            'unit': get_text(ts, 'quantity_Measure_Unit.name'),
            'periods': [],
            'totalPoints': 0
        }
        
        # PSR Type
        psr_type = ts.find(f'{ns}MktPSRType') or ts.find('MktPSRType')
        if psr_type is not None:
            ts_data['psrType'] = get_text(psr_type, 'psrType')
        
        # Domain info
        for field in ['outBiddingZone_Domain.mRID', 'inBiddingZone_Domain.mRID',
                      'in_Domain.mRID', 'out_Domain.mRID']:
            value = get_text(ts, field)
            if value:
                key = field.replace('.mRID', '').replace('_Domain', '')
                ts_data[key] = value
        
        # Parse periods
        for period in find_all(ts, 'Period'):
            interval = period.find(f'{ns}timeInterval') or period.find('timeInterval')
            resolution_str = get_text(period, 'resolution')
            resolution = resolution_map.get(resolution_str, timedelta(hours=1))
            
            period_start = get_text(interval, 'start') if interval else ''
            start_time = None
            if period_start:
                try:
                    start_time = datetime.fromisoformat(period_start.replace('Z', '+00:00'))
                except ValueError:
                    pass
            
            period_data = {
                'start': period_start,
                'end': get_text(interval, 'end') if interval else '',
                'resolution': resolution_str,
                'points': []
            }
            
            for point in find_all(period, 'Point'):
                position = int(get_text(point, 'position', '0'))
                point_data = {'position': position}
                
                if start_time:
                    timestamp = start_time + resolution * (position - 1)
                    point_data['timestamp'] = timestamp.isoformat()
                
                quantity = get_text(point, 'quantity')
                if quantity:
                    point_data['quantity'] = float(quantity)
                
                price = get_text(point, 'price.amount')
                if price:
                    point_data['price'] = float(price)
                
                # Imbalance price (for balancing documents)
                imbalance_price = get_text(point, 'imbalance_Price.amount')
                if imbalance_price:
                    point_data['imbalancePrice'] = float(imbalance_price)
                
                # Activation price
                activation_price = get_text(point, 'activation_Price.amount')
                if activation_price:
                    point_data['activationPrice'] = float(activation_price)
                
                period_data['points'].append(point_data)
                ts_data['totalPoints'] += 1
            
            ts_data['periods'].append(period_data)
        
        result['timeseries'].append(ts_data)
        result['totalDataPoints'] += ts_data['totalPoints']
    
    # Merge consecutive timeseries with same metadata
    result['timeseries'] = merge_consecutive_timeseries(result['timeseries'])
    result['timeseriesCount'] = len(result['timeseries'])
    result['totalDataPoints'] = sum(ts.get('totalPoints', 0) for ts in result['timeseries'])
    
    return result


def get_timeseries_signature(ts: Dict[str, Any]) -> str:
    """Generate a signature for a timeseries based on its metadata."""
    signature_fields = [
        'businessType', 'psrType', 'inBiddingZone', 'outBiddingZone',
        'in', 'out', 'controlArea', 'area', 'flowDirection', 
        'contractType', 'unit', 'currency'
    ]
    parts = []
    for field in signature_fields:
        if field in ts and ts[field]:
            parts.append(f"{field}={ts[field]}")
    return "|".join(sorted(parts))


def merge_consecutive_timeseries(timeseries_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge timeseries with same metadata but consecutive time periods."""
    if len(timeseries_list) <= 1:
        return timeseries_list
    
    # Group by signature
    groups = {}
    for ts in timeseries_list:
        sig = get_timeseries_signature(ts)
        if sig not in groups:
            groups[sig] = []
        groups[sig].append(ts)
    
    merged_list = []
    
    for sig, ts_group in groups.items():
        if len(ts_group) == 1:
            merged_list.append(ts_group[0])
            continue
        
        # Sort by start time of first period
        def get_start_time(ts):
            if ts.get('periods') and len(ts['periods']) > 0:
                start_str = ts['periods'][0].get('start', '')
                if start_str:
                    try:
                        return datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    except:
                        return datetime.min
            return datetime.min
        
        ts_group_sorted = sorted(ts_group, key=get_start_time)
        
        # Merge all into first one
        merged_ts = ts_group_sorted[0].copy()
        merged_ts['periods'] = list(ts_group_sorted[0].get('periods', []))
        
        for ts in ts_group_sorted[1:]:
            merged_ts['periods'].extend(ts.get('periods', []))
        
        merged_ts['totalPoints'] = sum(len(p.get('points', [])) for p in merged_ts['periods'])
        merged_ts['mRID'] = f"merged_{len(ts_group)}_series"
        
        merged_list.append(merged_ts)
    
    return merged_list


def dict_to_csv_rows(parsed_dict: Dict[str, Any]) -> List[List[str]]:
    """Convert parsed dict to CSV rows (including header)."""
    timeseries_list = parsed_dict.get('timeseries', [])
    
    if not timeseries_list:
        return [['timestamp']]
    
    # PSR type names for column naming
    psr_names = {
        'B01': 'Biomass', 'B04': 'FossilGas', 'B14': 'Nuclear',
        'B16': 'Solar', 'B18': 'WindOffshore', 'B19': 'WindOnshore'
    }
    
    # Generate column names
    columns = ['timestamp']
    ts_columns = {}
    
    for i, ts in enumerate(timeseries_list):
        psr = ts.get('psrType', '')
        name = psr_names.get(psr, psr) if psr else ts.get('businessType', f'series_{i}')
        unit = ts.get('unit', '')
        col_name = f"{name}_{unit}" if unit else name
        
        # Handle duplicates
        original = col_name
        counter = 1
        while col_name in columns:
            col_name = f"{original}_{counter}"
            counter += 1
        
        columns.append(col_name)
        ts_columns[i] = col_name
    
    # Collect data by timestamp
    data_by_ts = {}
    for i, ts in enumerate(timeseries_list):
        col = ts_columns[i]
        for period in ts.get('periods', []):
            for point in period.get('points', []):
                timestamp = point.get('timestamp', '')
                if not timestamp:
                    continue
                if timestamp not in data_by_ts:
                    data_by_ts[timestamp] = {}
                # Try different value fields
                value = (point.get('quantity') or point.get('price') or 
                         point.get('imbalancePrice') or point.get('activationPrice'))
                data_by_ts[timestamp][col] = value
    
    # Build rows
    rows = [columns]
    for timestamp in sorted(data_by_ts.keys()):
        row = [timestamp]
        for col in columns[1:]:
            val = data_by_ts[timestamp].get(col, '')
            row.append(str(val) if val is not None else '')
        rows.append(row)
    
    return rows


# =============================================================================
# MERGE FUNCTIONS
# =============================================================================

def merge_json_data(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Merge new JSON data into existing data."""
    if not existing or not existing.get('timeseries'):
        return new
    
    if not new or not new.get('timeseries'):
        return existing
    
    result = existing.copy()
    
    # Collect existing timestamps per timeseries
    existing_timestamps = {}
    for i, ts in enumerate(result.get('timeseries', [])):
        key = (ts.get('psrType', ''), ts.get('businessType', ''))
        if key not in existing_timestamps:
            existing_timestamps[key] = set()
        for period in ts.get('periods', []):
            for point in period.get('points', []):
                existing_timestamps[key].add(point.get('timestamp', ''))
    
    # Add new data
    for new_ts in new.get('timeseries', []):
        key = (new_ts.get('psrType', ''), new_ts.get('businessType', ''))
        
        # Find matching existing timeseries
        matched = False
        for existing_ts in result.get('timeseries', []):
            existing_key = (existing_ts.get('psrType', ''), existing_ts.get('businessType', ''))
            if key == existing_key:
                matched = True
                # Add new periods/points
                for new_period in new_ts.get('periods', []):
                    # Filter out duplicate points
                    filtered_points = [
                        p for p in new_period.get('points', [])
                        if p.get('timestamp', '') not in existing_timestamps.get(key, set())
                    ]
                    if filtered_points:
                        new_period_copy = new_period.copy()
                        new_period_copy['points'] = filtered_points
                        existing_ts['periods'].append(new_period_copy)
                        existing_ts['totalPoints'] = existing_ts.get('totalPoints', 0) + len(filtered_points)
                break
        
        if not matched:
            result['timeseries'].append(new_ts)
    
    # Update counts
    result['timeseriesCount'] = len(result['timeseries'])
    result['totalDataPoints'] = sum(ts.get('totalPoints', 0) for ts in result['timeseries'])
    
    # Update time interval
    all_starts = [result['timeInterval'].get('start', '')]
    all_ends = [result['timeInterval'].get('end', '')]
    if new.get('timeInterval'):
        all_starts.append(new['timeInterval'].get('start', ''))
        all_ends.append(new['timeInterval'].get('end', ''))
    
    result['timeInterval'] = {
        'start': min(s for s in all_starts if s),
        'end': max(e for e in all_ends if e)
    }
    
    return result


def append_csv_rows(existing_rows: List[List[str]], new_rows: List[List[str]]) -> List[List[str]]:
    """Append new CSV rows, avoiding duplicates by timestamp."""
    if not existing_rows:
        return new_rows
    
    if not new_rows or len(new_rows) <= 1:
        return existing_rows
    
    # Get existing timestamps
    existing_timestamps = {row[0] for row in existing_rows[1:]} if len(existing_rows) > 1 else set()
    
    # Header from existing
    result = existing_rows.copy()
    
    # Add new rows (skip header, skip duplicates)
    for row in new_rows[1:]:
        if row[0] not in existing_timestamps:
            result.append(row)
            existing_timestamps.add(row[0])
    
    return result


# =============================================================================
# MODAL FUNCTIONS
# =============================================================================

@app.function(
    image=image,
    volumes={VOLUME_PATH: volume},
    secrets=[modal.Secret.from_name("ENTSOE_API_KEY")],
    timeout=3600  # 1 hour for historical data
)
def fetch_historical(request: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch historical data (20 years) for a request."""
    import requests as http_requests
    
    name = request["name"]
    params = request["params"].copy()
    api_key = os.environ["ENTSOE_API_KEY"]
    
    print(f"📅 Fetching historical data for: {name}")
    
    # Set up directories
    xml_dir = VOLUME_PATH / "xml" / name
    json_dir = VOLUME_PATH / "json"
    csv_dir = VOLUME_PATH / "csv"
    
    xml_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    
    # Get historical time range
    start_str, end_str = get_historical_time_range()
    chunks = split_into_yearly_chunks(start_str, end_str)
    
    print(f"  📆 Fetching {len(chunks)} years of data...")
    
    all_parsed = []
    
    for i, (chunk_start, chunk_end, year_label) in enumerate(chunks, 1):
        print(f"  [{i}/{len(chunks)}] Year {year_label}...")
        
        chunk_params = params.copy()
        chunk_params['periodStart'] = chunk_start
        chunk_params['periodEnd'] = chunk_end
        chunk_params['securityToken'] = api_key
        
        try:
            response = http_requests.get(BASE_URL, params=chunk_params, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                response_content = response.content  # bytes, not text
                
                # Save as binary (preserves ZIP files)
                xml_path = xml_dir / f"{year_label}.xml"
                with open(xml_path, 'wb') as f:
                    f.write(response_content)
                
                # Extract XML and parse
                xml_content = get_xml_content(response_content)
                parsed = parse_xml_to_dict(xml_content)
                if not parsed.get('error'):
                    all_parsed.append(parsed)
                    print(f"    ✅ {parsed.get('totalDataPoints', 0)} points")
                else:
                    print(f"    ⚠️ No data for {year_label}")
            else:
                print(f"    ❌ HTTP {response.status_code}")
        
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        if i < len(chunks):
            time.sleep(REQUEST_DELAY)
    
    # Merge all parsed data
    merged = {}
    for parsed in all_parsed:
        merged = merge_json_data(merged, parsed)
    
    # Save JSON
    json_path = json_dir / f"{name}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, default=str)
    print(f"  💾 Saved JSON: {json_path.name}")
    
    # Save CSV
    csv_rows = dict_to_csv_rows(merged)
    csv_path = csv_dir / f"{name}.csv"
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        import csv
        writer = csv.writer(f)
        writer.writerows(csv_rows)
    print(f"  📄 Saved CSV: {csv_path.name} ({len(csv_rows)-1} rows)")
    
    # Commit volume changes
    volume.commit()
    
    return {
        "name": name,
        "chunks": len(chunks),
        "timeseries": merged.get('timeseriesCount', 0),
        "points": merged.get('totalDataPoints', 0)
    }


@app.function(
    image=image,
    volumes={VOLUME_PATH: volume},
    secrets=[modal.Secret.from_name("ENTSOE_API_KEY")],
    timeout=300  # 5 minutes for operational
)
def fetch_operational(request: Dict[str, Any], hours_back: int = 3) -> Dict[str, Any]:
    """Fetch operational data and append to existing files."""
    import requests as http_requests
    
    # CRITICAL: Reload volume to see changes from fetch_historical
    volume.reload()
    
    name = request["name"]
    params = request["params"].copy()
    api_key = os.environ["ENTSOE_API_KEY"]
    
    print(f"🔄 Fetching operational data for: {name}")
    
    # Set up paths
    xml_dir = VOLUME_PATH / "xml" / name
    json_dir = VOLUME_PATH / "json"
    csv_dir = VOLUME_PATH / "csv"
    
    xml_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = json_dir / f"{name}.json"
    csv_path = csv_dir / f"{name}.csv"
    
    # Get operational time range
    start_str, end_str = get_operational_time_range(hours_back)
    params['periodStart'] = start_str
    params['periodEnd'] = end_str
    params['securityToken'] = api_key
    
    print(f"  📆 Time range: {start_str} → {end_str}")
    
    try:
        response = http_requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            print(f"  ❌ HTTP {response.status_code}")
            return {"error": f"HTTP {response.status_code}"}
        
        response_content = response.content  # bytes, not text
        
        # Save as binary (preserves ZIP files)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M")
        xml_path = xml_dir / f"{timestamp}.xml"
        with open(xml_path, 'wb') as f:
            f.write(response_content)
        is_zip = is_zip_content(response_content)
        print(f"  💾 Saved {'ZIP' if is_zip else 'XML'}: {xml_path.name}")
        
        # Extract XML and parse
        xml_content = get_xml_content(response_content)
        new_parsed = parse_xml_to_dict(xml_content)
        
        if new_parsed.get('error'):
            print(f"  ⚠️ No data available")
            return {"warning": "No data available"}
        
        print(f"  📊 New data: {new_parsed.get('totalDataPoints', 0)} points")
        
        # Load existing JSON
        existing_json = {}
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                existing_json = json.load(f)
        
        # Merge JSON
        merged_json = merge_json_data(existing_json, new_parsed)
        
        # Save merged JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(merged_json, f, indent=2, default=str)
        print(f"  💾 Updated JSON: {json_path.name}")
        
        # Load existing CSV
        existing_csv = []
        if csv_path.exists():
            import csv
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                existing_csv = list(reader)
            print(f"  📂 Loaded existing CSV: {len(existing_csv)} rows")
        else:
            print(f"  ⚠️ No existing CSV found at {csv_path}")
        
        # Append CSV
        new_csv = dict_to_csv_rows(new_parsed)
        print(f"  📊 New CSV rows: {len(new_csv)}")
        merged_csv = append_csv_rows(existing_csv, new_csv)
        print(f"  🔀 Merged CSV: {len(merged_csv)} rows")
        
        # Save merged CSV
        import csv
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(merged_csv)
        print(f"  📄 Updated CSV: {csv_path.name} ({len(merged_csv)-1} total rows)")
        
        # Commit volume changes
        volume.commit()
        
        return {
            "name": name,
            "new_points": new_parsed.get('totalDataPoints', 0),
            "total_points": merged_json.get('totalDataPoints', 0)
        }
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {"error": str(e)}


@app.function(
    image=image,
    volumes={VOLUME_PATH: volume},
    secrets=[modal.Secret.from_name("ENTSOE_API_KEY")]
)
def check_historical_exists(name: str) -> bool:
    """Check if historical data already exists for a request."""
    # Reload volume to see latest state
    volume.reload()
    json_path = VOLUME_PATH / "json" / f"{name}.json"
    return json_path.exists()


@app.function(
    image=image,
    volumes={VOLUME_PATH: volume}
)
def upload_requests(requests_json: str):
    """Upload requests JSON to the volume."""
    requests_file = VOLUME_PATH / "my_requests.json"
    requests_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(requests_file, 'w', encoding='utf-8') as f:
        f.write(requests_json)
    
    volume.commit()
    print(f"✅ Uploaded requests to volume: {requests_file}")


# =============================================================================
# SCHEDULED CRON JOB
# =============================================================================

@app.function(
    image=image,
    volumes={VOLUME_PATH: volume},
    secrets=[modal.Secret.from_name("ENTSOE_API_KEY")],
    schedule=modal.Cron("0 * * * *"),  # Default: every hour
    timeout=3600
)
def scheduled_fetch():
    """
    Scheduled cron job that processes all Modal requests.
    
    For each request:
    1. Check if historical data exists
    2. If not, fetch historical first
    3. Then fetch operational data
    """
    print("\n" + "=" * 60)
    print("🕐 ENTSOE Scheduled Fetch Starting")
    print("=" * 60)
    
    # Load Modal requests from volume
    requests = load_modal_requests_from_volume()
    
    if not requests:
        print("⚠️ No Modal requests found in my_requests.json")
        return
    
    print(f"📋 Found {len(requests)} Modal request(s)\n")
    
    for i, req in enumerate(requests, 1):
        name = req["name"]
        print(f"\n[{i}/{len(requests)}] Processing: {name}")
        print("-" * 40)
        
        # Check if historical exists
        has_historical = check_historical_exists.remote(name)
        
        if not has_historical:
            print("  📅 No historical data found - fetching 20 years...")
            result = fetch_historical.remote(req)
            print(f"  ✅ Historical complete: {result.get('points', 0)} points")
        
        # Fetch operational
        schedule = req.get("schedule", "0 * * * *")
        # Extract hours from cron (simplified)
        hours_back = 3  # Default
        if "*/2" in schedule:
            hours_back = 3
        elif "*/6" in schedule:
            hours_back = 7
        
        result = fetch_operational.remote(req, hours_back)
        
        if "error" in result:
            print(f"  ❌ Operational failed: {result['error']}")
        else:
            print(f"  ✅ Operational: +{result.get('new_points', 0)} points (total: {result.get('total_points', 0)})")
    
    print("\n" + "=" * 60)
    print("✅ Scheduled fetch complete")
    print("=" * 60)


# =============================================================================
# LOCAL ENTRYPOINT
# =============================================================================

@app.local_entrypoint()
def main():
    """Run manually from command line."""
    print("\n" + "=" * 60)
    print("🚀 ENTSOE Modal Fetcher - Manual Run")
    print("=" * 60)
    
    # Load requests from local file
    requests = load_modal_requests_local()
    
    if not requests:
        print("\n⚠️ No Modal requests found!")
        print("Add requests to my_requests.json with 'run': 'modal'")
        return
    
    print(f"\n📋 Found {len(requests)} Modal request(s)")
    
    # Sync requests to volume
    print("\n📤 Syncing requests to Modal volume...")
    requests_file = LOCAL_PATH / "my_requests.json"
    with open(requests_file, 'r', encoding='utf-8') as f:
        requests_json = f.read()
    upload_requests.remote(requests_json)
    
    for req in requests:
        name = req["name"]
        print(f"\n📦 Processing: {name}")
        
        # Check historical
        has_historical = check_historical_exists.remote(name)
        
        if not has_historical:
            print("  Fetching historical data...")
            fetch_historical.remote(req)
        
        print("  Fetching operational data...")
        fetch_operational.remote(req)
    
    print("\n✅ Done!")


@app.local_entrypoint()
def sync_requests():
    """Sync local my_requests.json to Modal volume."""
    print("\n" + "=" * 60)
    print("📤 Syncing requests to Modal volume")
    print("=" * 60)
    
    requests_file = LOCAL_PATH / "my_requests.json"
    
    if not requests_file.exists():
        print(f"\n❌ my_requests.json not found at {requests_file}")
        return
    
    with open(requests_file, 'r', encoding='utf-8') as f:
        requests_json = f.read()
    
    # Parse to show what we're syncing
    data = json.loads(requests_json)
    modal_requests = [
        req for req in data.get("requests", [])
        if req.get("run") == "modal"
    ]
    
    print(f"\n📋 Found {len(modal_requests)} Modal request(s) to sync:")
    for req in modal_requests:
        print(f"   - {req['name']} ({req.get('schedule', 'no schedule')})")
    
    upload_requests.remote(requests_json)
    print("\n✅ Requests synced to volume!")

