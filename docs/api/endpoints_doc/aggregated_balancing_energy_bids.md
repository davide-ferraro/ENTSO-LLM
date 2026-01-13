#### 7.5.4 Aggregated Balancing Energy Bids (12.3.E GL EB)

Returns aggregated balancing energy bid data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A24` | Bid document |
| `processType` | **[M]** | Code | A51 = aFRR; A46 = RR; A47 = mFRR; A60/A61 = mFRR variants; A67/A68 = aFRR variants |
| `area_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A24&processType=A51&area_Domain=10YAT-APG------L&periodStart=202309022200&periodEnd=202309032200'
```

**Response Structure:**
- `businessType`: `A14` (Aggregated offers)
- Returns `quantity`, `secondaryQuantity`, and `unavailable_Quantity.quantity`

---
