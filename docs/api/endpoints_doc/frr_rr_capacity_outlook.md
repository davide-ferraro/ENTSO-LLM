#### 7.9.1 FRR & RR Capacity Outlook (188.3 & 189.2 SO GL)

Returns year-ahead FRR and RR capacity outlook.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | Code | A96 = aFRR; A97 = mFRR; A98 = RR |
| `processType` | **[M]** | `A33` | Year ahead |
| `area_Domain` | **[M]** | EIC Code | LFC Block |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---
