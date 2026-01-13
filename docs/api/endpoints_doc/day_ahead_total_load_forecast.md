#### 3.4.3 Day-ahead Total Load Forecast (6.1.B)

Returns day-ahead load forecast data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one day

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A01` | Day ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A01&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202308140000&periodEnd=202308170000'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `A04` (Base load)
- Returns one TimeSeries per day in the requested period

---
