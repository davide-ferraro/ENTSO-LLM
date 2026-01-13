#### 3.4.5 Month-ahead Total Load Forecast (6.1.D)

Returns month-ahead load forecast data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one month

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A32` | Month ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A32&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202307022200&periodEnd=202308062200'
```

**Response Structure:**
- Resolution: varies (daily or weekly aggregation)
- Returns forecast for the month-ahead period

---
