#### 2.2.2 Total Nominated Capacity (12.1.B)

Returns the total nominated capacity between two areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | `B08` | Total nominated capacity |
| `out_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone |
| `in_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A26&businessType=B08&out_Domain=10YGB----------A&in_Domain=10YBE----------2&periodStart=202308202200&periodEnd=202308212200'
```

**Response Structure:**
- Resolution: `PT60M` (hourly intervals)
- Data: `quantity` in MAW (Megawatt) per position
- Multiple TimeSeries for different contract types (A01=Day-ahead, A07=Intraday, A06=Long-term)

---
