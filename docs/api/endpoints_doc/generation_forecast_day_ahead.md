#### 4.4.5 Generation Forecast - Day Ahead (14.1.C)

Returns day-ahead generation forecast (total scheduled generation).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Note:** `inBiddingZone_Domain` = Generation; `outBiddingZone_Domain` = Consumption

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A71` | Generation forecast |
| `processType` | **[M]** | `A01` | Day ahead |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A71&processType=A01&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `A01` (Production)
- Returns total scheduled generation for the bidding zone

---
