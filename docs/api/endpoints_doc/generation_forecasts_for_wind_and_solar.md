#### 4.4.6 Generation Forecasts for Wind and Solar (14.1.D)

Returns forecasts specifically for wind and solar generation.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A69` | Wind and solar forecast |
| `processType` | **[M]** | Code | A01 = Day ahead; A18 = Current (intraday); A40 = Intraday |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | B16 = Solar; B18 = Wind Offshore; B19 = Wind Onshore |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A69&processType=A01&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `A94` (Solar forecast), `A93` (Wind forecast)
- Separate TimeSeries for each renewable type (Solar B16, Wind Offshore B18, Wind Onshore B19)

**Example - Solar Generation Forecast Pattern:**
```xml
<TimeSeries>
    <businessType>A94</businessType>
    <MktPSRType>
        <psrType>B16</psrType>
    </MktPSRType>
    <Period>
        <resolution>PT60M</resolution>
        <Point><position>1</position><quantity>0</quantity></Point>    <!-- Night -->
        <Point><position>8</position><quantity>337</quantity></Point>  <!-- Morning -->
        <Point><position>13</position><quantity>4029</quantity></Point> <!-- Peak -->
        <Point><position>20</position><quantity>586</quantity></Point> <!-- Evening -->
    </Period>
</TimeSeries>
```

---
