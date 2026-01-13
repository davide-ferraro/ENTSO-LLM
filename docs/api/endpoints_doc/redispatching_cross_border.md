#### 5.3.8 Redispatching - Cross Border (13.1.A)

Returns cross-border redispatching data between control areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response Document** | `TransmissionNetwork_MarketDocument` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A63` | Redispatch notice |
| `businessType` | **[M]** | `A46` | System Operator re-dispatching |
| `out_Domain` | **[M]** | EIC Code | Origin Control Area |
| `in_Domain` | **[M]** | EIC Code | Destination Control Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A63&businessType=A46&out_Domain=10YAT-APG------L&in_Domain=10YFR-RTE------C&periodStart=202311010000&periodEnd=202312010000'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `quantity_Measure_Unit.name`: `MWH`
- `flowDirection.direction`: `A02` (Down regulation)
- `mktPSRType.psrType`: Production type affected (e.g., A05 = Coal)

---
