"""
ENTSO-E XML Response Parser

This module provides parsing functionality for XML responses from the ENTSO-E 
Transparency Platform API. It extracts time series data and converts to JSON and CSV formats.

Supports both raw XML and ZIP-compressed responses (API returns ZIP for large responses).
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
import csv
import zipfile
import io
from typing import Dict, List, Any, Optional
from pathlib import Path


# =============================================================================
# ZIP HANDLING
# =============================================================================

def is_zip_content(content: bytes) -> bool:
    """Check if content is a ZIP file (starts with PK magic bytes)."""
    return content[:2] == b'PK'


def extract_xml_from_zip(zip_content: bytes) -> str:
    """Extract XML content from a ZIP file.
    
    Args:
        zip_content: Raw bytes of the ZIP file
        
    Returns:
        Extracted XML content as string
        
    Raises:
        ValueError: If no XML file found in ZIP
    """
    with zipfile.ZipFile(io.BytesIO(zip_content)) as zf:
        # Find the first XML file in the archive
        xml_files = [f for f in zf.namelist() if f.endswith('.xml')]
        if not xml_files:
            raise ValueError("No XML file found in ZIP archive")
        
        # Read the first XML file
        xml_filename = xml_files[0]
        with zf.open(xml_filename) as xml_file:
            return xml_file.read().decode('utf-8')


def read_xml_or_zip(file_path: str) -> str:
    """Read XML content from a file, handling both raw XML and ZIP files.
    
    Args:
        file_path: Path to the XML or ZIP file
        
    Returns:
        XML content as string
    """
    with open(file_path, 'rb') as f:
        content = f.read()
    
    if is_zip_content(content):
        return extract_xml_from_zip(content)
    else:
        return content.decode('utf-8')


# =============================================================================
# PSR TYPE NAMES (for CSV column naming)
# =============================================================================

PSR_TYPE_NAMES = {
    'B01': 'Biomass',
    'B02': 'Lignite',
    'B03': 'CoalGas',
    'B04': 'FossilGas',
    'B05': 'HardCoal',
    'B06': 'FossilOil',
    'B07': 'OilShale',
    'B08': 'Peat',
    'B09': 'Geothermal',
    'B10': 'HydroPumped',
    'B11': 'HydroRunOfRiver',
    'B12': 'HydroReservoir',
    'B13': 'Marine',
    'B14': 'Nuclear',
    'B15': 'OtherRenewable',
    'B16': 'Solar',
    'B17': 'Waste',
    'B18': 'WindOffshore',
    'B19': 'WindOnshore',
    'B20': 'Other',
}

BUSINESS_TYPE_NAMES = {
    'A01': 'Production',
    'A04': 'Consumption',
    'A14': 'AggregatedBids',
    'A37': 'InstalledCapacity',
    'A62': 'Price',
    'A66': 'PhysicalFlow',
    'B08': 'NominatedCapacity',
    'B10': 'CongestionIncome',
    'B33': 'ACE',
}


class ENTSOEXMLParser:
    """Parser for ENTSO-E API XML responses."""
    
    # Resolution to timedelta mapping
    RESOLUTION_MAP = {
        'PT1M': timedelta(minutes=1),
        'PT15M': timedelta(minutes=15),
        'PT30M': timedelta(minutes=30),
        'PT60M': timedelta(hours=1),
        'P1D': timedelta(days=1),
        'P7D': timedelta(days=7),
        'P1M': timedelta(days=30),  # Approximate
        'P1Y': timedelta(days=365),  # Approximate
    }
    
    def __init__(self, xml_content: str):
        """Initialize parser with XML content."""
        self.xml_content = xml_content
        self.root = ET.fromstring(xml_content)
        self.ns = self._detect_namespace()
        
    def _detect_namespace(self) -> str:
        """Detect the namespace from root element."""
        tag = self.root.tag
        if '{' in tag:
            return tag.split('}')[0] + '}'
        return ''
    
    def _find(self, element: ET.Element, path: str) -> Optional[ET.Element]:
        """Find element with namespace handling."""
        # Try with namespace
        result = element.find(f'{self.ns}{path}')
        if result is not None:
            return result
        # Try without namespace
        return element.find(path)
    
    def _findall(self, element: ET.Element, path: str) -> List[ET.Element]:
        """Find all elements with namespace handling."""
        result = element.findall(f'{self.ns}{path}')
        if not result:
            result = element.findall(path)
        return result
    
    def _get_text(self, element: ET.Element, path: str, default: str = '') -> str:
        """Get text content of child element."""
        child = self._find(element, path)
        return child.text if child is not None and child.text else default
    
    def is_no_data_response(self) -> bool:
        """Check if this is a 'no data' acknowledgement response."""
        return 'Acknowledgement_MarketDocument' in self.root.tag
    
    def get_error_reason(self) -> Optional[Dict[str, str]]:
        """Get error reason if this is an acknowledgement document."""
        if not self.is_no_data_response():
            return None
        
        reason = self._find(self.root, 'Reason')
        if reason is not None:
            return {
                'code': self._get_text(reason, 'code'),
                'text': self._get_text(reason, 'text')
            }
        return None
    
    def get_document_type(self) -> str:
        """Get the document type (root element name)."""
        tag = self.root.tag
        if '}' in tag:
            return tag.split('}')[1]
        return tag
    
    def get_document_info(self) -> Dict[str, Any]:
        """Extract document header information."""
        return {
            'documentType': self.get_document_type(),
            'mRID': self._get_text(self.root, 'mRID'),
            'revisionNumber': self._get_text(self.root, 'revisionNumber'),
            'type': self._get_text(self.root, 'type'),
            'processType': self._get_text(self.root, 'process.processType'),
            'createdDateTime': self._get_text(self.root, 'createdDateTime'),
        }
    
    def get_time_interval(self) -> Dict[str, str]:
        """Extract document time interval."""
        # Try different possible paths
        for path in ['time_Period.timeInterval', 'period.timeInterval']:
            interval = self._find(self.root, path)
            if interval is not None:
                return {
                    'start': self._get_text(interval, 'start'),
                    'end': self._get_text(interval, 'end')
                }
        return {'start': '', 'end': ''}
    
    def _parse_resolution(self, resolution: str) -> timedelta:
        """Convert resolution string to timedelta."""
        return self.RESOLUTION_MAP.get(resolution, timedelta(hours=1))
    
    def _parse_timeseries(self, ts: ET.Element) -> Dict[str, Any]:
        """Parse a single TimeSeries element."""
        timeseries = {
            'mRID': self._get_text(ts, 'mRID'),
            'businessType': self._get_text(ts, 'businessType'),
        }
        
        # Domain information (varies by document type)
        for domain_field in ['outBiddingZone_Domain.mRID', 'inBiddingZone_Domain.mRID',
                            'in_Domain.mRID', 'out_Domain.mRID', 
                            'controlArea_Domain.mRID', 'area_Domain.mRID']:
            value = self._get_text(ts, domain_field)
            if value:
                # Simplify field name
                key = domain_field.replace('.mRID', '').replace('_Domain', '')
                timeseries[key] = value
        
        # PSR Type (for generation data)
        psr_type = self._find(ts, 'MktPSRType')
        if psr_type is not None:
            timeseries['psrType'] = self._get_text(psr_type, 'psrType')
        
        # Flow direction (for balancing data)
        flow_dir = self._get_text(ts, 'flowDirection.direction')
        if flow_dir:
            timeseries['flowDirection'] = flow_dir
        
        # Contract/market agreement type
        contract_type = self._get_text(ts, 'contract_MarketAgreement.type')
        if contract_type:
            timeseries['contractType'] = contract_type
        
        # Unit and curve type
        timeseries['unit'] = self._get_text(ts, 'quantity_Measure_Unit.name')
        timeseries['curveType'] = self._get_text(ts, 'curveType')
        
        # Currency for price data
        currency = self._get_text(ts, 'currency_Unit.name')
        if currency:
            timeseries['currency'] = currency
        
        # Parse periods and points
        timeseries['periods'] = []
        for period in self._findall(ts, 'Period'):
            period_data = self._parse_period(period)
            timeseries['periods'].append(period_data)
        
        # Calculate total points
        total_points = sum(len(p['points']) for p in timeseries['periods'])
        timeseries['totalPoints'] = total_points
        
        return timeseries
    
    def _parse_period(self, period: ET.Element) -> Dict[str, Any]:
        """Parse a Period element."""
        interval = self._find(period, 'timeInterval')
        
        period_data = {
            'start': self._get_text(interval, 'start') if interval else '',
            'end': self._get_text(interval, 'end') if interval else '',
            'resolution': self._get_text(period, 'resolution'),
            'points': []
        }
        
        # Parse resolution for timestamp calculation
        resolution = self._parse_resolution(period_data['resolution'])
        start_time = None
        if period_data['start']:
            try:
                start_str = period_data['start'].replace('Z', '+00:00')
                start_time = datetime.fromisoformat(start_str)
            except ValueError:
                pass
        
        # Parse points
        for point in self._findall(period, 'Point'):
            point_data = self._parse_point(point, start_time, resolution)
            period_data['points'].append(point_data)
        
        return period_data
    
    def _parse_point(self, point: ET.Element, start_time: Optional[datetime], 
                     resolution: timedelta) -> Dict[str, Any]:
        """Parse a Point element."""
        position = int(self._get_text(point, 'position', '0'))
        
        point_data = {'position': position}
        
        # Calculate timestamp if possible
        if start_time:
            timestamp = start_time + resolution * (position - 1)
            point_data['timestamp'] = timestamp.isoformat()
        
        # Value fields (different for different data types)
        quantity = self._get_text(point, 'quantity')
        if quantity:
            point_data['quantity'] = float(quantity)
        
        price = self._get_text(point, 'price.amount')
        if price:
            point_data['price'] = float(price)
        
        # Imbalance price (for balancing documents)
        imbalance_price = self._get_text(point, 'imbalance_Price.amount')
        if imbalance_price:
            point_data['imbalancePrice'] = float(imbalance_price)
        
        # Imbalance price category
        imbalance_category = self._get_text(point, 'imbalance_Price.category')
        if imbalance_category:
            point_data['imbalancePriceCategory'] = imbalance_category
        
        # Secondary quantity (for bids)
        secondary = self._get_text(point, 'secondaryQuantity')
        if secondary:
            point_data['secondaryQuantity'] = float(secondary)
        
        # Unavailable quantity
        unavailable = self._get_text(point, 'unavailable_Quantity.quantity')
        if unavailable:
            point_data['unavailableQuantity'] = float(unavailable)
        
        # Activation price (for activated balancing energy)
        activation_price = self._get_text(point, 'activation_Price.amount')
        if activation_price:
            point_data['activationPrice'] = float(activation_price)
        
        return point_data
    
    def _get_timeseries_signature(self, ts: Dict[str, Any]) -> str:
        """
        Generate a signature for a timeseries based on its metadata.
        Used to identify timeseries that can be merged (same variable, different periods).
        """
        # Fields that identify the "same" timeseries (excluding mRID and time-related)
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
    
    def _merge_consecutive_timeseries(self, timeseries_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge timeseries that have the same metadata but consecutive time periods.
        This handles the common case where API returns one timeseries per day.
        """
        if len(timeseries_list) <= 1:
            return timeseries_list
        
        # Group by signature
        groups = {}
        for ts in timeseries_list:
            sig = self._get_timeseries_signature(ts)
            if sig not in groups:
                groups[sig] = []
            groups[sig].append(ts)
        
        merged_list = []
        
        for sig, ts_group in groups.items():
            if len(ts_group) == 1:
                # Only one timeseries with this signature, no merging needed
                merged_list.append(ts_group[0])
                continue
            
            # Sort by the start time of their first period
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
            
            # Merge all into the first one
            merged_ts = ts_group_sorted[0].copy()
            merged_ts['periods'] = list(ts_group_sorted[0].get('periods', []))
            
            for ts in ts_group_sorted[1:]:
                # Add periods from this timeseries
                merged_ts['periods'].extend(ts.get('periods', []))
            
            # Recalculate total points
            merged_ts['totalPoints'] = sum(len(p.get('points', [])) for p in merged_ts['periods'])
            
            # Update mRID to indicate merged
            merged_ts['mRID'] = f"merged_{len(ts_group)}_series"
            
            merged_list.append(merged_ts)
        
        return merged_list
    
    def extract_all_timeseries(self) -> List[Dict[str, Any]]:
        """Extract all TimeSeries from the document, merging consecutive ones."""
        if self.is_no_data_response():
            return []
        
        timeseries_list = []
        for ts in self._findall(self.root, 'TimeSeries'):
            ts_data = self._parse_timeseries(ts)
            timeseries_list.append(ts_data)
        
        # Merge consecutive timeseries with same metadata
        merged_list = self._merge_consecutive_timeseries(timeseries_list)
        
        return merged_list
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert parsed data to dictionary."""
        result = {
            'documentInfo': self.get_document_info(),
            'timeInterval': self.get_time_interval(),
        }
        
        if self.is_no_data_response():
            result['error'] = self.get_error_reason()
            result['timeseries'] = []
            result['timeseriesCount'] = 0
        else:
            result['timeseries'] = self.extract_all_timeseries()
            result['timeseriesCount'] = len(result['timeseries'])
            
            # Calculate total data points
            total_points = sum(
                ts.get('totalPoints', 0) for ts in result['timeseries']
            )
            result['totalDataPoints'] = total_points
        
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """Convert parsed data to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)


