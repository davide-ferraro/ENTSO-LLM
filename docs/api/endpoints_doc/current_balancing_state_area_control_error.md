#### 7.6.4 Current Balancing State / Area Control Error (12.3.A GL EB)

Returns Area Control Error (ACE) data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A86` | Imbalance volume |
| `businessType` | **[M]** | `B33` | Area Control Error |
| `area_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A86&businessType=B33&area_Domain=10YHU-MAVIR----U&periodStart=202405292200&periodEnd=202405302200'
```

**Response Structure:**
- Resolution: `PT1M` (1-minute intervals)
- Returns ACE values in MW

---

### 7.7 Endpoints - Reserve Procurement

---
