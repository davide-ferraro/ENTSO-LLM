#### 7.4.1 Prices of Activated Balancing Energy (17.1.F)

Returns prices for activated balancing energy.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A84` | Activated balancing prices |
| `processType` | **[M]** | Code | A16 = Realised; A60 = Scheduled mFRR; A61 = Direct mFRR; A68 = Local Selection aFRR |
| `controlArea_Domain` | **[M]** | EIC Code | LFA, IPA, or SCA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `businessType` | [O] | Code | A95 = FCR; A96 = aFRR; A97 = mFRR; A98 = RR |
| `PsrType` | [O] | Code | A04 = Generation; A05 = Load |
| `Standard_MarketProduct` | [O] | `A01` | Standard product |
| `Original_MarketProduct` | [O] | Code | A02 = Specific; A04 = Local |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A84&processType=A16&controlArea_Domain=10YBE----------2&periodStart=202309032200&periodEnd=202309042200&businessType=A96'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- Returns `activation_Price.amount` in EUR/MWh
- `imbalance_Price.category`: Price direction indicator
- `flowDirection.direction`: A01 = Up; A02 = Down

---
