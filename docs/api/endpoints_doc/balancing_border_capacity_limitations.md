#### 7.10.2 Balancing Border Capacity Limitations (IFs 4.3 & 4.4)

Returns capacity limitations on balancing borders.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `B42` | Capacity Allocation Document |
| `Acquiring_Domain` | **[M]** | EIC Code | LFA/SCA |
| `Connecting_Domain` | **[M]** | EIC Code | LFA/SCA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

### 7.11 Endpoints - Financial & System Operation

---
