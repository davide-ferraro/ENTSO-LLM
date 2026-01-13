#### 6.3.6 Unavailability of Transmission Infrastructure - Net Position Impact (10.1.A&B)

Query for transmission outages that impact the net position of a specific area (PTDF-based query).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A78` | Transmission unavailability |
| `pTDF_Domain.mRID` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `Asset_RegisteredResource.mRID` | [O] | EIC Code | Transmission Asset EIC |
| `mRID` | [O] | String | Document mRID |
| `offset` | [O] | Integer | Pagination offset [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A78&pTDF_Domain.mRID=10YBE----------2&periodStart=202312012300&periodEnd=202312022300'
```

---
