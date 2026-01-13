#### 7.9.2 FRR and RR Actual Capacity (188.4 & 189.3 SO GL)

Returns actual FRR and RR capacity data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | Code | A96 = aFRR; A97 = mFRR; A98 = RR |
| `processType` | **[M]** | `A16` | Realised |
| `area_Domain` | **[M]** | EIC Code | LFC Block |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

### 7.10 Endpoints - Cross-Border & Capacity Allocation

---
