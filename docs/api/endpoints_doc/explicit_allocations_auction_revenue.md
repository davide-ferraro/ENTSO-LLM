#### 2.2.8 Explicit Allocations - Auction Revenue (12.1.A)

Returns auction revenue from explicit capacity allocations.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A25` | Allocation result document |
| `businessType` | **[M]** | `B07` | Auction revenue |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Daily, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A25&businessType=B07&contract_MarketAgreement.Type=A01&out_Domain=10YHR-HEP------M&in_Domain=10YBA-JPCC-----D&periodStart=202308242200&periodEnd=202308252200'
```

---
