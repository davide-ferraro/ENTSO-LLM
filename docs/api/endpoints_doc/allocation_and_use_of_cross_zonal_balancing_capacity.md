#### 7.10.1 Allocation and Use of Cross-Zonal Balancing Capacity (12.3.H&I)

Returns cross-zonal balancing capacity allocation data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A38` | Allocation result document |
| `processType` | **[M]** | Code | A51 = aFRR; A47 = mFRR; A46 = RR |
| `Acquiring_Domain` | **[M]** | EIC Code | Scheduling Area |
| `Connecting_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---
