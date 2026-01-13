#### 2.2.9 Implicit Auction - Net Positions (12.1.E)

Returns net positions from implicit auctions for a bidding zone.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A25` | Allocation results |
| `businessType` | **[M]** | `B09` | Net position |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Daily, A05=Total, A07=Intraday |
| `out_Domain` | **[M]** | EIC Code | Bidding Zone or Control Area |
| `in_Domain` | **[M]** | EIC Code | **Must be same as out_Domain** |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A25&businessType=B09&contract_MarketAgreement.Type=A07&out_Domain=10YBE----------2&in_Domain=10YBE----------2&periodStart=202308222200&periodEnd=202308232200'
```

**Response Structure:**
- Resolution: `PT15M`
- Data: `quantity` in MAW (positive = export, negative = import)

---
