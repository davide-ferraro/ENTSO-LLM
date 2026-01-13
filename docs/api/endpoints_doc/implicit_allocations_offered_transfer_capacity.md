#### 2.2.3 Implicit Allocations - Offered Transfer Capacity (11.1)

Returns offered transfer capacity for implicit allocations.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A31` | Agreed capacity |
| `auction.Type` | **[M]** | `A01` | Implicit |
| `contract_MarketAgreement.Type` | **[M]** | `A01` or `A07` | A01 = Day ahead; A07 = Intraday |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `Update_DateAndOrTime` | [O] | Numeric datetime | For capacity evolution queries (e.g., `20230313123900`) |
| `ClassificationSequence_AttributeInstanceComponent.Position` | [O] | Integer | Position filter |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A31&auction.Type=A01&contract_MarketAgreement.Type=A01&out_Domain=10YDK-1--------W&in_Domain=10Y1001A1001A82H&periodStart=202212312300&periodEnd=202301012300'
```

**Response Structure:**
- Resolution: `PT60M`
- Data: `quantity` in MAW
- Includes `auction.mRID` identifying the specific auction

---
