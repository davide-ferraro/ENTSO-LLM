#### 6.3.1 Unavailability of Production Units (15.1.C-D)

Returns unavailability information for production units (aggregated by bidding zone).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A77` | Production unit unavailability |
| `BiddingZone_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID is present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability (unplanned) |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `RegisteredResource` | [O] | EIC Code | Specific Production Unit EIC |
| `mRID` | [O] | String | Document mRID - returns older versions when specified |
| `offset` | [O] | Integer | Pagination offset [0-4800], returns records n+1 to n+100 |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A77&BiddingZone_Domain=10YBE----------2&periodStart=202212312300&periodEnd=202301312300'
```

**Response Structure:**
- Each outage is a separate XML document in the ZIP file
- `process.processType`: `A26` (System operator data)
- `revisionNumber`: Version of the outage document
- Includes `TimeSeries` with availability periods

---
