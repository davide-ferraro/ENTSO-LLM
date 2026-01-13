#### 7.11.2 Results of Criteria Application Process - Measurements (185.4 SO GL)

Returns measurement results from criteria application process for frequency quality.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A45` | Measurement Value Document |
| `processType` | **[M]** | Code | A64 = Criteria for instantaneous frequency (SNA); A65 = Criteria for frequency restoration (LFC Block) |
| `area_domain` | **[M]** | EIC Code | SNA (for A64) or LFC Block (for A65) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A45&processType=A65&area_domain=10YCZ-CEPS-----N&periodStart=202209302200&periodEnd=202212312300'
```

---

### 7.12 Document Types Summary

| Code | Description |
|------|-------------|
| `A15` | Acquiring system operator reserve schedule |
| `A24` | Bid document |
| `A26` | Capacity document |
| `A30` | Cross border schedule |
| `A37` | Reserve bid document |
| `A38` | Allocation result document |
| `A45` | Measurement Value Document |
| `A81` | Contracted reserves |
| `A84` | Activated balancing prices |
| `A85` | Imbalance prices |
| `A86` | Imbalance volume |
| `A87` | Financial situation |
| `B17` | Aggregated netted external TSO schedule document |
| `B42` | Capacity Allocation Document |
| `B45` | Bid Availability Document |

### 7.13 Market Agreement Types

| Code | Description |
|------|-------------|
| `A01` | Daily |
| `A02` | Weekly |
| `A03` | Monthly |
| `A04` | Yearly |
| `A05` | Total |
| `A06` | Long term |
| `A07` | Intraday |
| `A13` | Hourly |

### 7.14 Flow Direction Codes

| Code | Description |
|------|-------------|
| `A01` | Up (upward regulation) |
| `A02` | Down (downward regulation) |

### 7.15 Market Product Types

| Code | Type | Description |
|------|------|-------------|
| `A01` | Standard | Standard market product |
| `A02` | Original/Specific | Specific product |
| `A03` | Integrated | Integrated process |
| `A04` | Local | Local product |
| `A05` | Standard_mFRR_SA | Standard mFRR scheduled activation |
| `A07` | Standard_mFRR_DA | Standard mFRR direct activation |

---

## Chapter 8: Master Data

The Master Data domain provides access to configuration data for production and generation units registered in the ENTSO-E Transparency Platform.

### 8.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`Configuration_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-6:configurationdocument:3:0` |
| **Unit of Measurement** | MAW (Megawatt), KVT (Kilovolt) |

### 8.2 Endpoints

---
