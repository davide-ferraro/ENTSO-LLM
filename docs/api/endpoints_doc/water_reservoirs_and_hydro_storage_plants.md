#### 4.4.2 Water Reservoirs and Hydro Storage Plants (16.1.D)

Returns reservoir filling information for hydro storage plants.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A72` | Reservoir filling information |
| `processType` | **[M]** | `A16` | Realised |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A72&processType=A16&in_Domain=10YCA-BULGARIA-R&periodStart=202307092100&periodEnd=202307162100'
```

**Response Structure:**
- Resolution: typically `P7D` (weekly)
- Returns energy storage levels in MWh or percentage

---