def parse_entsoe_xml(xml_file_path: str, json_output_path: str = None) -> Dict[str, Any]:
    """
    Parse an ENTSO-E XML file and optionally save as JSON.
    
    Handles both raw XML and ZIP-compressed responses (API returns ZIP for large responses).
    
    Args:
        xml_file_path: Path to the XML file (or ZIP file containing XML)
        json_output_path: Optional path to save JSON output
        
    Returns:
        Parsed data as dictionary
    """
    # Read file, handling both XML and ZIP formats
    xml_content = read_xml_or_zip(xml_file_path)
    
    parser = ENTSOEXMLParser(xml_content)
    result = parser.to_dict()
    
    if json_output_path:
        json_path = Path(json_output_path)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
    
    return result


def parse_xml_string(xml_content: str) -> Dict[str, Any]:
    """
    Parse XML content string directly.
    
    Args:
        xml_content: XML content as string
        
    Returns:
        Parsed data as dictionary
    """
    parser = ENTSOEXMLParser(xml_content)
    return parser.to_dict()


# =============================================================================
# CSV EXPORT FUNCTIONS
# =============================================================================

def _generate_column_name(ts: Dict[str, Any], index: int) -> str:
    """
    Generate a descriptive column name for a timeseries.
    
    Args:
        ts: Timeseries dictionary
        index: Index of the timeseries (fallback for naming)
        
    Returns:
        Column name string
    """
    parts = []
    
    # PSR Type (generation source)
    psr_type = ts.get('psrType', '')
    if psr_type:
        psr_name = PSR_TYPE_NAMES.get(psr_type, psr_type)
        parts.append(psr_name)
    
    # Business Type
    biz_type = ts.get('businessType', '')
    if biz_type and not psr_type:  # Only add if no PSR type
        biz_name = BUSINESS_TYPE_NAMES.get(biz_type, biz_type)
        parts.append(biz_name)
    
    # Flow direction
    flow_dir = ts.get('flowDirection', '')
    if flow_dir:
        parts.append('Up' if flow_dir == 'A01' else 'Down')
    
    # Domain info for flows
    in_domain = ts.get('in', '')
    out_domain = ts.get('out', '')
    if in_domain and out_domain:
        # Shorten domain codes
        in_short = in_domain[-8:-1] if len(in_domain) > 8 else in_domain
        out_short = out_domain[-8:-1] if len(out_domain) > 8 else out_domain
        parts.append(f"{out_short}_to_{in_short}")
    
    # Unit
    unit = ts.get('unit', '') or ts.get('currency', '')
    if unit:
        parts.append(unit)
    
    # Fallback to index if no parts
    if not parts:
        parts.append(f"series_{index}")
    
    return '_'.join(parts)


