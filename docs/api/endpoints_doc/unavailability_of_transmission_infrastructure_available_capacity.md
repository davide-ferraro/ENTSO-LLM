#### 6.3.5 Unavailability of Transmission Infrastructure - Available Capacity (10.1.A&B)

Alternative query for transmission unavailability filtered by control area (returns outages affecting a specific area).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A78` | Transmission unavailability |
| `ControlArea_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |
| `Asset_RegisteredResource.mRID` | [O] | EIC Code | Specific Transmission Asset EIC |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `mRID` | [O] | String | Document mRID - retrieves older versions |
| `offset` | [O] | Integer | Pagination offset [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A78&ControlArea_Domain=10YFR-RTE------C&periodStart=202312012300&periodEnd=202312022300'
```

---
