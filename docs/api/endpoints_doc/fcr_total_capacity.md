#### 7.8.1 FCR Total Capacity (187.2 SO GL)

Returns total FCR capacity for a synchronous area.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | `A25` | General Capacity Information |
| `area_Domain` | **[M]** | EIC Code | Synchronous Area (e.g., 10YEU-CONT-SYNC0) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A26&businessType=A25&area_Domain=10YEU-CONT-SYNC0&periodStart=202312312300&periodEnd=202412312300'
```

---
