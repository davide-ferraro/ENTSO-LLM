#### 5.3.1 Cross-Border Physical Flows (12.1.G)

Returns aggregated physical energy flows between bidding zones or control areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Important:** Unlike the Web GUI, the API responds with **non-netted values** as data is requested per direction.

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A11` | Aggregated energy data report |
| `out_Domain` | **[M]** | EIC Code | Origin Control Area, Bidding Zone, or Country |
| `in_Domain` | **[M]** | EIC Code | Destination Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A11&out_Domain=10YDE-RWENET---I&in_Domain=10YBE----------2&periodStart=202308232200&periodEnd=202308242200'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `businessType`: `A66` (Physical flow)
- Returns time series with position/quantity pairs representing power flow in MW

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>A66</businessType>
    <in_Domain.mRID codingScheme="A01">10YBE----------2</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YDE-RWENET---I</out_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <curveType>A01</curveType>
    <Period>
        <resolution>PT15M</resolution>
        <Point>
            <position>1</position>
            <quantity>0</quantity>
        </Point>
    </Period>
</TimeSeries>
```

---
