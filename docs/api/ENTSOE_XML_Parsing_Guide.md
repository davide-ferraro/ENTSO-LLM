# ENTSO-E API XML Response Parsing Guide

> **Purpose:** This guide explains how to parse XML responses from the ENTSO-E Transparency Platform API and extract time series data into structured JSON format.

---

## 📋 Table of Contents

1. [XML Document Types](#xml-document-types)
2. [Common XML Structure](#common-xml-structure)
3. [TimeSeries Extraction](#timeseries-extraction)
4. [Point Data Extraction](#point-data-extraction)
5. [Handling Multiple TimeSeries](#handling-multiple-timeseries)
6. [No Data Responses](#no-data-responses)
7. [Python Parsing Code](#python-parsing-code)
8. [JSON Output Format](#json-output-format)

---

## XML Document Types

The API returns different root document types depending on the data requested:

| Document Type | Root Element | Used For |
|---------------|--------------|----------|
| Generation/Load | `GL_MarketDocument` | Load data (A65), Generation (A73, A75), Installed capacity (A68) |
| Market/Publication | `Publication_MarketDocument` | Prices (A44), Flows (A11), Capacity (A26, A61), Schedules (A09) |
| Balancing | `Balancing_MarketDocument` | ACE (A86), Imbalance (A85, A86), Bids (A24, A37) |
| Unavailability | `Unavailability_MarketDocument` | Outages (A78, A80) |
| Error/No Data | `Acknowledgement_MarketDocument` | Error responses, no data available |

### Namespaces

```xml
<!-- Generation/Load -->
xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"

<!-- Publication/Market -->
xmlns="urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0"
xmlns="urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"

<!-- Balancing -->
xmlns="urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:1"

<!-- Acknowledgement (errors) -->
xmlns="urn:iec62325.351:tc57wg16:451-1:acknowledgementdocument:7:0"
```

---

## Common XML Structure

### Document Header

All responses contain a standard header:

```xml
<?xml version="1.0" encoding="utf-8"?>
<GL_MarketDocument xmlns="...">
  <mRID>unique-document-id</mRID>
  <revisionNumber>1</revisionNumber>
  <type>A65</type>                              <!-- Document type code -->
  <process.processType>A16</process.processType> <!-- Process type -->
  <sender_MarketParticipant.mRID>...</sender_MarketParticipant.mRID>
  <receiver_MarketParticipant.mRID>...</receiver_MarketParticipant.mRID>
  <createdDateTime>2026-01-08T18:45:41Z</createdDateTime>
  <time_Period.timeInterval>                    <!-- OR period.timeInterval -->
    <start>2026-01-07T22:00Z</start>
    <end>2026-01-08T22:00Z</end>
  </time_Period.timeInterval>
  
  <TimeSeries>...</TimeSeries>                  <!-- One or more -->
</GL_MarketDocument>
```

### Key Header Fields

| Field | Description |
|-------|-------------|
| `mRID` | Unique document identifier |
| `type` | Document type code (A65, A44, A11, etc.) |
| `process.processType` | Process type (A16=realised, A01=day-ahead, etc.) |
| `createdDateTime` | When the response was generated |
| `time_Period.timeInterval` | Requested time range |

---

## TimeSeries Extraction

### Basic TimeSeries Structure

```xml
<TimeSeries>
  <mRID>1</mRID>                                <!-- Series identifier -->
  <businessType>A04</businessType>              <!-- Business type code -->
  <objectAggregation>A01</objectAggregation>    <!-- Optional -->
  
  <!-- Domain identifiers (varies by data type) -->
  <outBiddingZone_Domain.mRID>10YCZ-CEPS-----N</outBiddingZone_Domain.mRID>
  <!-- OR -->
  <in_Domain.mRID>10YBE----------2</in_Domain.mRID>
  <out_Domain.mRID>10YDE-RWENET---I</out_Domain.mRID>
  <!-- OR -->
  <inBiddingZone_Domain.mRID>10YBE----------2</inBiddingZone_Domain.mRID>
  
  <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
  <curveType>A03</curveType>
  
  <!-- Optional: PSR Type for generation data -->
  <MktPSRType>
    <psrType>B01</psrType>                      <!-- Biomass, B04=Fossil Gas, etc. -->
  </MktPSRType>
  
  <!-- Optional: Flow direction for balancing -->
  <flowDirection.direction>A01</flowDirection.direction>  <!-- A01=up, A02=down -->
  
  <Period>...</Period>                          <!-- One or more periods -->
</TimeSeries>
```

### TimeSeries Metadata Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `businessType` | Type of data | A01 (production), A04 (consumption), A62 (price), B08 (capacity), B33 (ACE) |
| `psrType` | Power System Resource type | B01 (Biomass), B04 (Fossil Gas), B16 (Solar), B19 (Wind Onshore) |
| `flowDirection.direction` | Direction | A01 (up/positive), A02 (down/negative) |
| `quantity_Measure_Unit.name` | Unit | MAW (MW), MWH (MWh) |
| `curveType` | Curve type | A01 (sequential), A03 (variable) |

---

## Point Data Extraction

### Period and Points Structure

```xml
<Period>
  <timeInterval>
    <start>2026-01-07T22:00Z</start>
    <end>2026-01-08T22:00Z</end>
  </timeInterval>
  <resolution>PT15M</resolution>                 <!-- Time resolution -->
  
  <Point>
    <position>1</position>                       <!-- Position in sequence -->
    <quantity>8669.39</quantity>                 <!-- Value (MW or MWh) -->
  </Point>
  <Point>
    <position>2</position>
    <quantity>8548.76</quantity>
  </Point>
  <!-- ... more points ... -->
</Period>
```

### Resolution Codes

| Code | Duration | Typical Use |
|------|----------|-------------|
| `PT1M` | 1 minute | ACE data |
| `PT15M` | 15 minutes | Most operational data |
| `PT30M` | 30 minutes | Some UK data |
| `PT60M` | 1 hour | Day-ahead prices, schedules |
| `P1D` | 1 day | Daily aggregates |
| `P7D` | 1 week | Weekly data |
| `P1M` | 1 month | Monthly data |
| `P1Y` | 1 year | Annual installed capacity |

### Point Value Fields

Different data types have different value fields:

| Data Type | Value Field | Example |
|-----------|-------------|---------|
| Load, Generation, Flows | `<quantity>8669.39</quantity>` | MW value |
| Prices | `<price.amount>102.55</price.amount>` | EUR/MWh |
| Balancing Bids | `<quantity>173</quantity>` + `<secondaryQuantity>1.319</secondaryQuantity>` | Volume + Price |

---

## Handling Multiple TimeSeries

### When Multiple TimeSeries Occur

1. **Generation by Type (A75):** One TimeSeries per PSR type (B01, B04, B16, etc.)
2. **Capacity per Border:** Separate TimeSeries for each direction
3. **ACE Data (A86):** Many TimeSeries for minute-by-minute data with direction changes
4. **Installed Capacity (A68):** One TimeSeries per generation type

### Example: Multiple TimeSeries (Generation by Type)

```xml
<GL_MarketDocument>
  <!-- TimeSeries 1: Biomass -->
  <TimeSeries>
    <mRID>1</mRID>
    <MktPSRType><psrType>B01</psrType></MktPSRType>
    <Period>
      <Point><position>1</position><quantity>45.01</quantity></Point>
    </Period>
  </TimeSeries>
  
  <!-- TimeSeries 2: Fossil Gas -->
  <TimeSeries>
    <mRID>2</mRID>
    <MktPSRType><psrType>B04</psrType></MktPSRType>
    <Period>
      <Point><position>1</position><quantity>1250.5</quantity></Point>
    </Period>
  </TimeSeries>
  
  <!-- ... more for B06, B10, B11, B14, B16, B17, B18, B19, B20 ... -->
</GL_MarketDocument>
```

---

## No Data Responses

When no data is available, the API returns an `Acknowledgement_MarketDocument`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Acknowledgement_MarketDocument
    xmlns="urn:iec62325.351:tc57wg16:451-1:acknowledgementdocument:7:0">
  <mRID>1baecd4d-6a8a-4</mRID>
  <createdDateTime>2026-01-08T19:02:45Z</createdDateTime>
  <sender_MarketParticipant.mRID>10X1001A1001A450</sender_MarketParticipant.mRID>
  <receiver_MarketParticipant.mRID>10X1001A1001A450</receiver_MarketParticipant.mRID>
  <Reason>
    <code>999</code>
    <text>No matching data found for Data item COMMERCIAL_SCHEDULES [12.1.F] 
          (10YAT-APG------L, 10YAT-APG------L) and interval .</text>
  </Reason>
</Acknowledgement_MarketDocument>
```

### Detecting No Data

Check for:
1. Root element `Acknowledgement_MarketDocument`
2. Presence of `<Reason>` element
3. `<code>999</code>` (no data)

---

## Python Parsing Code

### Complete Parser Implementation

```python
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import json
from typing import Dict, List, Any, Optional

class ENTSOEXMLParser:
    """Parser for ENTSO-E API XML responses."""
    
    # Namespace mappings
    NAMESPACES = {
        'gl': 'urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0',
        'pub': 'urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0',
        'pub73': 'urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3',
        'bal': 'urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:1',
        'ack': 'urn:iec62325.351:tc57wg16:451-1:acknowledgementdocument:7:0',
    }
    
    # Resolution to timedelta
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
    
    def get_document_info(self) -> Dict[str, Any]:
        """Extract document header information."""
        return {
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
                start_time = datetime.fromisoformat(
                    period_data['start'].replace('Z', '+00:00')
                )
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
        
        # Secondary quantity (for bids)
        secondary = self._get_text(point, 'secondaryQuantity')
        if secondary:
            point_data['secondaryQuantity'] = float(secondary)
        
        # Unavailable quantity
        unavailable = self._get_text(point, 'unavailable_Quantity.quantity')
        if unavailable:
            point_data['unavailableQuantity'] = float(unavailable)
        
        return point_data
    
    def extract_all_timeseries(self) -> List[Dict[str, Any]]:
        """Extract all TimeSeries from the document."""
        if self.is_no_data_response():
            return []
        
        timeseries_list = []
        for ts in self._findall(self.root, 'TimeSeries'):
            ts_data = self._parse_timeseries(ts)
            timeseries_list.append(ts_data)
        
        return timeseries_list
    
    def to_json(self, indent: int = 2) -> str:
        """Convert parsed data to JSON string."""
        result = {
            'documentInfo': self.get_document_info(),
            'timeInterval': self.get_time_interval(),
        }
        
        if self.is_no_data_response():
            result['error'] = self.get_error_reason()
            result['timeseries'] = []
        else:
            result['timeseries'] = self.extract_all_timeseries()
            result['timeseriesCount'] = len(result['timeseries'])
        
        return json.dumps(result, indent=indent, default=str)


def parse_entsoe_xml(xml_file_path: str, json_output_path: str = None) -> Dict:
    """
    Parse an ENTSO-E XML file and optionally save as JSON.
    
    Args:
        xml_file_path: Path to the XML file
        json_output_path: Optional path to save JSON output
        
    Returns:
        Parsed data as dictionary
    """
    with open(xml_file_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    parser = ENTSOEXMLParser(xml_content)
    
    result = {
        'documentInfo': parser.get_document_info(),
        'timeInterval': parser.get_time_interval(),
    }
    
    if parser.is_no_data_response():
        result['error'] = parser.get_error_reason()
        result['timeseries'] = []
    else:
        result['timeseries'] = parser.extract_all_timeseries()
        result['timeseriesCount'] = len(result['timeseries'])
    
    if json_output_path:
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
    
    return result


# Example usage
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python parser.py <xml_file> [json_output]")
        sys.exit(1)
    
    xml_path = sys.argv[1]
    json_path = sys.argv[2] if len(sys.argv) > 2 else xml_path.replace('.xml', '.json')
    
    result = parse_entsoe_xml(xml_path, json_path)
    
    print(f"Parsed {result.get('timeseriesCount', 0)} time series")
    print(f"Document type: {result['documentInfo'].get('type')}")
    print(f"Time range: {result['timeInterval'].get('start')} to {result['timeInterval'].get('end')}")
```

---

## JSON Output Format

### Successful Response

```json
{
  "documentInfo": {
    "mRID": "eeecce63b6104e789e1c48300ddd0846",
    "revisionNumber": "1",
    "type": "A65",
    "processType": "A16",
    "createdDateTime": "2026-01-08T18:45:41Z"
  },
  "timeInterval": {
    "start": "2026-01-07T22:00Z",
    "end": "2026-01-08T18:00Z"
  },
  "timeseriesCount": 1,
  "timeseries": [
    {
      "mRID": "1",
      "businessType": "A04",
      "outBiddingZone": "10YCZ-CEPS-----N",
      "unit": "MAW",
      "curveType": "A03",
      "periods": [
        {
          "start": "2026-01-07T22:00Z",
          "end": "2026-01-08T18:00Z",
          "resolution": "PT15M",
          "points": [
            {"position": 1, "timestamp": "2026-01-07T22:00:00+00:00", "quantity": 8669.39},
            {"position": 2, "timestamp": "2026-01-07T22:15:00+00:00", "quantity": 8548.76},
            {"position": 3, "timestamp": "2026-01-07T22:30:00+00:00", "quantity": 8424.44}
          ]
        }
      ]
    }
  ]
}
```

### No Data Response

```json
{
  "documentInfo": {
    "mRID": "1baecd4d-6a8a-4",
    "revisionNumber": "",
    "type": "",
    "processType": "",
    "createdDateTime": "2026-01-08T19:02:45Z"
  },
  "timeInterval": {
    "start": "",
    "end": ""
  },
  "error": {
    "code": "999",
    "text": "No matching data found for Data item COMMERCIAL_SCHEDULES [12.1.F]..."
  },
  "timeseries": []
}
```

### Multiple TimeSeries (Generation by Type)

```json
{
  "documentInfo": {
    "type": "A75"
  },
  "timeseriesCount": 10,
  "timeseries": [
    {
      "mRID": "1",
      "businessType": "A01",
      "inBiddingZone": "10YBE----------2",
      "psrType": "B01",
      "unit": "MAW",
      "periods": [{"resolution": "PT60M", "points": [...]}]
    },
    {
      "mRID": "2",
      "businessType": "A01",
      "psrType": "B04",
      "periods": [{"resolution": "PT60M", "points": [...]}]
    }
  ]
}
```

---

## PSR Type Reference

| Code | Generation Type |
|------|-----------------|
| B01 | Biomass |
| B02 | Fossil Brown coal/Lignite |
| B03 | Fossil Coal-derived gas |
| B04 | Fossil Gas |
| B05 | Fossil Hard coal |
| B06 | Fossil Oil |
| B07 | Fossil Oil shale |
| B08 | Fossil Peat |
| B09 | Geothermal |
| B10 | Hydro Pumped Storage |
| B11 | Hydro Run-of-river |
| B12 | Hydro Water Reservoir |
| B13 | Marine |
| B14 | Nuclear |
| B15 | Other renewable |
| B16 | Solar |
| B17 | Waste |
| B18 | Wind Offshore |
| B19 | Wind Onshore |
| B20 | Other |

---

## Business Type Reference

| Code | Description |
|------|-------------|
| A01 | Production |
| A04 | Consumption |
| A14 | Aggregated energy bids |
| A37 | Installed capacity |
| A62 | Price information |
| A66 | Physical flow |
| B08 | Total nominated capacity |
| B10 | Congestion income |
| B33 | Area Control Error |

---

*This parser handles all ENTSO-E API response formats. For additional help, see the main API documentation.*

