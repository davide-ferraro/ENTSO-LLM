#### 7.4.2 Cross Border Marginal Prices (CBMPs) for aFRR Central Selection (IF aFRR 3.16)

Returns cross-border marginal prices from aFRR central selection optimization.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A84` | Activated balancing prices |
| `processType` | **[M]** | `A67` | Central Selection aFRR |
| `businessType` | **[M]** | `A96` | Automatic frequency restoration reserve |
| `Standard_MarketProduct` | **[M]** | `A01` | Standard |
| `controlArea_Domain` | **[M]** | EIC Code | LFA, SCA, or IPA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A84&processType=A67&businessType=A96&Standard_MarketProduct=A01&controlArea_Domain=10YDE-VE-------2&periodStart=202311082300&periodEnd=202311092300'
```

**Response Structure:**
- Resolution: `PT4S` (4-second intervals for aFRR)
- High-frequency price data from central optimization

---
