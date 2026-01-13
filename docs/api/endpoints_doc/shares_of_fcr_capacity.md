#### 7.8.2 Shares of FCR Capacity (187.2 SO GL)

Returns FCR capacity shares per LFC block.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | `B32` | FCR sharing |
| `area_Domain` | **[M]** | EIC Code | LFC Block |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---
