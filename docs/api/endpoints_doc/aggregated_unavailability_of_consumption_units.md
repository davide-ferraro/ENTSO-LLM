#### 6.3.3 Aggregated Unavailability of Consumption Units (7.1.A-B)

Returns aggregated unavailability information for consumption units.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A76` | Load unavailability |
| `BiddingZone_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID is present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime (optional if PeriodStartUpdate defined) |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime (optional if PeriodEndUpdate defined) |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A76&BiddingZone_Domain=10Y1001A1001A82H&periodStart=202310312300&periodEnd=202311302300'
```

**Response Structure:**
- `process.processType`: `A26`
- `unavailability_Time_Period.timeInterval`: Overall outage period
- TimeSeries includes unavailable load in MW

---
