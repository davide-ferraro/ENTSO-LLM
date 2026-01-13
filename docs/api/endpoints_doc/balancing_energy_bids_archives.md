#### 7.5.2 Balancing Energy Bids Archives (12.3.B&C)

Returns archived balancing energy bids (older than 93 days).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | Nested ZIP files |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A37` | Reserve bid document |
| `businessType` | **[M]** | `B74` | Offer |
| `processType` | **[M]** | Code | A46 = RR; A47 = mFRR; A51 = aFRR |
| `connecting_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Must be outside 93-day retention |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | Must be outside 93-day retention |
| `storageType` | **[M]** | `archive` | Request archived data |
| `offset` | [O] | Integer | Pagination [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A37&businessType=B74&processType=A47&connecting_Domain=10YBE----------2&periodStart=202310072200&periodEnd=202310082200&storageType=archive'
```

---
