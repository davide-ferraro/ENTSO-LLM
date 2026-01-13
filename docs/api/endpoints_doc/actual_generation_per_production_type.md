#### 4.4.3 Actual Generation per Production Type (16.1.B&C)

Returns actual electricity generation aggregated by production type.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Important Notes:**
- Response is the same whether using `A74` (Wind & Solar only) or `A75` (All production types)
- `inBiddingZone_Domain` = Generation values
- `outBiddingZone_Domain` = Consumption values

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A75` or `A74` | A75 = All types; A74 = Wind and solar only |
| `processType` | **[M]** | `A16` | Realised |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `psrType` | [O] | Code | Production type (B01-B25). If omitted, returns all types |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A75&processType=A16&in_Domain=10Y1001A1001A83F&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: `PT15M` or `PT60M` (depends on country)
- `businessType`: `A01` (Production)
- One TimeSeries per production type
- `objectAggregation`: `A08` (Resource type)

---
