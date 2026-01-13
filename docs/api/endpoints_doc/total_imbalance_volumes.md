#### 7.6.3 Total Imbalance Volumes (17.1.H)

Returns total system imbalance volumes.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A86` | Imbalance volume |
| `controlArea_Domain` | **[M]** | EIC Code | Scheduling Area or Market Balance Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `businessType` | [O] | `A19` | Balance Energy Deviation (default) |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A86&controlArea_Domain=10YAT-APG------L&periodStart=202311032300&periodEnd=202311042300'
```

---
