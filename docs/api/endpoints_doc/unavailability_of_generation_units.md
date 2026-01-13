#### 6.3.2 Unavailability of Generation Units (15.1.A&B)

Returns unavailability information for individual generation units.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |
| **Max Results** | 200 documents per request |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A80` | Generation unavailability |
| `BiddingZone_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID is present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `RegisteredResource` | [O] | EIC Code | Specific Generation Unit EIC |
| `mRID` | [O] | String | Document mRID - retrieves older versions |
| `offset` | [O] | Integer | Pagination offset [0-4800], returns records n+1 to n+200 |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A80&BiddingZone_Domain=10YBE----------2&periodStart=202301022200&periodEnd=202301032200'
```

**Response Structure:**
- ZIP file: `OUTAGES_A80_[START]-[END].zip`
- Contains individual XML files for each generation unit outage
- Includes unit details, outage periods, and available capacity

---
