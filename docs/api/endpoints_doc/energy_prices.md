#### 2.2.12 Energy Prices (12.1.D)

Returns day-ahead and intraday energy prices for a bidding zone.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Maximum 100 documents per response (use offset for pagination)

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A44` | Price Document |
| `out_Domain` | **[M]** | EIC Code | Bidding Zone |
| `in_Domain` | **[M]** | EIC Code | Bidding Zone (must be same as out_Domain) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `contract_MarketAgreement.type` | [O] | Code | A01=Day-ahead, A07=Intraday |
| `classificationSequence_AttributeInstanceComponent.position` | [O] | Integer | Position filter |
| `offset` | [O] | Integer [0-4800] | Pagination offset |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A44&out_Domain=10YAT-APG------L&in_Domain=10YAT-APG------L&periodStart=202407272200&periodEnd=202407282200'
```

**Response Structure:**
- Resolution: `PT15M` or `PT60M` depending on market
- Data: `price.amount` in EUR/MWH
- Currency: EUR
- Includes `auction.type` (A01=Day-ahead auction)

---

### 2.3 Contract/Market Agreement Types Reference

| Code | Description | Typical Use |
|------|-------------|-------------|
| `A01` | Day-ahead | Day-ahead auctions and allocations |
| `A02` | Weekly | Long-term weekly products |
| `A03` | Monthly | Long-term monthly products |
| `A04` | Yearly | Long-term yearly products |
| `A05` | Total | Aggregated/total values |
| `A06` | Long Term | Other long-term products |
| `A07` | Intraday | Intraday continuous/auctions |
| `A08` | Quarterly | Quarterly products |

### 2.4 Auction Types Reference

| Code | Description |
|------|-------------|
| `A01` | Implicit (market coupling) |
| `A02` | Explicit (capacity auctions) |
| `A08` | Continuous (intraday) |

### 2.5 Business Types Reference (Market Domain)

| Code | Description |
|------|-------------|
| `A29` | Already allocated capacity |
| `A31` | Offered capacity |
| `A34` | Allocated capacity (third countries) |
| `A43` | Requested capacity (without price) |
| `B05` | Capacity allocated (with price) |
| `B07` | Auction revenue |
| `B08` | Total nominated capacity |
| `B09` | Net position |
| `B10` | Congestion income |

---

## Chapter 3: Load

The Load domain provides access to electricity consumption data including actual load measurements and load forecasts at various time horizons (day-ahead, week-ahead, month-ahead, year-ahead).

### 3.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`GL_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0` |
| **Unit of Measurement** | MAW (Megawatt) |

### 3.2 Common Parameters for Load Endpoints

All Load endpoints share these common parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `documentType` | **[M]** | `A65` (System total load) or `A70` (Load forecast margin) |
| `processType` | **[M]** | Specifies the time horizon (see table below) |
| `outBiddingZone_Domain` | **[M]** | EIC code of Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | Start datetime (`yyyyMMddHHmm`) |
| `periodEnd` | **[M]** | End datetime (`yyyyMMddHHmm`) |

### 3.3 Process Types for Load Data

| Code | Description | Minimum Response Interval |
|------|-------------|---------------------------|
| `A16` | Realised (Actual) | One MTU period |
| `A01` | Day ahead | One day |
| `A31` | Week ahead | One week |
| `A32` | Month ahead | One month |
| `A33` | Year ahead | One year |

### 3.4 Endpoints

---
