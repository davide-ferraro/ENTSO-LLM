#### 2.2.4 Transfer Capacities with Third Countries (12.1.H)

Returns transfer capacities allocated with non-EU countries (explicit allocations).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A94` | Non EU allocations |
| `auction.Type` | **[M]** | `A02` | Explicit |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Daily, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `auction.Category` | [O] | Code | A01=Base, A02=Peak, A03=Off Peak, A04=Hourly |
| `classificationSequence_AttributeInstanceComponent.Position` | [O] | Integer | Position filter |

**Example Request (Finland to Russia):**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A94&auction.Type=A02&contract_MarketAgreement.Type=A07&out_Domain=10YFI-1--------U&in_Domain=10Y1001A1001A49F&periodStart=202308232200&periodEnd=202308242200'
```

---
