#### 3.4.6 Year-ahead Total Load Forecast (6.1.E)

Returns year-ahead load forecast data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one year

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A33` | Year ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A33&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202301012300&periodEnd=202312312300'
```

**Response Structure:**
- Resolution: `P7D` (weekly points)
- `businessType`: `A60` (Forecast)
- Returns weekly forecast values for the entire year

---
