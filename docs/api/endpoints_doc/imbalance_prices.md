#### 7.4.3 Imbalance Prices (17.1.G)

Returns imbalance settlement prices.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A85` | Imbalance prices |
| `controlArea_Domain` | **[M]** | EIC Code | Scheduling Area or Market Balance Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | A04 = Generation; A05 = Load |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A85&controlArea_Domain=10YNL----------L&periodStart=202310312300&periodEnd=202311012300'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `imbalance_Price.amount`: Price in EUR/MWh
- `imbalance_Price.category`: A04 = generation direction; A05 = consumption direction
- `businessType`: `A19` (Balance Energy Deviation)

---

### 7.5 Endpoints - Balancing Energy Bids

---
