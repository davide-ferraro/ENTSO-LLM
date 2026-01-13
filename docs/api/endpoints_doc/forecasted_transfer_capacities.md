#### 5.3.2 Forecasted Transfer Capacities (11.1.A)

Returns estimated net transfer capacity (NTC) forecasts between areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A61` | Estimated Net Transfer Capacity |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01 = Day ahead; A02 = Week ahead; A03 = Month ahead; A04 = Year ahead |
| `out_Domain` | **[M]** | EIC Code | Origin Control Area or Bidding Zone |
| `in_Domain` | **[M]** | EIC Code | Destination Control Area or Bidding Zone |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A61&contract_MarketAgreement.Type=A01&out_Domain=10YGB----------A&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: Varies by forecast type (PT60M for day-ahead)
- Returns NTC values in MW

---
