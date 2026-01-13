#### 2.2.5 Total Capacity Already Allocated (12.1.C)

Returns capacity that has already been allocated on a border.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity Document |
| `businessType` | **[M]** | `A29` | Already Allocated Capacity |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Daily, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `auction.Category` | [O] | Code | A01=Base, A02=Peak, A03=Off Peak, A04=Hourly |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A26&businessType=A29&contract_MarketAgreement.Type=A01&out_Domain=10YHR-HEP------M&in_Domain=10YBA-JPCC-----D&periodStart=202308242200&periodEnd=202308252200'
```

---
