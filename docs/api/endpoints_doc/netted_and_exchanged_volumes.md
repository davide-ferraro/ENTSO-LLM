#### 7.6.1 Netted and Exchanged Volumes (IFs 3.10, 3.16 & 3.17)

Returns netted and exchanged volumes for imbalance netting and balancing energy exchange.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `B17` | Aggregated netted external TSO schedule document |
| `processType` | **[M]** | Code | A60 = mFRR scheduled; A61 = mFRR direct; A51 = aFRR; A63 = Imbalance Netting |
| `Acquiring_Domain` | **[M]** | EIC Code | LFA or SCA |
| `Connecting_Domain` | **[M]** | EIC Code | LFA or SCA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=B17&processType=A63&Acquiring_Domain=10YDE-VE-------2&Connecting_Domain=10YDE-VE-------2&periodStart=202301012300&periodEnd=202301022300'
```

**Response Structure:**
- Resolution: `PT15M`
- `businessType`: `B09` (Net position)
- Returns volumes in MWh

---
