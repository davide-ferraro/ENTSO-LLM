#### 5.3.9 Expansion and Dismantling Projects (9.1)

Returns information about planned interconnector network expansion or dismantling projects.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response Document** | `TransmissionNetwork_MarketDocument` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A90` | Interconnector network expansion |
| `out_Domain` | **[M]** | EIC Code | Bidding Zone or Control Area |
| `in_Domain` | **[M]** | EIC Code | Bidding Zone or Control Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `businessType` | [O] | Code | B01 = Network evolution; B02 = Network dismantling |
| `DocStatus` | [O] | Code | A01 = Intermediate; A02 = Final; A05 = Active; A09 = Cancelled; A13 = Withdrawn; X01 = Estimated |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A90&out_Domain=10YHU-MAVIR----U&in_Domain=10YSK-SEPS-----K&periodStart=202301010000&periodEnd=202312312300'
```

**Response Structure:**
- Returns project information with planned capacity changes
- `businessType`: `B01` (Network evolution)
- `quantity_Measure_Unit.name`: `MAW`

---
