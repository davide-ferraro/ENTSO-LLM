#### 7.5.5 Elastic Demands (IFs aFRR 3.4 & mFRR 3.4)

Returns elastic demand data for balancing markets.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A37` | Reserve bid document |
| `businessType` | **[M]** | `B75` | Need |
| `processType` | **[M]** | Code | A51 = aFRR; A47 = mFRR |
| `Acquiring_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `offset` | [O] | Integer | Pagination [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A37&businessType=B75&processType=A47&Acquiring_Domain=10YCZ-CEPS-----N&periodStart=202311302300&periodEnd=202312012300'
```

---

### 7.6 Endpoints - Volumes

---