def _get_value_from_point(point: Dict[str, Any]) -> Optional[float]:
    """
    Extract the primary value from a point.
    
    Args:
        point: Point dictionary
        
    Returns:
        Value (quantity, price, imbalancePrice, etc.) or None
    """
    # Try different value fields in order of preference
    for field in ['quantity', 'price', 'imbalancePrice', 'activationPrice', 
                  'secondaryQuantity', 'unavailableQuantity']:
        if field in point:
            return point[field]
    return None


def parsed_to_csv(parsed_dict: Dict[str, Any], csv_output_path: str) -> Dict[str, Any]:
    """
    Convert parsed ENTSO-E data to CSV format.
    
    Creates a tabular format with:
    - First column: timestamp
    - One column per timeseries (named by metadata)
    
    Args:
        parsed_dict: Parsed data dictionary (from parse_entsoe_xml)
        csv_output_path: Path to save the CSV file
        
    Returns:
        Dictionary with CSV export info (columns, rows count)
    """
    timeseries_list = parsed_dict.get('timeseries', [])
    
    # Handle no data case
    if not timeseries_list:
        csv_path = Path(csv_output_path)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp'])  # Header only
        return {'columns': ['timestamp'], 'rows': 0, 'path': str(csv_path)}
    
    # Generate column names for each timeseries
    column_names = ['timestamp']
    ts_columns = {}  # Map timeseries index to column name
    
    for i, ts in enumerate(timeseries_list):
        col_name = _generate_column_name(ts, i)
        # Handle duplicate column names
        original_name = col_name
        counter = 1
        while col_name in column_names:
            col_name = f"{original_name}_{counter}"
            counter += 1
        column_names.append(col_name)
        ts_columns[i] = col_name
    
    # Collect all data points by timestamp
    data_by_timestamp = {}
    
    for i, ts in enumerate(timeseries_list):
        col_name = ts_columns[i]
        for period in ts.get('periods', []):
            for point in period.get('points', []):
                timestamp = point.get('timestamp', '')
                if not timestamp:
                    continue
                
                value = _get_value_from_point(point)
                
                if timestamp not in data_by_timestamp:
                    data_by_timestamp[timestamp] = {}
                
                data_by_timestamp[timestamp][col_name] = value
    
    # Sort timestamps and write CSV
    sorted_timestamps = sorted(data_by_timestamp.keys())
    
    csv_path = Path(csv_output_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(column_names)
        
        # Write data rows
        for timestamp in sorted_timestamps:
            row = [timestamp]
            ts_data = data_by_timestamp[timestamp]
            for col in column_names[1:]:  # Skip timestamp column
                value = ts_data.get(col, '')
                row.append(value if value is not None else '')
            writer.writerow(row)
    
    return {
        'columns': column_names,
        'rows': len(sorted_timestamps),
        'path': str(csv_path)
    }


def parse_entsoe_xml_full(xml_file_path: str, json_output_path: str = None, 
                          csv_output_path: str = None) -> Dict[str, Any]:
    """
    Parse an ENTSO-E XML file and optionally save as JSON and/or CSV.
    
    Handles both raw XML and ZIP-compressed responses (API returns ZIP for large responses).
    
    Args:
        xml_file_path: Path to the XML file (or ZIP file containing XML)
        json_output_path: Optional path to save JSON output
        csv_output_path: Optional path to save CSV output
        
    Returns:
        Parsed data as dictionary (with csv_info if CSV was exported)
    """
    # Read file, handling both XML and ZIP formats
    xml_content = read_xml_or_zip(xml_file_path)
    
    parser = ENTSOEXMLParser(xml_content)
    result = parser.to_dict()
    
    # Save JSON if path provided
    if json_output_path:
        json_path = Path(json_output_path)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
    
    # Save CSV if path provided
    if csv_output_path:
        csv_info = parsed_to_csv(result, csv_output_path)
        result['csvInfo'] = csv_info
    
    return result


# =============================================================================
# JSON/CSV MERGE FUNCTIONS (for appending operational data)
# =============================================================================

def merge_json_files(existing_path: str, new_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
    """
    Merge new JSON data into an existing JSON file.
    
    Combines timeseries, avoiding duplicate timestamps.
    
    Args:
        existing_path: Path to existing JSON file
        new_data: New parsed data dictionary to merge
        output_path: Optional output path (defaults to existing_path)
        
    Returns:
        Merged data dictionary
    """
    existing_file = Path(existing_path)
    
    # Load existing data
    existing_data = {}
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    
    if not existing_data or not existing_data.get('timeseries'):
        merged = new_data
    elif not new_data or not new_data.get('timeseries'):
        merged = existing_data
    else:
        merged = _merge_json_data(existing_data, new_data)
    
    # Save merged result
    out_path = Path(output_path) if output_path else existing_file
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, default=str)
    
    return merged


def _merge_json_data(existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """
    Internal function to merge two JSON data dictionaries.
    
    Args:
        existing: Existing parsed data
        new: New parsed data to merge
        
    Returns:
        Merged data dictionary
    """
    result = existing.copy()
    result['timeseries'] = list(existing.get('timeseries', []))
    
    # Collect existing timestamps per timeseries key
    existing_timestamps = {}
    for ts in result.get('timeseries', []):
        key = _get_timeseries_key(ts)
        if key not in existing_timestamps:
            existing_timestamps[key] = set()
        for period in ts.get('periods', []):
            for point in period.get('points', []):
                ts_val = point.get('timestamp', '')
                if ts_val:
                    existing_timestamps[key].add(ts_val)
    
    # Process new timeseries
    for new_ts in new.get('timeseries', []):
        key = _get_timeseries_key(new_ts)
        
        # Find matching existing timeseries
        matched_idx = None
        for idx, existing_ts in enumerate(result['timeseries']):
            if _get_timeseries_key(existing_ts) == key:
                matched_idx = idx
                break
        
        if matched_idx is not None:
            # Add new periods/points to existing timeseries
            existing_ts = result['timeseries'][matched_idx]
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
        else:
            # Add new timeseries
            result['timeseries'].append(new_ts)
    
    # Update counts
    result['timeseriesCount'] = len(result['timeseries'])
    result['totalDataPoints'] = sum(ts.get('totalPoints', 0) for ts in result['timeseries'])
    
    # Update time interval
    starts = [result['timeInterval'].get('start', '')]
    ends = [result['timeInterval'].get('end', '')]
    if new.get('timeInterval'):
        starts.append(new['timeInterval'].get('start', ''))
        ends.append(new['timeInterval'].get('end', ''))
    
    starts = [s for s in starts if s]
    ends = [e for e in ends if e]
    
    result['timeInterval'] = {
        'start': min(starts) if starts else '',
        'end': max(ends) if ends else ''
    }
    
    return result


def _get_timeseries_key(ts: Dict[str, Any]) -> tuple:
    """Generate a key to identify a timeseries for merging."""
    return (
        ts.get('psrType', ''),
        ts.get('businessType', ''),
        ts.get('outBiddingZone', ''),
        ts.get('inBiddingZone', ''),
        ts.get('in', ''),
        ts.get('out', ''),
        ts.get('flowDirection', ''),
    )


def append_csv_file(existing_path: str, new_data: Dict[str, Any], output_path: str = None) -> Dict[str, Any]:
    """
    Append new CSV rows to an existing CSV file, avoiding duplicates.
    
    Args:
        existing_path: Path to existing CSV file
        new_data: New parsed data dictionary
        output_path: Optional output path (defaults to existing_path)
        
    Returns:
        Info dict with row counts
    """
    existing_file = Path(existing_path)
    out_file = Path(output_path) if output_path else existing_file
    
    # Load existing CSV
    existing_rows = []
    existing_timestamps = set()
    
    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)
            existing_rows = list(reader)
        
        # Collect existing timestamps (skip header)
        if len(existing_rows) > 1:
            existing_timestamps = {row[0] for row in existing_rows[1:]}
    
    # Generate new CSV data
    new_csv_info = parsed_to_csv(new_data, '/tmp/temp_csv.csv')
    
    # Read new CSV
    with open('/tmp/temp_csv.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        new_rows = list(reader)
    
    # Merge
    if not existing_rows:
        merged_rows = new_rows
    else:
        merged_rows = existing_rows.copy()
        # Add new rows (skip header, avoid duplicates)
        for row in new_rows[1:]:
            if row[0] not in existing_timestamps:
                merged_rows.append(row)
                existing_timestamps.add(row[0])
    
    # Save merged CSV
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(merged_rows)
    
    # Clean up temp file
    Path('/tmp/temp_csv.csv').unlink(missing_ok=True)
    
    return {
        'existing_rows': len(existing_rows) - 1 if existing_rows else 0,
        'new_rows': len(new_rows) - 1 if new_rows else 0,
        'total_rows': len(merged_rows) - 1 if merged_rows else 0,
        'path': str(out_file)
    }


# =============================================================================
# MULTI-FILE MERGE FUNCTIONS (for historical data)
# =============================================================================

def merge_parsed_results(parsed_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple parsed XML results into a single combined result.
    
    Used for historical data requests where multiple years of data
    are fetched separately and need to be combined.
    
    Args:
        parsed_list: List of parsed result dictionaries
        
    Returns:
        Merged result dictionary with combined timeseries
    """
    if not parsed_list:
        return {
            'documentInfo': {},
            'timeInterval': {'start': '', 'end': ''},
            'timeseries': [],
            'timeseriesCount': 0,
            'totalDataPoints': 0,
            'chunksWithData': 0,
            'isMerged': True
        }
    
    # Filter out no-data responses
    valid_results = [r for r in parsed_list if not r.get('error') and r.get('timeseries')]
    chunks_with_data = len(valid_results)
    
    if not valid_results:
        # All chunks had no data - return first result's structure with error info
        return {
            'documentInfo': parsed_list[0].get('documentInfo', {}),
            'timeInterval': _get_merged_time_interval(parsed_list),
            'timeseries': [],
            'timeseriesCount': 0,
            'totalDataPoints': 0,
            'chunksWithData': 0,
            'isMerged': True,
            'error': {'code': 'NO_DATA', 'text': 'No data available for any chunk in the requested period'}
        }
    
    # Use first valid result as base for document info
    base = valid_results[0]
    
    # Merge all timeseries
    all_timeseries = []
    for result in valid_results:
        all_timeseries.extend(result.get('timeseries', []))
    
    # Group timeseries by their identifying characteristics
    merged_timeseries = _merge_timeseries_by_type(all_timeseries)
    
    # Calculate totals
    total_points = sum(ts.get('totalPoints', 0) for ts in merged_timeseries)
    
    return {
        'documentInfo': base.get('documentInfo', {}),
        'timeInterval': _get_merged_time_interval(parsed_list),
        'timeseries': merged_timeseries,
        'timeseriesCount': len(merged_timeseries),
        'totalDataPoints': total_points,
        'chunksWithData': chunks_with_data,
        'isMerged': True
    }


def _get_merged_time_interval(parsed_list: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Calculate the overall time interval spanning all parsed results.
    
    Args:
        parsed_list: List of parsed results
        
    Returns:
        Time interval dict with earliest start and latest end
    """
    starts = []
    ends = []
    
    for result in parsed_list:
        interval = result.get('timeInterval', {})
        if interval.get('start'):
            starts.append(interval['start'])
        if interval.get('end'):
            ends.append(interval['end'])
    
    return {
        'start': min(starts) if starts else '',
        'end': max(ends) if ends else ''
    }


def _merge_timeseries_by_type(timeseries_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge timeseries that have the same identifying characteristics.
    
    Timeseries are grouped by: businessType, psrType, domain fields, etc.
    Their periods are combined chronologically.
    
    Args:
        timeseries_list: List of all timeseries from multiple chunks
        
    Returns:
        List of merged timeseries
    """
    # Group timeseries by their key characteristics
    groups = {}
    
    for ts in timeseries_list:
        # Create a key from identifying fields
        key_parts = [
            ts.get('businessType', ''),
            ts.get('psrType', ''),
            ts.get('outBiddingZone', ''),
            ts.get('inBiddingZone', ''),
            ts.get('in', ''),
            ts.get('out', ''),
            ts.get('controlArea', ''),
            ts.get('area', ''),
            ts.get('flowDirection', ''),
            ts.get('contractType', ''),
        ]
        key = tuple(k for k in key_parts if k)  # Only non-empty values
        
        if key not in groups:
            groups[key] = []
        groups[key].append(ts)
    
    # Merge each group
    merged = []
    for key, ts_group in groups.items():
        merged_ts = _merge_single_timeseries_group(ts_group)
        merged.append(merged_ts)
    
    return merged


def _merge_single_timeseries_group(ts_group: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge a group of timeseries with the same characteristics.
    
    Args:
        ts_group: List of timeseries to merge
        
    Returns:
        Single merged timeseries
    """
    if len(ts_group) == 1:
        return ts_group[0]
    
    # Use first as base
    base = ts_group[0].copy()
    
    # Collect all periods from all timeseries
    all_periods = []
    for ts in ts_group:
        all_periods.extend(ts.get('periods', []))
    
    # Sort periods by start time
    all_periods.sort(key=lambda p: p.get('start', ''))
    
    # Update base with merged periods
    base['periods'] = all_periods
    base['totalPoints'] = sum(len(p.get('points', [])) for p in all_periods)
    
    return base


def parse_and_merge_xml_folder(folder_path: str, json_output_path: str = None,
                                csv_output_path: str = None) -> Dict[str, Any]:
    """
    Parse all XML files in a folder and merge into a single result.
    
    Used for historical requests where each year's data is saved
    as a separate XML file.
    
    Args:
        folder_path: Path to folder containing XML files
        json_output_path: Optional path to save merged JSON output
        csv_output_path: Optional path to save merged CSV output
        
    Returns:
        Merged result dictionary
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        raise ValueError(f"Folder not found: {folder_path}")
    
    # Find all XML files, sorted by name (year order)
    xml_files = sorted(folder.glob('*.xml'))
    
    if not xml_files:
        raise ValueError(f"No XML files found in: {folder_path}")
    
    # Parse each file
    parsed_results = []
    for xml_file in xml_files:
        try:
            result = parse_entsoe_xml(str(xml_file))
            parsed_results.append(result)
        except Exception as e:
            # Log but continue with other files
            print(f"  ⚠️ Error parsing {xml_file.name}: {e}")
    
    if not parsed_results:
        raise ValueError(f"Could not parse any XML files in: {folder_path}")
    
    # Merge all results
    merged = merge_parsed_results(parsed_results)
    
    # Save JSON if output path provided
    if json_output_path:
        json_path = Path(json_output_path)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, default=str)
    
    # Save CSV if output path provided
    if csv_output_path:
        csv_info = parsed_to_csv(merged, csv_output_path)
        merged['csvInfo'] = csv_info
    
    return merged


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m src.parser <xml_file> [json_output]")
        print("\nExample:")
        print("  python -m src.parser results/E11_v1_load_CZ_1day.xml")
        print("  python -m src.parser results/E11_v1_load_CZ_1day.xml output.json")
        sys.exit(1)
    
    xml_path = sys.argv[1]
    json_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = parse_entsoe_xml(xml_path, json_path)
        
        print(f"\n{'='*60}")
        print(f"📄 File: {xml_path}")
        print(f"{'='*60}")
        print(f"Document Type: {result['documentInfo'].get('documentType')}")
        print(f"Data Type Code: {result['documentInfo'].get('type')}")
        print(f"Time Range: {result['timeInterval'].get('start')} → {result['timeInterval'].get('end')}")
        print(f"TimeSeries Count: {result.get('timeseriesCount', 0)}")
        print(f"Total Data Points: {result.get('totalDataPoints', 0)}")
        
        if result.get('error'):
            print(f"\n⚠️  Error: {result['error'].get('text')}")
        
        if json_path:
            print(f"\n✅ JSON saved to: {json_path}")
            
    except Exception as e:
        print(f"❌ Error parsing {xml_path}: {e}")
        sys.exit(1)

