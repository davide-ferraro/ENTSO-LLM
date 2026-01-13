#### 7.5.1 Balancing Energy Bids (12.3.B&C)

Returns individual balancing energy bids (within 93-day retention period).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |
| **Data Retention** | 93 days |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A37` | Reserve bid document |
| `businessType` | **[M]** | `B74` | Offer |
| `processType` | **[M]** | Code | A46 = RR; A47 = mFRR; A51 = aFRR |
| `connecting_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Must be within 93-day retention |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | Must be within 93-day retention |
| `offset` | [O] | Integer | Pagination [0-4800], returns n+1 to n+100 |
| `Standard_MarketProduct` | [O] | Code | A01 = Standard; A05 = mFRR scheduled; A07 = mFRR direct |
| `Original_MarketProduct` | [O] | Code | A02 = Specific; A03 = Integrated; A04 = Local |
| `Direction` | [O] | Code | A01 = Up; A02 = Down |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A37&businessType=B74&processType=A47&connecting_Domain=10YCZ-CEPS-----N&periodStart=202410012200&periodEnd=202410022200'
```

---
