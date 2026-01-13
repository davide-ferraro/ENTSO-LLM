#### 2.2.10 Flow Based Allocations (11.1.B)

Returns flow-based domain publication data including Critical Network Elements (CNEs) and PTDFs.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file containing XML |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `B09` | Flow Based Domain Publication |
| `processType` | **[M]** | Code | A43=Day ahead, A44=Intraday, A32=Month-ahead, A33=Year-ahead |
| `out_Domain` | **[M]** | EIC Code | Region code |
| `in_Domain` | **[M]** | EIC Code | Region code (same as out_Domain) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=B09&processType=A33&out_Domain=10Y1001A1001A91G&in_Domain=10Y1001A1001A91G&periodStart=202412312300&periodEnd=202512312300'
```

**Response Structure:**
- Document type: `CriticalNetworkElement_MarketDocument`
- Contains: Constraint_Series with PTDFs, contingencies, and measurements

---
