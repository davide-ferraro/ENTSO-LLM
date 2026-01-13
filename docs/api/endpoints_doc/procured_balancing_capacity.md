#### 7.7.2 Procured Balancing Capacity (12.3.F GL EB)

Returns procured balancing capacity data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A15` | Acquiring system operator reserve schedule |
| `processType` | **[M]** | Code | A46 = RR; A47 = mFRR; A51 = aFRR; A52 = FCR |
| `area_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime (min 1 hour interval) |
| `offset` | [O] | Integer | Pagination [0-4800] |
| `Type_MarketAgreement.Type` | [O] | Code | A01 = Daily; A02 = Weekly; A03 = Monthly; A04 = Yearly; A05 = Total; A06 = Long term; A07 = Intraday; A13 = Hourly |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A15&processType=A51&area_Domain=10YDE-VE-------2&periodStart=202306150000&periodEnd=202306150100'
```

---

### 7.8 Endpoints - FCR (Frequency Containment Reserve)

---
