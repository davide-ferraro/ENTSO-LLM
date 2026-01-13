#### 7.8.3 Sharing of FCR between Synchronous Areas (190.2 SO GL)

Returns FCR exchange data between synchronous areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | `A95` | Frequency Containment Reserve |
| `Acquiring_Domain` | **[M]** | EIC Code | Synchronous Area |
| `Connecting_Domain` | **[M]** | EIC Code | Synchronous Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

### 7.9 Endpoints - FRR/RR Capacity

---
