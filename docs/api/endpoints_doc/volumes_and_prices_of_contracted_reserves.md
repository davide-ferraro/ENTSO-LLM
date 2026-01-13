#### 7.7.1 Volumes and Prices of Contracted Reserves (17.1.B&C)

Returns contracted reserve volumes and prices.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A81` | Contracted reserves |
| `businessType` | **[M]** | `B95` | Procured capacity |
| `Type_MarketAgreement.Type` | **[M]** | Code | A01 = Daily; A02 = Weekly; A03 = Monthly; A04 = Yearly; A06 = Long term; A13 = Hourly |
| `controlArea_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `processType` | [O] | Code | A51 = aFRR; A52 = FCR; A47 = mFRR; A46 = RR |
| `psrType` | [O] | Code | A03 = Mixed; A04 = Generation; A05 = Load |
| `offset` | [O] | Integer | Pagination [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A81&businessType=B95&processType=A52&Type_MarketAgreement.Type=A01&controlArea_Domain=10YCZ-CEPS-----N&periodStart=202309242200&periodEnd=202309252200'
```

---
