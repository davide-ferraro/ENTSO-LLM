#### 6.3.7 Unavailability of Offshore Grid Infrastructure (10.1.C)

Returns unavailability information for offshore grid infrastructure (cables, platforms, etc.).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A79` | Offshore grid infrastructure unavailability |
| `BiddingZone_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime (optional if PeriodStartUpdate defined) |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime (optional if PeriodEndUpdate defined) |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) - mandatory if period not defined |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) - mandatory if period not defined |
| `mRID` | [O] | String | Document mRID - retrieves older versions |
| `offset` | [O] | Integer | Pagination offset [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A79&BiddingZone_Domain=10Y1001A1001A82H&periodStart=202301142300&periodEnd=202301152300'
```

**Response Structure:**
- ZIP file: `OUTAGES_A79_[START]-[END].zip`
- Includes offshore wind farm connection details
- `production_RegisteredResource.pSRType.powerSystemResources.nominalP`: Nominal power in MW
- `biddingZone_Domain.mRID`: Affected bidding zone

---
