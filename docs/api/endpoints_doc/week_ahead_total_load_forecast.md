#### 3.4.4 Week-ahead Total Load Forecast (6.1.C)

Returns week-ahead load forecast data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one week

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A31` | Week ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A31&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202308132200&periodEnd=202308202200'
```

**Response Structure:**
- Resolution: varies by TSO (typically `PT60M` or aggregated)
- Returns forecast for the week-ahead period

---
