#### 2.2.7 Explicit Allocations - Use of Transfer Capacity (12.1.A)

Returns the actual use of allocated transfer capacity including prices.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A25` | Allocation result document |
| `businessType` | **[M]** | `B05` or `A43` | B05=Capacity allocated (with price), A43=Requested capacity (without price) |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Day ahead, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `Auction.Category` | [O] | Code | A01=Base, A02=Peak, A03=Off Peak, A04=Hourly |
| `ClassificationSequence_AttributeInstanceComponent.Position` | [O] | Integer | Position filter |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A25&businessType=B05&contract_MarketAgreement.Type=A07&out_Domain=10YGB----------A&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

---
