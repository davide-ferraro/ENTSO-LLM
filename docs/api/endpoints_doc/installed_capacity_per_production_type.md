#### 4.4.1 Installed Capacity per Production Type (14.1.A)

Returns the installed generation capacity aggregated by production type (year-ahead).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A68` | Installed generation per type |
| `processType` | **[M]** | `A33` | Year ahead |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | Production type (B01-B25). If omitted, returns all types |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A68&processType=A33&in_Domain=10YBE----------2&periodStart=202212312300&periodEnd=202312312300'
```

**Response Structure:**
- Resolution: `P1Y` (yearly)
- `businessType`: `A37` (Installed capacity)
- One TimeSeries per production type with `MktPSRType/psrType` indicating the type
- `objectAggregation`: `A08` (Resource type)

**Example Response Data:**
```xml
<TimeSeries>
    <businessType>A37</businessType>
    <MktPSRType>
        <psrType>B04</psrType>  <!-- Fossil Gas -->
    </MktPSRType>
    <Period>
        <resolution>P1Y</resolution>
        <Point>
            <position>1</position>
            <quantity>6915</quantity>  <!-- MW installed -->
        </Point>
    </Period>
</TimeSeries>
```

---
