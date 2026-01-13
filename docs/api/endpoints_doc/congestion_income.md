#### 2.2.1 Congestion Income (12.1.E)

**Implicit and Flow-based Allocations - Congestion Income**

Returns congestion income data from implicit or flow-based capacity allocations.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A25` | Allocation results |
| `businessType` | **[M]** | `B10` | Congestion income |
| `contract_MarketAgreement.Type` | **[M]** | `A01` or `A07` | A01 = Daily; A07 = Intraday |
| `out_Domain` | **[M]** | EIC Code | Border or Bidding Zone (for Flow Based) |
| `in_Domain` | **[M]** | EIC Code | Same as out_Domain |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A25&businessType=B10&contract_MarketAgreement.Type=A07&out_Domain=10YDOM-CZ-D2---O&in_Domain=10YDOM-CZ-D2---O&periodStart=202308242200&periodEnd=202308252200'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- Data: `price.amount` in EUR/MWH per position

---
