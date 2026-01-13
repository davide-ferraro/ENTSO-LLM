#### 5.3.4 Commercial Schedules - Net Positions (12.1.F)

Returns net position data for a specific bidding zone (import/export balance).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Key Difference:** Set `in_Domain` = `out_Domain` (same EIC code) to get net positions.

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A09` | Finalised schedule |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `in_Domain` | **[M]** | EIC Code | **Same as out_Domain** |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `contract_MarketAgreement.Type` | [O] | Code | A01 = Day Ahead; A05 = Total |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A09&out_Domain=10YAT-APG------L&in_Domain=10YAT-APG------L&periodStart=202506102200&periodEnd=202506112200'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `businessType`: `B09` (Net position)
- Multiple TimeSeries showing exchanges with neighboring zones
- Positive values = export, Negative values = import

---
