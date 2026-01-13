#### 7.6.2 Netted and Exchanged Volumes per Border (IFs 3.10, 3.16 & 3.17)

Returns cross-border exchange volumes between specific areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A30` | Cross border schedule |
| `processType` | **[M]** | Code | A60 = mFRR scheduled; A61 = mFRR direct; A51 = aFRR; A63 = Imbalance Netting |
| `Acquiring_Domain` | **[M]** | EIC Code | LFA or SCA |
| `Connecting_Domain` | **[M]** | EIC Code | LFA or SCA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A30&processType=A60&Acquiring_Domain=10YBE----------2&Connecting_Domain=10YFR-RTE------C&periodStart=202503010000&periodEnd=202503020000'
```

---
