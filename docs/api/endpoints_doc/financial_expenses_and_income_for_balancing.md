#### 7.11.1 Financial Expenses and Income for Balancing (17.1.I)

Returns financial data related to balancing operations.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A87` | Financial situation |
| `controlArea_Domain` | **[M]** | EIC Code | Control Area or Market Balance Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A87&controlArea_Domain=10YHU-MAVIR----U&periodStart=202301312300&periodEnd=202302282300'
```

---
