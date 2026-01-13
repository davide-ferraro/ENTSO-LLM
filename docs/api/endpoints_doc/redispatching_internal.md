#### 5.3.7 Redispatching - Internal (13.1.A)

Returns internal redispatching data within a control area.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response Document** | `TransmissionNetwork_MarketDocument` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A63` | Redispatch notice |
| `businessType` | **[M]** | `A85` | Internal requirements |
| `out_Domain` | **[M]** | EIC Code | Control Area |
| `in_Domain` | **[M]** | EIC Code | Control Area (**must be same as out_Domain**) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A63&businessType=A85&out_Domain=10YNL----------L&in_Domain=10YNL----------L&periodStart=202310312300&periodEnd=202311302300'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `quantity_Measure_Unit.name`: `MWH`
- `flowDirection.direction`: `A02` (Down regulation)
- Includes `Asset_RegisteredResource` with:
  - `mRID` - Asset EIC code
  - `pSRType.psrType` - Production type (e.g., B21 = Wind onshore)
  - `location.name` - Physical location name

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>A85</businessType>
    <in_Domain.mRID codingScheme="A01">10YNL----------L</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YNL----------L</out_Domain.mRID>
    <quantity_Measure_Unit.name>MWH</quantity_Measure_Unit.name>
    <mktPSRType.psrType>A04</mktPSRType.psrType>
    <curveType>A01</curveType>
    <flowDirection.direction>A02</flowDirection.direction>
    <Asset_RegisteredResource>
        <mRID codingScheme="A01">49T000000000436O</mRID>
        <pSRType.psrType>B21</pSRType.psrType>
        <location.name>Hardenberg - Ommen Dante wit 110 kV</location.name>
    </Asset_RegisteredResource>
    <Period>
        <resolution>PT15M</resolution>
        <Point>
            <position>1</position>
            <quantity>6</quantity>
        </Point>
    </Period>
</TimeSeries>
```

---
