#### 2.2.6 Explicit Allocations - Offered Transfer Capacity (11.1.A)

Returns offered transfer capacity for explicit auctions.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A31` | Agreed capacity |
| `auction.Type` | **[M]** | `A02` | Explicit |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Day ahead, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `auction.Category` | [O] | Code | A01=Base, A02=Peak, A03=Off Peak, A04=Hourly |
| `Update_DateAndOrTime` | [O] | Numeric datetime | For capacity evolution queries |
| `ClassificationSequence_AttributeInstanceComponent.Position` | [O] | Integer | Position filter |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A31&auction.Type=A02&contract_MarketAgreement.Type=A01&out_Domain=10YGB----------A&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

---
