#### 2.2.11 Continuous Allocations - Offered Transfer Capacity (11.1)

Returns offered transfer capacity for continuous intraday markets.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `DocumentType` | **[M]** | `A31` or `B33` | A31=Agreed capacity (intermediate), B33=Published offered capacity (most recent) |
| `Auction.Type` | **[M]** | `A08` | Continuous |
| `Out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `In_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `PeriodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `PeriodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `Contract_MarketAgreement.Type` | **[M]** | `A07` | Intraday |
| `Update_DateAndOrTime` | [O] | Numeric datetime | For capacity evolution. If omitted, returns most recent published version |
| `offset` | [O] | Integer [0-4800] | Pagination offset |

**Note on Document Types:**
- `A31`: Intermediate OC (Offered Capacity) values
- `B33`: Most recent published OC values

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&DocumentType=A31&Auction.Type=A08&Out_Domain=10YBE----------2&In_Domain=10YNL----------L&PeriodStart=202405152200&PeriodEnd=202405162200&Contract_MarketAgreement.Type=A07'
```

**Response Structure:**
- Resolution: `PT15M`
- Includes `update_DateAndOrTime.dateTime` showing when the capacity was published

---
