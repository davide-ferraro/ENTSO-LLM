#### 5.3.5 Cross Border Capacity of DC Links - Intraday Transfer Limits (11.3)

Returns capacity information for DC interconnector links for intraday trading.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A93` | DC link capacity |
| `out_Domain` | **[M]** | EIC Code | Bidding Zone, Control Area, or Country |
| `in_Domain` | **[M]** | EIC Code | Bidding Zone, Control Area, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A93&out_Domain=11Y0-0000-0265-K&in_Domain=10YFR-RTE------C&periodStart=202308160000&periodEnd=202308162200'
```

**Response Structure:**
- Returns DC link transfer limits in MW
- Used for interconnectors like ElecLink (GB-FR), BritNed, NorNed, etc.

---
