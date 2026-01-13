#### 7.5.3 Changes to Bid Availability (IFs mFRR 9.9, aFRR 9.6&9.8)

Returns bid availability change documents.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `B45` | Bid Availability Document |
| `processType` | **[M]** | `A47` | mFRR |
| `Domain` | **[M]** | EIC Code | Scheduling Area or LFA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `businessType` | [O] | Code | C40-C46 (see below) |
| `offset` | [O] | Integer | Pagination [0-4800] |

**Business Types for Bid Availability:**
- `C40` = Conditional bid
- `C41` = Thermal limit
- `C42` = Frequency limit
- `C43` = Voltage limit
- `C44` = Current limit
- `C45` = Short-circuit current limits
- `C46` = Dynamic stability limit

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=B45&processType=A47&Domain=10YDE-VE-------2&periodStart=202309232200&periodEnd=202309242200'
```

---
