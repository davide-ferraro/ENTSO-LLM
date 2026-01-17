# ENTSO-E Transparency Platform REST API Documentation

> **Purpose**: This document provides a structured, LLM-readable reference for the ENTSO-E Transparency Platform REST API. It enables programmatic access to European electricity market data including load, generation, transmission, outages, balancing, and market information.

---

## Table of Contents

1. [Chapter 1: General Introduction](#chapter-1-general-introduction)
2. [Chapter 2: Market](#chapter-2-market)
3. [Chapter 3: Load](#chapter-3-load)
4. [Chapter 4: Generation](#chapter-4-generation)
5. [Chapter 5: Transmission](#chapter-5-transmission)
6. [Chapter 6: Outages](#chapter-6-outages)
7. [Chapter 7: Balancing](#chapter-7-balancing)
8. [Chapter 8: Master Data](#chapter-8-master-data)
9. [Chapter 9: OMI (Other Market Information)](#chapter-9-omi-other-market-information)

---

## Chapter 1: General Introduction

### 1.1 Overview

The **ENTSO-E Transparency Platform REST API** provides programmatic access to European electricity market data. This API is maintained by ENTSO-E (European Network of Transmission System Operators for Electricity).

- **Base URL**: `https://web-api.tp.entsoe.eu/api`
- **Protocol**: HTTPS (REST)
- **Response Format**: XML (IEC 62325 standard)
- **Documentation Source**: [Postman Collection](https://documenter.getpostman.com/view/7009892/2s93JtP3F6)

### 1.2 Authentication

| Property | Value |
|----------|-------|
| **Type** | API Key |
| **Key Name** | `securityToken` |
| **Location** | Query Parameter |

To obtain an API key:
1. Register at the ENTSO-E Transparency Platform
2. Request API access through your account settings
3. Include the `securityToken` parameter in all API requests

**Example**:
```
https://web-api.tp.entsoe.eu/api?securityToken=YOUR_API_KEY&documentType=A65&...
```

### 1.3 Common Request Parameters

| Parameter | Format | Required | Description |
|-----------|--------|----------|-------------|
| `securityToken` | String | **Yes** | Your API authentication key |
| `documentType` | Code (e.g., A65) | **Yes** | Specifies the type of data requested |
| `periodStart` | `yyyyMMddHHmm` | **Yes** | Start of the query period (UTC) |
| `periodEnd` | `yyyyMMddHHmm` | **Yes** | End of the query period (UTC) |
| `in_Domain` | EIC Code | Depends | Area/zone receiving (import side) |
| `out_Domain` | EIC Code | Depends | Area/zone sending (export side) |
| `businessType` | Code (e.g., B10) | Depends | Type of business process |
| `psrType` | Code (e.g., B16) | Optional | Production/consumption type |
| `offset` | Integer [0-4800] | Optional | Pagination offset (max 4900 docs) |

### 1.4 Date/Time Format

- **Pattern**: `yyyyMMddHHmm`
- **Timezone**: UTC
- **Example**: `202308232200` = August 23, 2023, 22:00 UTC

### 1.4.1 ⚠️ Time Range Limitations

**Important:** The API has maximum time range limits for requests:

| Data Type | Maximum Time Range | Notes |
|-----------|-------------------|-------|
| Most operational data | **~1 year** | Requests spanning > 1 year will fail |
| Minute-resolution data (ACE) | **~1 day** | Very granular data has shorter limits |
| High-volume data (bids) | **~1 day to 1 week** | May fail due to result size limits |
| Installed capacity | **1 year** | Returns yearly aggregates |

**Common Error for Long Time Ranges:**
```xml
<Reason>
  <code>999</code>
  <text>The requested time period is too long</text>
</Reason>
```

**Best Practices:**
1. For multi-year data, make **separate requests per year** and combine results
2. For large datasets, use **pagination** (`offset` parameter) if available
3. Start with **shorter time ranges** (1 day to 1 week) and expand as needed
4. Monitor response size - very large responses may timeout

### 1.5 EIC Codes (Energy Identification Codes)

EIC codes uniquely identify market participants, areas, and resources. Examples:

| EIC Code | Description |
|----------|-------------|
| `10YAT-APG------L` | Austria (APG control area) |
| `10YDE-VE-------2` | Germany (50Hertz) |
| `10YFR-RTE------C` | France (RTE) |
| `10YES-REE------0` | Spain (REE) |
| `10YIT-GRTN-----B` | Italy (Terna) |

### 1.6 API Data Domains

The API is organized into the following domains:

| Domain | Description |
|--------|-------------|
| **Market** | Congestion income, allocation results, day-ahead/intraday prices |
| **Load** | Actual total load, day-ahead load forecast, week-ahead forecast |
| **Generation** | Installed capacity, actual generation, forecasts by production type |
| **Transmission** | Cross-border physical flows, transfer capacities |
| **Outages** | Planned and forced outages for generation and transmission |
| **Balancing** | Balancing energy prices, volumes, reserves, imbalance data |
| **Master Data** | Production units, generation units metadata |
| **OMI** | Other market information |

### 1.7 Document Types (documentType Parameter)

Common document type codes used across the API:

| Code | Description |
|------|-------------|
| `A25` | Allocation result document |
| `A44` | Price document |
| `A61` | Estimated Net Transfer Capacity |
| `A65` | System total load |
| `A68` | Installed generation per type |
| `A69` | Wind and solar generation forecast |
| `A70` | Load forecast margin |
| `A71` | Generation forecast |
| `A73` | Actual generation per type |
| `A74` | Wind and solar generation |
| `A75` | Actual generation per generation unit |
| `A77` | Scheduled generation |
| `A78` | Unavailability of generation units |
| `A79` | Unavailability of production units |
| `A80` | Unavailability of offshore grid |
| `A81` | Unavailability of transmission infrastructure |
| `A85` | Imbalance prices |
| `A86` | Imbalance volume |

### 1.8 Business Types (businessType Parameter)

| Code | Description |
|------|-------------|
| `A04` | Base load |
| `A29` | Imports |
| `A30` | Exports |
| `B01` | Solar |
| `B02` | Wind onshore |
| `B03` | Wind offshore |
| `B04` | Fossil gas |
| `B05` | Fossil hard coal |
| `B06` | Fossil lignite |
| `B09` | Geothermal |
| `B10` | Congestion income |
| `B11` | Hydro pumped storage |
| `B12` | Hydro run-of-river |
| `B14` | Nuclear |
| `B15` | Fossil oil |
| `B16` | Solar |
| `B17` | Biomass |
| `B18` | Wind onshore |
| `B19` | Wind offshore |

### 1.9 PSR Types (psrType Parameter - Production Source)

| Code | Description |
|------|-------------|
| `B01` | Biomass |
| `B02` | Fossil Brown coal/Lignite |
| `B03` | Fossil Coal-derived gas |
| `B04` | Fossil Gas |
| `B05` | Fossil Hard coal |
| `B06` | Fossil Oil |
| `B07` | Fossil Oil shale |
| `B08` | Fossil Peat |
| `B09` | Geothermal |
| `B10` | Hydro Pumped Storage |
| `B11` | Hydro Run-of-river and poundage |
| `B12` | Hydro Water Reservoir |
| `B13` | Marine |
| `B14` | Nuclear |
| `B15` | Other renewable |
| `B16` | Solar |
| `B17` | Waste |
| `B18` | Wind Offshore |
| `B19` | Wind Onshore |
| `B20` | Other |

### 1.10 Response Format

All API responses are in **XML format** following IEC 62325 standards. Common document structures:

- `GL_MarketDocument` - Generation/Load documents
- `Publication_MarketDocument` - Publication/allocation documents
- `Unavailability_MarketDocument` - Outage documents
- `Balancing_MarketDocument` - Balancing documents

**Namespace examples**:
- `urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0`
- `urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0`

### 1.11 Time Series Resolution

Data is returned in time series with various resolutions:

| Resolution Code | Description |
|-----------------|-------------|
| `PT15M` | 15-minute intervals |
| `PT30M` | 30-minute intervals |
| `PT60M` | 1-hour intervals |
| `P1D` | Daily |
| `P7D` | Weekly |
| `P1M` | Monthly |
| `P1Y` | Yearly |

### 1.12 Available Endpoints Summary

This section provides a complete reference of all 60+ API endpoints available on the ENTSO-E Transparency Platform, organized by domain. Each endpoint references the corresponding EU Regulation 543/2013 article number where applicable.

---

#### Load Domain (Chapter 3) — 7 Endpoints

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **6.1.A** | Actual Total Load | Actual electricity consumption per bidding zone or control area | `A65` |
| **6.1.B** | Day-ahead Total Load Forecast | Day-ahead load forecast values | `A65` |
| **6.1.C** | Week-ahead Total Load Forecast | Week-ahead load forecast values | `A65` |
| **6.1.D** | Month-ahead Total Load Forecast | Month-ahead load forecast values | `A65` |
| **6.1.E** | Year-ahead Total Load Forecast | Year-ahead load forecast values | `A65` |
| **8.1** | Year-ahead Forecast Margin | Forecast margin between generation and load | `A70` |

---

#### Generation Domain (Chapter 4) — 7 Endpoints

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **14.1.A** | Installed Capacity per Production Type | Aggregated installed generation capacity by production type | `A68` |
| **14.1.B** | Installed Capacity per Production Unit | Per-unit installed generation capacity | `A71` |
| **14.1.C** | Generation Forecast - Day Ahead | Aggregated day-ahead generation forecast | `A71` |
| **14.1.D** | Generation Forecasts for Wind and Solar | Day-ahead and intraday forecasts for wind and solar | `A69` |
| **16.1.A** | Actual Generation per Generation Unit | Actual generation output per individual generation unit | `A73` / `A75` |
| **16.1.B&C** | Actual Generation per Production Type | Aggregated actual generation by production type | `A74` / `A75` |
| **16.1.D** | Water Reservoirs and Hydro Storage Plants | Filling rate of water reservoirs and hydro storage | `A72` |

---

#### Market Domain (Chapter 2) — 12 Endpoints

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **11.1** | Implicit Allocations - Offered Transfer Capacity | NTC/ATC for implicit capacity allocation (day-ahead/intraday) | `A61` |
| **11.1** | Continuous Allocations - Offered Transfer Capacity | Transfer capacity for continuous intraday markets | `A61` |
| **11.1.A** | Explicit Allocations - Offered Transfer Capacity | Transfer capacity for explicit auctions | `A61` |
| **11.1.B** | Flow Based Allocations | Flow-based domain parameters and constraints | `B10` |
| **12.1.A** | Explicit Allocations - Use of Transfer Capacity | Usage of explicitly allocated transfer capacity | `A26` |
| **12.1.A** | Explicit Allocations - Auction Revenue | Revenue from explicit capacity auctions | `A25` |
| **12.1.B** | Total Nominated Capacity | Total nominated schedules between areas | `A26` |
| **12.1.C** | Total Capacity Already Allocated | Already allocated capacity per border | `A26` |
| **12.1.D** | Energy Prices | Day-ahead and intraday energy prices per bidding zone | `A44` |
| **12.1.E** | Congestion Income | Revenue from implicit/flow-based allocations | `A25` |
| **12.1.E** | Implicit Auction - Net Positions | Net import/export positions per bidding zone | `A25` |
| **12.1.H** | Transfer Capacities with Third Countries | NTC with non-EU countries | `A61` |

---

#### Transmission Domain (Chapter 5) — 10 Endpoints

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **9.1** | Expansion and Dismantling Projects | Infrastructure projects affecting cross-border capacity | `A90` |
| **11.1.A** | Forecasted Transfer Capacities | Forecast NTC/ATC values (day-ahead/week-ahead/year-ahead) | `A61` |
| **11.3** | DC Links - Intraday Transfer Limits | Capacity limits on HVDC interconnectors | `A61` |
| **12.1.F** | Commercial Schedules | Scheduled commercial flows per border | `A09` |
| **12.1.F** | Commercial Schedules - Net Positions | Net scheduled import/export positions | `A09` |
| **12.1.G** | Cross-Border Physical Flows | Actual measured physical flows at borders | `A11` |
| **13.1.A** | Redispatching - Internal | Internal redispatching actions | `A63` |
| **13.1.A** | Redispatching - Cross Border | Cross-border redispatching actions | `A63` |
| **13.1.B** | Countertrading | Countertrading actions for congestion management | `A91` |
| **13.1.C** | Costs of Congestion Management | Costs incurred for congestion management | `A92` |

---

#### Outages Domain (Chapter 6) — 8 Endpoints

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **7.1.A-B** | Aggregated Unavailability of Consumption Units | Planned/forced unavailability of consumption units | `A76` |
| **10.1.A&B** | Unavailability of Transmission Infrastructure | Planned/forced transmission outages | `A78` / `A80` |
| **10.1.A&B** | Unavailability of Transmission Infrastructure - Available Capacity | Remaining capacity during outages | `A78` / `A80` |
| **10.1.A&B** | Unavailability of Transmission Infrastructure - Net Position Impact | Impact on net positions | `A78` / `A80` |
| **10.1.C** | Unavailability of Offshore Grid Infrastructure | Offshore grid outages | `A79` |
| **15.1.A&B** | Unavailability of Generation Units | Planned/forced outages of generation units | `A77` / `A80` |
| **15.1.C-D** | Unavailability of Production Units | Planned/forced outages of production units | `A77` / `A80` |
| **IFs** | Fall-backs for Balancing Processes | Fallback activations (mFRR, aFRR, imbalance netting) | `A85` |

---

#### Balancing Domain (Chapter 7) — 23 Endpoints

**Balancing Energy Prices (3 endpoints):**

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **17.1.F** | Prices of Activated Balancing Energy | Prices for activated aFRR, mFRR, RR | `A84` |
| **IF aFRR 3.16** | Cross Border Marginal Prices (CBMPs) | CBMPs for aFRR central selection | `A84` |
| **17.1.G** | Imbalance Prices | System imbalance prices per imbalance price area | `A86` |

**Balancing Energy Bids (5 endpoints):**

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **12.3.B&C** | Balancing Energy Bids | Individual balancing energy bid data | `A37` |
| **12.3.B&C** | Balancing Energy Bids Archives | Historical bid data (>93 days) | `A37` |
| **IFs** | Changes to Bid Availability | Real-time changes to bid availability status | `A37` |
| **12.3.E** | Aggregated Balancing Energy Bids | Aggregated merit order list | `A24` |
| **IFs** | Elastic Demands | Elastic demand curves for aFRR/mFRR | `A24` |

**Volumes (4 endpoints):**

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **IFs** | Netted and Exchanged Volumes | Cross-border netted/exchanged balancing volumes | `A85` |
| **IFs** | Netted and Exchanged Volumes per Border | Per-border breakdown of balancing exchanges | `A85` |
| **17.1.H** | Total Imbalance Volumes | Total system imbalance volumes | `A86` |
| **12.3.A** | Current Balancing State / ACE | Area Control Error and balancing state | `A86` |

**Reserve Procurement (2 endpoints):**

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **17.1.B&C** | Volumes and Prices of Contracted Reserves | Contracted reserve capacity and prices | `A81` |
| **12.3.F** | Procured Balancing Capacity | Procured balancing capacity per reserve type | `A82` |

**FCR Capacity (3 endpoints):**

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **187.2** | FCR Total Capacity | Total FCR capacity per synchronous area | `A26` |
| **187.2** | Shares of FCR Capacity | FCR capacity shares per LFC block | `A26` |
| **190.2** | Sharing of FCR between Synchronous Areas | FCR exchanges between synchronous areas | `A26` |

**FRR/RR Capacity (2 endpoints):**

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **188.3 & 189.2** | FRR & RR Capacity Outlook | Reserve capacity requirements outlook | `A26` |
| **188.4 & 189.3** | FRR and RR Actual Capacity | Actual dimensioned FRR/RR capacity | `A26` |

**Cross-Border & Capacity Allocation (2 endpoints):**

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **12.3.H&I** | Allocation and Use of Cross-Zonal Balancing Capacity | Cross-zonal capacity for balancing | `A38` |
| **IFs 4.3 & 4.4** | Balancing Border Capacity Limitations | Capacity constraints per balancing border | `A38` |

**Financial & System Operation (2 endpoints):**

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| **17.1.I** | Financial Expenses and Income for Balancing | Financial results of balancing | `A87` |
| **185.4** | Results of Criteria Application Process | System operation criteria measurements | `A88` |

---

#### Master Data Domain (Chapter 8) — 1 Endpoint

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| — | Production and Generation Units | Master data for all generation/production units | `A95` |

---

#### OMI Domain (Chapter 9) — 1 Endpoint

| Article | Endpoint Name | Description | documentType |
|---------|---------------|-------------|--------------|
| — | Other Market Information | Market-specific notices and publications | `A73` |

---

#### Quick Reference: Endpoints by documentType

| documentType | Endpoints |
|--------------|-----------|
| `A09` | Commercial Schedules, Net Positions |
| `A11` | Cross-Border Physical Flows |
| `A24` | Aggregated Balancing Energy Bids, Elastic Demands |
| `A25` | Congestion Income, Auction Revenue, Net Positions |
| `A26` | Nominated Capacity, Already Allocated, FCR/FRR/RR Capacity |
| `A37` | Balancing Energy Bids |
| `A38` | Cross-Zonal Balancing Capacity |
| `A44` | Energy Prices (Day-ahead, Intraday) |
| `A61` | Transfer Capacities (NTC/ATC) |
| `A63` | Redispatching |
| `A65` | Total Load (Actual and Forecasts) |
| `A68` | Installed Capacity per Production Type |
| `A69` | Wind and Solar Forecasts |
| `A70` | Forecast Margin |
| `A71` | Generation Forecast, Installed Capacity per Unit |
| `A72` | Water Reservoirs |
| `A73` / `A74` / `A75` | Actual Generation |
| `A77` / `A78` / `A79` / `A80` | Outages/Unavailability |
| `A81` / `A82` | Reserve Procurement |
| `A84` | Balancing Energy Prices |
| `A85` / `A86` / `A87` | Imbalance Data |
| `A90` / `A91` / `A92` | Infrastructure Projects, Countertrading, Congestion Costs |
| `A95` | Master Data |

---

#### Total Endpoint Count by Domain

| Domain | Endpoints |
|--------|-----------|
| Load | 7 |
| Generation | 7 |
| Market | 12 |
| Transmission | 10 |
| Outages | 8 |
| Balancing | 23 |
| Master Data | 1 |
| OMI | 1 |
| **Total** | **69** |

### 1.13 Error Handling

The API returns standard HTTP status codes:
- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid or missing security token
- `404 Not Found` - No data found for the query
- `500 Internal Server Error` - Server-side error

### 1.14 Rate Limiting and Pagination

- **Maximum documents per request**: 100
- **Pagination**: Use `offset` parameter (0-4800) to retrieve additional documents
- **Maximum retrievable**: 4900 documents per query

### 1.15 Contact Information

- **Email**: transparency@entsoe.eu
- **Knowledge Base**: [ENTSO-E Transparency Platform Help](https://transparencyplatform.zendesk.com/hc/en-us/sections/12783116987028-Web-API)

---

## Chapter 2: Market

The Market domain provides access to cross-border capacity allocation data, congestion income, energy prices, and net positions. This data is essential for understanding electricity market dynamics across European borders.

### 2.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`Publication_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0` |

### 2.2 Endpoints

---

#### 2.2.1 Congestion Income (12.1.E)

**Implicit and Flow-based Allocations - Congestion Income**

Returns congestion income data from implicit or flow-based capacity allocations.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A25` | Allocation results |
| `businessType` | **[M]** | `B10` | Congestion income |
| `contract_MarketAgreement.Type` | **[M]** | `A01` or `A07` | A01 = Daily; A07 = Intraday |
| `out_Domain` | **[M]** | EIC Code | Border or Bidding Zone (for Flow Based) |
| `in_Domain` | **[M]** | EIC Code | Same as out_Domain |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A25&businessType=B10&contract_MarketAgreement.Type=A07&out_Domain=10YDOM-CZ-D2---O&in_Domain=10YDOM-CZ-D2---O&periodStart=202308242200&periodEnd=202308252200'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- Data: `price.amount` in EUR/MWH per position

---

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

#### 2.2.3 Implicit Allocations - Offered Transfer Capacity (11.1)

Returns offered transfer capacity for implicit allocations.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A31` | Agreed capacity |
| `auction.Type` | **[M]** | `A01` | Implicit |
| `contract_MarketAgreement.Type` | **[M]** | `A01` or `A07` | A01 = Day ahead; A07 = Intraday |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `Update_DateAndOrTime` | [O] | Numeric datetime | For capacity evolution queries (e.g., `20230313123900`) |
| `ClassificationSequence_AttributeInstanceComponent.Position` | [O] | Integer | Position filter |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A31&auction.Type=A01&contract_MarketAgreement.Type=A01&out_Domain=10YDK-1--------W&in_Domain=10Y1001A1001A82H&periodStart=202212312300&periodEnd=202301012300'
```

**Response Structure:**
- Resolution: `PT60M`
- Data: `quantity` in MAW
- Includes `auction.mRID` identifying the specific auction

---

#### 2.2.4 Transfer Capacities with Third Countries (12.1.H)

Returns transfer capacities allocated with non-EU countries (explicit allocations).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A94` | Non EU allocations |
| `auction.Type` | **[M]** | `A02` | Explicit |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Daily, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `auction.Category` | [O] | Code | A01=Base, A02=Peak, A03=Off Peak, A04=Hourly |
| `classificationSequence_AttributeInstanceComponent.Position` | [O] | Integer | Position filter |

**Example Request (Finland to Russia):**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A94&auction.Type=A02&contract_MarketAgreement.Type=A07&out_Domain=10YFI-1--------U&in_Domain=10Y1001A1001A49F&periodStart=202308232200&periodEnd=202308242200'
```

---

#### 2.2.5 Total Capacity Already Allocated (12.1.C)

Returns capacity that has already been allocated on a border.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity Document |
| `businessType` | **[M]** | `A29` | Already Allocated Capacity |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Daily, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `auction.Category` | [O] | Code | A01=Base, A02=Peak, A03=Off Peak, A04=Hourly |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A26&businessType=A29&contract_MarketAgreement.Type=A01&out_Domain=10YHR-HEP------M&in_Domain=10YBA-JPCC-----D&periodStart=202308242200&periodEnd=202308252200'
```

---

#### 2.2.6 Explicit Allocations - Offered Transfer Capacity (11.1.A)

Returns offered transfer capacity for explicit auctions.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A31` | Agreed capacity |
| `auction.Type` | **[M]** | `A02` | Explicit |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Day ahead, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `auction.Category` | [O] | Code | A01=Base, A02=Peak, A03=Off Peak, A04=Hourly |
| `Update_DateAndOrTime` | [O] | Numeric datetime | For capacity evolution queries |
| `ClassificationSequence_AttributeInstanceComponent.Position` | [O] | Integer | Position filter |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A31&auction.Type=A02&contract_MarketAgreement.Type=A01&out_Domain=10YGB----------A&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

---

#### 2.2.7 Explicit Allocations - Use of Transfer Capacity (12.1.A)

Returns the actual use of allocated transfer capacity including prices.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A25` | Allocation result document |
| `businessType` | **[M]** | `B05` or `A43` | B05=Capacity allocated (with price), A43=Requested capacity (without price) |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Day ahead, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `Auction.Category` | [O] | Code | A01=Base, A02=Peak, A03=Off Peak, A04=Hourly |
| `ClassificationSequence_AttributeInstanceComponent.Position` | [O] | Integer | Position filter |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A25&businessType=B05&contract_MarketAgreement.Type=A07&out_Domain=10YGB----------A&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

---

#### 2.2.8 Explicit Allocations - Auction Revenue (12.1.A)

Returns auction revenue from explicit capacity allocations.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A25` | Allocation result document |
| `businessType` | **[M]** | `B07` | Auction revenue |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Daily, A02=Weekly, A03=Monthly, A04=Yearly, A06=Long Term, A07=Intraday, A08=Quarterly |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A25&businessType=B07&contract_MarketAgreement.Type=A01&out_Domain=10YHR-HEP------M&in_Domain=10YBA-JPCC-----D&periodStart=202308242200&periodEnd=202308252200'
```

---

#### 2.2.9 Implicit Auction - Net Positions (12.1.E)

Returns net positions from implicit auctions for a bidding zone.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A25` | Allocation results |
| `businessType` | **[M]** | `B09` | Net position |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01=Daily, A05=Total, A07=Intraday |
| `out_Domain` | **[M]** | EIC Code | Bidding Zone or Control Area |
| `in_Domain` | **[M]** | EIC Code | **Must be same as out_Domain** |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A25&businessType=B09&contract_MarketAgreement.Type=A07&out_Domain=10YBE----------2&in_Domain=10YBE----------2&periodStart=202308222200&periodEnd=202308232200'
```

**Response Structure:**
- Resolution: `PT15M`
- Data: `quantity` in MAW (positive = export, negative = import)

---

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

#### 2.2.11 Continuous Allocations - Offered Transfer Capacity (11.1)

Returns offered transfer capacity for continuous intraday markets.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `DocumentType` | **[M]** | `A31` or `B33` | A31=Agreed capacity (intermediate), B33=Published offered capacity (most recent) |
| `Auction.Type` | **[M]** | `A08` | Continuous |
| `Out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `In_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Aggregation |
| `PeriodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `PeriodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `Contract_MarketAgreement.Type` | **[M]** | `A07` | Intraday |
| `Update_DateAndOrTime` | [O] | Numeric datetime | For capacity evolution. If omitted, returns most recent published version |
| `offset` | [O] | Integer [0-4800] | Pagination offset |

**Note on Document Types:**
- `A31`: Intermediate OC (Offered Capacity) values
- `B33`: Most recent published OC values

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&DocumentType=A31&Auction.Type=A08&Out_Domain=10YBE----------2&In_Domain=10YNL----------L&PeriodStart=202405152200&PeriodEnd=202405162200&Contract_MarketAgreement.Type=A07'
```

**Response Structure:**
- Resolution: `PT15M`
- Includes `update_DateAndOrTime.dateTime` showing when the capacity was published

---

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

#### 3.4.1 Actual Total Load (6.1.A) - GET Method

Returns realized/actual total electricity load for a bidding zone.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one MTU (Market Time Unit) period

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A16` | Realised |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A16&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202303030000&periodEnd=202303060000'
```

**Response Structure:**
```xml
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
    <mRID>...</mRID>
    <type>A65</type>
    <process.processType>A16</process.processType>
    <TimeSeries>
        <businessType>A04</businessType>
        <outBiddingZone_Domain.mRID>10YCZ-CEPS-----N</outBiddingZone_Domain.mRID>
        <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
        <Period>
            <resolution>PT60M</resolution>
            <Point>
                <position>1</position>
                <quantity>7146</quantity>
            </Point>
            ...
        </Period>
    </TimeSeries>
</GL_MarketDocument>
```

- Resolution: `PT60M` (hourly) or `PT15M`/`PT30M` depending on country
- `businessType`: `A04` (Base load)
- `objectAggregation`: `A01` (Area)

---

#### 3.4.2 Actual Total Load (6.1.A) - POST Method

Alternative method using XML request body instead of query parameters.

| Property | Value |
|----------|-------|
| **Method** | POST |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Content-Type** | `application/xml` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one MTU period

**Headers:**

| Header | Value |
|--------|-------|
| `Content-Type` | `application/xml` |
| `SECURITY_TOKEN` | Your API token |

**Request Body Structure:**
```xml
<StatusRequest_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-5:statusrequestdocument:4:0">
    <mRID>SampleCallToRestfulApi</mRID>
    <type>A59</type>
    <sender_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450</sender_MarketParticipant.mRID>
    <sender_MarketParticipant.marketRole.type>A07</sender_MarketParticipant.marketRole.type>
    <receiver_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450</receiver_MarketParticipant.mRID>
    <receiver_MarketParticipant.marketRole.type>A32</receiver_MarketParticipant.marketRole.type>
    <createdDateTime>2016-01-10T13:00:00Z</createdDateTime>
    <AttributeInstanceComponent>
        <attribute>DocumentType</attribute>
        <attributeValue>A65</attributeValue>
    </AttributeInstanceComponent>
    <AttributeInstanceComponent>
        <attribute>ProcessType</attribute>
        <attributeValue>A16</attributeValue>
    </AttributeInstanceComponent>
    <AttributeInstanceComponent>
        <attribute>OutBiddingZone_Domain</attribute>
        <attributeValue>10YCZ-CEPS-----N</attributeValue>
    </AttributeInstanceComponent>
    <AttributeInstanceComponent>
        <attribute>TimeInterval</attribute>
        <attributeValue>2016-01-01T00:00Z/2016-01-02T00:00Z</attributeValue>
    </AttributeInstanceComponent>
</StatusRequest_MarketDocument>
```

**Note:** The POST method is an alternative for programmatic access when query string length is a concern.

---

#### 3.4.3 Day-ahead Total Load Forecast (6.1.B)

Returns day-ahead load forecast data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one day

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A01` | Day ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A01&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202308140000&periodEnd=202308170000'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `A04` (Base load)
- Returns one TimeSeries per day in the requested period

---

#### 3.4.4 Week-ahead Total Load Forecast (6.1.C)

Returns week-ahead load forecast data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one week

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A31` | Week ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A31&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202308132200&periodEnd=202308202200'
```

**Response Structure:**
- Resolution: varies by TSO (typically `PT60M` or aggregated)
- Returns forecast for the week-ahead period

---

#### 3.4.5 Month-ahead Total Load Forecast (6.1.D)

Returns month-ahead load forecast data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one month

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A32` | Month ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A32&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202307022200&periodEnd=202308062200'
```

**Response Structure:**
- Resolution: varies (daily or weekly aggregation)
- Returns forecast for the month-ahead period

---

#### 3.4.6 Year-ahead Total Load Forecast (6.1.E)

Returns year-ahead load forecast data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one year

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A33` | Year ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A33&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202301012300&periodEnd=202312312300'
```

**Response Structure:**
- Resolution: `P7D` (weekly points)
- `businessType`: `A60` (Forecast)
- Returns weekly forecast values for the entire year

---

#### 3.4.7 Year-ahead Forecast Margin (8.1)

Returns the year-ahead forecast margin (difference between available capacity and forecasted load).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one year

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A70` | Load forecast margin |
| `processType` | **[M]** | `A33` | Year ahead |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A70&processType=A33&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202212312300&periodEnd=202312312300'
```

**Response Structure:**
- Resolution: `P7D` (weekly) or `P1M` (monthly)
- Returns the margin between expected available generation and expected load

---

### 3.5 Business Types in Load Domain

| Code | Description |
|------|-------------|
| `A04` | Base load (used in actual and day-ahead data) |
| `A60` | Forecast (used in year-ahead forecasts) |

### 3.6 Response Resolution by Endpoint

| Endpoint | Typical Resolution | Notes |
|----------|-------------------|-------|
| Actual Total Load | `PT15M`, `PT30M`, or `PT60M` | Varies by country/TSO |
| Day-ahead Forecast | `PT60M` | Hourly values |
| Week-ahead Forecast | `PT60M` or aggregated | Varies by TSO |
| Month-ahead Forecast | `P1D` or `P7D` | Daily or weekly |
| Year-ahead Forecast | `P7D` | Weekly values |
| Forecast Margin | `P7D` or `P1M` | Weekly or monthly |

### 3.7 Common EIC Codes for Load Queries

| Country | EIC Code | Description |
|---------|----------|-------------|
| Austria | `10YAT-APG------L` | APG Control Area |
| Belgium | `10YBE----------2` | Elia |
| Czech Republic | `10YCZ-CEPS-----N` | CEPS |
| Germany | `10Y1001A1001A83F` | Germany (aggregated) |
| France | `10YFR-RTE------C` | RTE |
| Netherlands | `10YNL----------L` | TenneT NL |
| Poland | `10YPL-AREA-----S` | PSE |
| Spain | `10YES-REE------0` | REE |

---

## Chapter 4: Generation

The Generation domain provides access to electricity generation data including installed capacity, actual generation, and forecasts by production type and individual generation units.

### 4.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`GL_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0` |
| **Unit of Measurement** | MAW (Megawatt) |

### 4.2 Important Notes

1. **PsrType Parameter**: For most generation endpoints, the `PsrType` parameter is **optional**. When not provided, the API returns data for **all production types**. When specified, only the requested production type is returned.

2. **Generation vs Consumption**: In response TimeSeries:
   - `inBiddingZone_Domain` attribute = **Generation** values
   - `outBiddingZone_Domain` attribute = **Consumption** values (e.g., pumped storage consumption)

### 4.3 PSR Types (Production Source Types)

| Code | Description |
|------|-------------|
| `B01` | Biomass |
| `B02` | Fossil Brown coal/Lignite |
| `B03` | Fossil Coal-derived gas |
| `B04` | Fossil Gas |
| `B05` | Fossil Hard coal |
| `B06` | Fossil Oil |
| `B07` | Fossil Oil shale |
| `B08` | Fossil Peat |
| `B09` | Geothermal |
| `B10` | Hydro Pumped Storage |
| `B11` | Hydro Run-of-river and poundage |
| `B12` | Hydro Water Reservoir |
| `B13` | Marine |
| `B14` | Nuclear |
| `B15` | Other renewable |
| `B16` | Solar |
| `B17` | Waste |
| `B18` | Wind Offshore |
| `B19` | Wind Onshore |
| `B20` | Other |
| `B25` | Energy storage |

### 4.4 Endpoints

---

#### 4.4.1 Installed Capacity per Production Type (14.1.A)

Returns the installed generation capacity aggregated by production type (year-ahead).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A68` | Installed generation per type |
| `processType` | **[M]** | `A33` | Year ahead |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | Production type (B01-B25). If omitted, returns all types |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A68&processType=A33&in_Domain=10YBE----------2&periodStart=202212312300&periodEnd=202312312300'
```

**Response Structure:**
- Resolution: `P1Y` (yearly)
- `businessType`: `A37` (Installed capacity)
- One TimeSeries per production type with `MktPSRType/psrType` indicating the type
- `objectAggregation`: `A08` (Resource type)

**Example Response Data:**
```xml
<TimeSeries>
    <businessType>A37</businessType>
    <MktPSRType>
        <psrType>B04</psrType>  <!-- Fossil Gas -->
    </MktPSRType>
    <Period>
        <resolution>P1Y</resolution>
        <Point>
            <position>1</position>
            <quantity>6915</quantity>  <!-- MW installed -->
        </Point>
    </Period>
</TimeSeries>
```

---

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

#### 4.4.3 Actual Generation per Production Type (16.1.B&C)

Returns actual electricity generation aggregated by production type.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Important Notes:**
- Response is the same whether using `A74` (Wind & Solar only) or `A75` (All production types)
- `inBiddingZone_Domain` = Generation values
- `outBiddingZone_Domain` = Consumption values

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A75` or `A74` | A75 = All types; A74 = Wind and solar only |
| `processType` | **[M]** | `A16` | Realised |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `psrType` | [O] | Code | Production type (B01-B25). If omitted, returns all types |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A75&processType=A16&in_Domain=10Y1001A1001A83F&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: `PT15M` or `PT60M` (depends on country)
- `businessType`: `A01` (Production)
- One TimeSeries per production type
- `objectAggregation`: `A08` (Resource type)

---

#### 4.4.4 Actual Generation per Generation Unit (16.1.A)

Returns actual generation data for individual generation units (power plants).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- Maximum time interval: 1 day
- Minimum time interval: 1 Market Time Unit (MTU)

**Important Notes:**
- `inBiddingZone_Domain` = **Generation** values
- `outBiddingZone_Domain` = **Consumption** values

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A73` | Actual generation |
| `processType` | **[M]** | `A16` | Realised |
| `in_Domain` | **[M]** | EIC Code | Control Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | Production type filter |
| `RegisteredResource` | [O] | EIC Code | Specific generation unit EIC |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A73&processType=A16&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `A01` (Production)
- `objectAggregation`: `A06` (Resource object)
- Each TimeSeries includes:
  - `registeredResource.mRID` - Unit EIC code
  - `MktPSRType/PowerSystemResources/name` - Plant name (e.g., "DOEL 1")
  - `MktPSRType/psrType` - Production type

**Example Response Data:**
```xml
<TimeSeries>
    <businessType>A01</businessType>
    <registeredResource.mRID codingScheme="A01">22WDOELX1000076X</registeredResource.mRID>
    <MktPSRType>
        <psrType>B14</psrType>  <!-- Nuclear -->
        <PowerSystemResources>
            <mRID codingScheme="A01">22WDOELX1150076X</mRID>
            <name>DOEL 1</name>
        </PowerSystemResources>
    </MktPSRType>
    <Period>
        <resolution>PT60M</resolution>
        <Point>
            <position>1</position>
            <quantity>439</quantity>
        </Point>
    </Period>
</TimeSeries>
```

---

#### 4.4.5 Generation Forecast - Day Ahead (14.1.C)

Returns day-ahead generation forecast (total scheduled generation).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Note:** `inBiddingZone_Domain` = Generation; `outBiddingZone_Domain` = Consumption

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A71` | Generation forecast |
| `processType` | **[M]** | `A01` | Day ahead |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A71&processType=A01&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `A01` (Production)
- Returns total scheduled generation for the bidding zone

---

#### 4.4.6 Generation Forecasts for Wind and Solar (14.1.D)

Returns forecasts specifically for wind and solar generation.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A69` | Wind and solar forecast |
| `processType` | **[M]** | Code | A01 = Day ahead; A18 = Current (intraday); A40 = Intraday |
| `in_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | B16 = Solar; B18 = Wind Offshore; B19 = Wind Onshore |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A69&processType=A01&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `A94` (Solar forecast), `A93` (Wind forecast)
- Separate TimeSeries for each renewable type (Solar B16, Wind Offshore B18, Wind Onshore B19)

**Example - Solar Generation Forecast Pattern:**
```xml
<TimeSeries>
    <businessType>A94</businessType>
    <MktPSRType>
        <psrType>B16</psrType>
    </MktPSRType>
    <Period>
        <resolution>PT60M</resolution>
        <Point><position>1</position><quantity>0</quantity></Point>    <!-- Night -->
        <Point><position>8</position><quantity>337</quantity></Point>  <!-- Morning -->
        <Point><position>13</position><quantity>4029</quantity></Point> <!-- Peak -->
        <Point><position>20</position><quantity>586</quantity></Point> <!-- Evening -->
    </Period>
</TimeSeries>
```

---

#### 4.4.7 Installed Capacity Per Production Unit (14.1.B)

Returns installed capacity for individual generation units (power plants).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A71` | Generation forecast |
| `processType` | **[M]** | `A33` | Year ahead |
| `in_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | Production type filter (B01-B25) |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A71&processType=A33&in_Domain=10YBE----------2&periodStart=202308010000&periodEnd=202308020000'
```

**Response Structure:**
- Resolution: `P1Y` (yearly - single value)
- `businessType`: `A37` (Installed capacity)
- `objectAggregation`: `A06` (Resource object)
- Each TimeSeries includes:
  - `registeredResource.mRID` - Unit EIC code
  - `registeredResource.name` - Plant name
  - `MktPSRType/psrType` - Production type
  - `voltage_PowerSystemResources.highVoltageLimit` - Connection voltage (KVT)

**Example Response Data:**
```xml
<TimeSeries>
    <businessType>A37</businessType>
    <registeredResource.mRID codingScheme="A01">22WDOELX40000793</registeredResource.mRID>
    <registeredResource.name>DOEL 4</registeredResource.name>
    <MktPSRType>
        <psrType>B14</psrType>  <!-- Nuclear -->
        <voltage_PowerSystemResources.highVoltageLimit unit="KVT">380</voltage_PowerSystemResources.highVoltageLimit>
    </MktPSRType>
    <Period>
        <resolution>P1Y</resolution>
        <Point>
            <position>1</position>
            <quantity>1039</quantity>  <!-- MW installed -->
        </Point>
    </Period>
</TimeSeries>
```

---

### 4.5 Document Types Summary

| Code | Description | Use Case |
|------|-------------|----------|
| `A68` | Installed generation per type | Aggregated installed capacity |
| `A69` | Wind and solar forecast | Renewable forecasts |
| `A71` | Generation forecast | Day-ahead scheduled generation, Per-unit installed capacity |
| `A72` | Reservoir filling information | Hydro storage levels |
| `A73` | Actual generation | Per-unit actual generation |
| `A74` | Wind and solar generation | Actual renewable generation |
| `A75` | Actual generation per type | Aggregated actual generation |

### 4.6 Business Types in Generation Domain

| Code | Description |
|------|-------------|
| `A01` | Production (actual generation) |
| `A37` | Installed capacity |
| `A93` | Wind forecast |
| `A94` | Solar forecast |

---

## Chapter 5: Transmission

The Transmission domain provides access to cross-border physical flows, transfer capacities, commercial schedules, congestion management costs, redispatching operations, and infrastructure expansion plans.

### 5.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`Publication_MarketDocument` or `TransmissionNetwork_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:0` or `urn:iec62325.351:tc57wg16:451-6:transmissionnetworkdocument:3:0` |
| **Unit of Measurement** | MAW (Megawatt), MWH (Megawatt-hour), EUR (for costs) |

### 5.2 Key Concepts

1. **in_Domain / out_Domain**: For cross-border flows, these represent the direction of power flow:
   - `out_Domain` → `in_Domain` represents flow FROM out_Domain TO in_Domain

2. **Unlike Web GUI**: API returns **non-netted values** - data is requested per direction, not as a net flow.

3. **Net Positions**: When `in_Domain` = `out_Domain` (same EIC code), the API returns net position data for that area.

### 5.3 Endpoints

---

#### 5.3.1 Cross-Border Physical Flows (12.1.G)

Returns aggregated physical energy flows between bidding zones or control areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Important:** Unlike the Web GUI, the API responds with **non-netted values** as data is requested per direction.

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A11` | Aggregated energy data report |
| `out_Domain` | **[M]** | EIC Code | Origin Control Area, Bidding Zone, or Country |
| `in_Domain` | **[M]** | EIC Code | Destination Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A11&out_Domain=10YDE-RWENET---I&in_Domain=10YBE----------2&periodStart=202308232200&periodEnd=202308242200'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `businessType`: `A66` (Physical flow)
- Returns time series with position/quantity pairs representing power flow in MW

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>A66</businessType>
    <in_Domain.mRID codingScheme="A01">10YBE----------2</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YDE-RWENET---I</out_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <curveType>A01</curveType>
    <Period>
        <resolution>PT15M</resolution>
        <Point>
            <position>1</position>
            <quantity>0</quantity>
        </Point>
    </Period>
</TimeSeries>
```

---

#### 5.3.2 Forecasted Transfer Capacities (11.1.A)

Returns estimated net transfer capacity (NTC) forecasts between areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A61` | Estimated Net Transfer Capacity |
| `contract_MarketAgreement.Type` | **[M]** | Code | A01 = Day ahead; A02 = Week ahead; A03 = Month ahead; A04 = Year ahead |
| `out_Domain` | **[M]** | EIC Code | Origin Control Area or Bidding Zone |
| `in_Domain` | **[M]** | EIC Code | Destination Control Area or Bidding Zone |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A61&contract_MarketAgreement.Type=A01&out_Domain=10YGB----------A&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: Varies by forecast type (PT60M for day-ahead)
- Returns NTC values in MW

---

#### 5.3.3 Commercial Schedules (12.1.F)

Returns finalized commercial schedules for cross-border energy exchanges.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A09` | Finalised schedule |
| `out_Domain` | **[M]** | EIC Code | Origin Control Area, Bidding Zone, or Country |
| `in_Domain` | **[M]** | EIC Code | Destination Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `contract_MarketAgreement.Type` | [O] | Code | A01 = Day Ahead Commercial Schedules; A05 = Total Commercial Schedules |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A09&out_Domain=10YBE----------2&in_Domain=10YFR-RTE------C&periodStart=202410312300&periodEnd=202411012300'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `businessType`: `A06` (Commercial exchange)
- Returns separate TimeSeries for Day-Ahead (`A01`) and Total (`A05`) schedules
- `curveType`: `A03` (Variable-sized blocks)

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>A06</businessType>
    <in_Domain.mRID codingScheme="A01">10YFR-RTE------C</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YBE----------2</out_Domain.mRID>
    <contract_MarketAgreement.type>A01</contract_MarketAgreement.type>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <curveType>A03</curveType>
    <Period>
        <resolution>PT15M</resolution>
        <Point>
            <position>1</position>
            <quantity>0</quantity>
        </Point>
    </Period>
</TimeSeries>
```

---

#### 5.3.4 Commercial Schedules - Net Positions (12.1.F)

Returns net position data for a specific bidding zone (import/export balance).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Key Difference:** Set `in_Domain` = `out_Domain` (same EIC code) to get net positions.

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A09` | Finalised schedule |
| `out_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `in_Domain` | **[M]** | EIC Code | **Same as out_Domain** |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `contract_MarketAgreement.Type` | [O] | Code | A01 = Day Ahead; A05 = Total |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A09&out_Domain=10YAT-APG------L&in_Domain=10YAT-APG------L&periodStart=202506102200&periodEnd=202506112200'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `businessType`: `B09` (Net position)
- Multiple TimeSeries showing exchanges with neighboring zones
- Positive values = export, Negative values = import

---

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

#### 5.3.6 Costs of Congestion Management (13.1.C)

Returns monthly aggregated costs associated with congestion management activities.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response Document** | `TransmissionNetwork_MarketDocument` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A92` | Congestion costs |
| `out_Domain` | **[M]** | EIC Code | Control Area |
| `in_Domain` | **[M]** | EIC Code | Control Area (same as out_Domain) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A92&out_Domain=10YBE----------2&in_Domain=10YBE----------2&periodStart=202112312300&periodEnd=202212312300'
```

**Response Structure:**
- Resolution: `P1M` (monthly)
- `currency_Unit.name`: `EUR`
- Returns `congestionCost_Price.amount` instead of quantity
- Multiple TimeSeries with different `businessType` values:
  - `A46` = System Operator re-dispatching costs
  - `B03` = Redispatching costs
  - `B04` = Countertrading costs

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>A46</businessType>
    <in_Domain.mRID codingScheme="A01">10YBE----------2</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YBE----------2</out_Domain.mRID>
    <currency_Unit.name>EUR</currency_Unit.name>
    <curveType>A01</curveType>
    <Period>
        <timeInterval>
            <start>2021-12-31T23:00Z</start>
            <end>2022-01-31T23:00Z</end>
        </timeInterval>
        <resolution>P1M</resolution>
        <Point>
            <position>1</position>
            <congestionCost_Price.amount>0.00</congestionCost_Price.amount>
        </Point>
    </Period>
</TimeSeries>
```

---

#### 5.3.7 Redispatching - Internal (13.1.A)

Returns internal redispatching data within a control area.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response Document** | `TransmissionNetwork_MarketDocument` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A63` | Redispatch notice |
| `businessType` | **[M]** | `A85` | Internal requirements |
| `out_Domain` | **[M]** | EIC Code | Control Area |
| `in_Domain` | **[M]** | EIC Code | Control Area (**must be same as out_Domain**) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A63&businessType=A85&out_Domain=10YNL----------L&in_Domain=10YNL----------L&periodStart=202310312300&periodEnd=202311302300'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `quantity_Measure_Unit.name`: `MWH`
- `flowDirection.direction`: `A02` (Down regulation)
- Includes `Asset_RegisteredResource` with:
  - `mRID` - Asset EIC code
  - `pSRType.psrType` - Production type (e.g., B21 = Wind onshore)
  - `location.name` - Physical location name

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>A85</businessType>
    <in_Domain.mRID codingScheme="A01">10YNL----------L</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YNL----------L</out_Domain.mRID>
    <quantity_Measure_Unit.name>MWH</quantity_Measure_Unit.name>
    <mktPSRType.psrType>A04</mktPSRType.psrType>
    <curveType>A01</curveType>
    <flowDirection.direction>A02</flowDirection.direction>
    <Asset_RegisteredResource>
        <mRID codingScheme="A01">49T000000000436O</mRID>
        <pSRType.psrType>B21</pSRType.psrType>
        <location.name>Hardenberg - Ommen Dante wit 110 kV</location.name>
    </Asset_RegisteredResource>
    <Period>
        <resolution>PT15M</resolution>
        <Point>
            <position>1</position>
            <quantity>6</quantity>
        </Point>
    </Period>
</TimeSeries>
```

---

#### 5.3.8 Redispatching - Cross Border (13.1.A)

Returns cross-border redispatching data between control areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response Document** | `TransmissionNetwork_MarketDocument` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A63` | Redispatch notice |
| `businessType` | **[M]** | `A46` | System Operator re-dispatching |
| `out_Domain` | **[M]** | EIC Code | Origin Control Area |
| `in_Domain` | **[M]** | EIC Code | Destination Control Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A63&businessType=A46&out_Domain=10YAT-APG------L&in_Domain=10YFR-RTE------C&periodStart=202311010000&periodEnd=202312010000'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `quantity_Measure_Unit.name`: `MWH`
- `flowDirection.direction`: `A02` (Down regulation)
- `mktPSRType.psrType`: Production type affected (e.g., A05 = Coal)

---

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

#### 5.3.10 Countertrading (13.1.B)

Returns countertrading operations data to manage congestion.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response Document** | `TransmissionNetwork_MarketDocument` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A91` | Counter trade notice |
| `out_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone |
| `in_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A91&out_Domain=10YES-REE------0&in_Domain=10YFR-RTE------C&periodStart=202309122200&periodEnd=202309132200'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `B03` (Countertrade)
- `flowDirection.direction`: `A02` (Down regulation)
- Includes `Reason` element with:
  - `code`: Reason code (e.g., `A95` = Congestion in real time)
  - `text`: Human-readable reason

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>B03</businessType>
    <in_Domain.mRID codingScheme="A01">10YFR-RTE------C</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YES-REE------0</out_Domain.mRID>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <curveType>A01</curveType>
    <flowDirection.direction>A02</flowDirection.direction>
    <Period>
        <timeInterval>
            <start>2023-09-12T22:00Z</start>
            <end>2023-09-12T23:00Z</end>
        </timeInterval>
        <resolution>PT60M</resolution>
        <Point>
            <position>1</position>
            <quantity>847</quantity>
        </Point>
    </Period>
    <Reason>
        <code>A95</code>
        <text>Congestion in real time</text>
    </Reason>
</TimeSeries>
```

---

### 5.4 Document Types Summary

| Code | Description | Use Case |
|------|-------------|----------|
| `A09` | Finalised schedule | Commercial schedules, net positions |
| `A11` | Aggregated energy data report | Cross-border physical flows |
| `A61` | Estimated Net Transfer Capacity | Forecasted transfer capacities |
| `A63` | Redispatch notice | Internal and cross-border redispatching |
| `A90` | Interconnector network expansion | Expansion/dismantling projects |
| `A91` | Counter trade notice | Countertrading operations |
| `A92` | Congestion costs | Costs of congestion management |
| `A93` | DC link capacity | DC interconnector limits |

### 5.5 Business Types in Transmission Domain

| Code | Description |
|------|-------------|
| `A06` | Commercial exchange (schedules) |
| `A46` | System Operator re-dispatching |
| `A66` | Physical flow |
| `A85` | Internal requirements (redispatching) |
| `B01` | Interconnector network evolution |
| `B02` | Interconnector network dismantling |
| `B03` | Redispatching / Countertrading costs |
| `B04` | Countertrading costs |
| `B09` | Net position |

### 5.6 Contract/Market Agreement Types

| Code | Description |
|------|-------------|
| `A01` | Day ahead |
| `A02` | Week ahead |
| `A03` | Month ahead |
| `A04` | Year ahead |
| `A05` | Total (all timeframes) |

### 5.7 Flow Direction Codes

| Code | Description |
|------|-------------|
| `A01` | Up regulation (increase) |
| `A02` | Down regulation (decrease) |

### 5.8 Common DC Link EIC Codes

| Interconnector | EIC Code | Connection |
|---------------|----------|------------|
| ElecLink | `11Y0-0000-0265-K` | GB-FR |
| IFA | `10YINTER-IFA---G` | GB-FR |
| BritNed | `11Y0-0000-0264-M` | GB-NL |
| NorNed | `10Y1001A1001A47A` | NO-NL |

---

## Chapter 6: Outages

The Outages domain provides access to planned and unplanned unavailability information for production units, generation units, consumption units, transmission infrastructure, and offshore grid infrastructure.

### 6.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`Unavailability_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-6:outagedocument:3:0` or `urn:iec62325.351:tc57wg16:451-6:outagedocument:4:0` |
| **Response Type** | ZIP file containing XML documents (when multiple outages) or single XML |
| **Unit of Measurement** | MAW (Megawatt) |

### 6.2 Important Notes

1. **Timezone Considerations**: It is important to consider area timezone and winter/summer time:
   - Example (CET winter): February 2, 2016 starts at 2016-02-01T23:00Z and ends at 2016-02-02T23:00Z
   - Example (CET summer): July 5, 2016 starts at 2016-07-04T22:00Z and ends at 2016-07-05T22:00Z

2. **Time Range Limits**:
   - When using only `periodStart` & `periodEnd`: **Limited to 1 year**
   - When using `periodStart` & `periodEnd` WITH `periodStartUpdate` & `periodEndUpdate`: The 1-year limit applies only to the update parameters (not to period parameters)

3. **TimeIntervalUpdate Parameters**: Use `PeriodStartUpdate` and `PeriodEndUpdate` to fetch only the latest updated version of outages. This corresponds to the 'Updated(UTC)' timestamp in the platform. Useful to avoid re-downloading previously fetched outages.

4. **Pagination**: Use `offset` parameter to retrieve more than 100/200 documents. The offset range is [0,4800], allowing up to 5000 documents max.

5. **Response Format**: When multiple outages are returned, the response is a ZIP file containing individual XML documents for each outage.

### 6.3 Endpoints

---

#### 6.3.1 Unavailability of Production Units (15.1.C-D)

Returns unavailability information for production units (aggregated by bidding zone).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A77` | Production unit unavailability |
| `BiddingZone_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID is present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability (unplanned) |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `RegisteredResource` | [O] | EIC Code | Specific Production Unit EIC |
| `mRID` | [O] | String | Document mRID - returns older versions when specified |
| `offset` | [O] | Integer | Pagination offset [0-4800], returns records n+1 to n+100 |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A77&BiddingZone_Domain=10YBE----------2&periodStart=202212312300&periodEnd=202301312300'
```

**Response Structure:**
- Each outage is a separate XML document in the ZIP file
- `process.processType`: `A26` (System operator data)
- `revisionNumber`: Version of the outage document
- Includes `TimeSeries` with availability periods

---

#### 6.3.2 Unavailability of Generation Units (15.1.A&B)

Returns unavailability information for individual generation units.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |
| **Max Results** | 200 documents per request |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A80` | Generation unavailability |
| `BiddingZone_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID is present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `RegisteredResource` | [O] | EIC Code | Specific Generation Unit EIC |
| `mRID` | [O] | String | Document mRID - retrieves older versions |
| `offset` | [O] | Integer | Pagination offset [0-4800], returns records n+1 to n+200 |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A80&BiddingZone_Domain=10YBE----------2&periodStart=202301022200&periodEnd=202301032200'
```

**Response Structure:**
- ZIP file: `OUTAGES_A80_[START]-[END].zip`
- Contains individual XML files for each generation unit outage
- Includes unit details, outage periods, and available capacity

---

#### 6.3.3 Aggregated Unavailability of Consumption Units (7.1.A-B)

Returns aggregated unavailability information for consumption units.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A76` | Load unavailability |
| `BiddingZone_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID is present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime (optional if PeriodStartUpdate defined) |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime (optional if PeriodEndUpdate defined) |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A76&BiddingZone_Domain=10Y1001A1001A82H&periodStart=202310312300&periodEnd=202311302300'
```

**Response Structure:**
- `process.processType`: `A26`
- `unavailability_Time_Period.timeInterval`: Overall outage period
- TimeSeries includes unavailable load in MW

---

#### 6.3.4 Unavailability of Transmission Infrastructure (10.1.A&B)

Returns unavailability information for transmission infrastructure (cross-border links).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A78` | Transmission unavailability |
| `Out_Domain` | **[M]** | EIC Code | Origin Control Area or Bidding Zone (optional if mRID present) |
| `In_Domain` | **[M]** | EIC Code | Destination Control Area or Bidding Zone (optional if mRID present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `mRID` | [O] | String | Document mRID - retrieves older versions |
| `offset` | [O] | Integer | Pagination offset [0-4800], returns records n+1 to n+200 |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A78&Out_Domain=10YFR-RTE------C&In_Domain=10YBE----------2&periodStart=202312012300&periodEnd=202312022300'
```

**Response Structure:**
- ZIP file with individual outage XML documents
- Each outage includes:
  - `Asset_RegisteredResource`: Transmission asset details (mRID, name, location)
  - `asset_PSRType.psrType`: Asset type (e.g., B21 = transmission line)
  - `Available_Period`: Time periods with available capacity values
  - `docStatus`: Current status (A05=Active, A09=Cancelled)

**Example Response Data:**
```xml
<Unavailability_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:outagedocument:3:0">
    <mRID>A47mJe5e9jml9FeSL6jfKg</mRID>
    <revisionNumber>10</revisionNumber>
    <type>A78</type>
    <docStatus>
        <value>A09</value>
    </docStatus>
    <TimeSeries>
        <businessType>A53</businessType>
        <Asset_RegisteredResource>
            <mRID codingScheme="A01">10T-BE-FR-00007U</mRID>
            <name>CHOOZ220 48 MONCE</name>
            <asset_PSRType.psrType>B21</asset_PSRType.psrType>
            <location.name>MONCEAU (B) - CHOOZ (FR) 220.48</location.name>
        </Asset_RegisteredResource>
        <Available_Period>
            <timeInterval>
                <start>2023-07-01T12:30Z</start>
                <end>2023-07-01T13:00Z</end>
            </timeInterval>
            <resolution>PT30M</resolution>
            <Point>
                <position>1</position>
                <quantity>1850</quantity>
            </Point>
        </Available_Period>
    </TimeSeries>
</Unavailability_MarketDocument>
```

---

#### 6.3.5 Unavailability of Transmission Infrastructure - Available Capacity (10.1.A&B)

Alternative query for transmission unavailability filtered by control area (returns outages affecting a specific area).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A78` | Transmission unavailability |
| `ControlArea_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |
| `Asset_RegisteredResource.mRID` | [O] | EIC Code | Specific Transmission Asset EIC |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `mRID` | [O] | String | Document mRID - retrieves older versions |
| `offset` | [O] | Integer | Pagination offset [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A78&ControlArea_Domain=10YFR-RTE------C&periodStart=202312012300&periodEnd=202312022300'
```

---

#### 6.3.6 Unavailability of Transmission Infrastructure - Net Position Impact (10.1.A&B)

Query for transmission outages that impact the net position of a specific area (PTDF-based query).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A78` | Transmission unavailability |
| `pTDF_Domain.mRID` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `Asset_RegisteredResource.mRID` | [O] | EIC Code | Transmission Asset EIC |
| `mRID` | [O] | String | Document mRID |
| `offset` | [O] | Integer | Pagination offset [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A78&pTDF_Domain.mRID=10YBE----------2&periodStart=202312012300&periodEnd=202312022300'
```

---

#### 6.3.7 Unavailability of Offshore Grid Infrastructure (10.1.C)

Returns unavailability information for offshore grid infrastructure (cables, platforms, etc.).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A79` | Offshore grid infrastructure unavailability |
| `BiddingZone_Domain` | **[M]** | EIC Code | Control Area or Bidding Zone (optional if mRID present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime (optional if PeriodStartUpdate defined) |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime (optional if PeriodEndUpdate defined) |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) - mandatory if period not defined |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) - mandatory if period not defined |
| `mRID` | [O] | String | Document mRID - retrieves older versions |
| `offset` | [O] | Integer | Pagination offset [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A79&BiddingZone_Domain=10Y1001A1001A82H&periodStart=202301142300&periodEnd=202301152300'
```

**Response Structure:**
- ZIP file: `OUTAGES_A79_[START]-[END].zip`
- Includes offshore wind farm connection details
- `production_RegisteredResource.pSRType.powerSystemResources.nominalP`: Nominal power in MW
- `biddingZone_Domain.mRID`: Affected bidding zone

---

#### 6.3.8 Fall-backs for Balancing Processes (IFs IN 7.2, mFRR 3.11, aFRR 3.10)

Returns fall-back (disconnection) events for imbalance netting (IN), mFRR, and aFRR processes.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A53` | Outage publication document |
| `ProcessType` | **[M]** | Code | A47 = mFRR; A51 = aFRR; A63 = Imbalance Netting |
| `BusinessType` | **[M]** | Code | C47 = Disconnection; A53 = Planned maintenance; A54 = Unplanned outage; A83 = Auction cancellation |
| `BiddingZone_Domain` | **[M]** | EIC Code | CTA/LFA/REG area code |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime (optional if PeriodStartUpdate defined) |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime (optional if PeriodEndUpdate defined) |
| `DocStatus` | [O] | Code | A13 = Withdrawn (to return withdrawn documents) |
| `mRID` | [O] | String | Document mRID - retrieves older versions |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A53&ProcessType=A51&BusinessType=C47&BiddingZone_Domain=10YBE----------2&periodStart=202301010000&periodEnd=202401010000'
```

**Response Structure:**
- ZIP file with fall-back event documents
- `process.processType`: Type of balancing process affected
- `businessType`: Type of event (disconnection, maintenance, etc.)
- Namespace version: `urn:iec62325.351:tc57wg16:451-6:outagedocument:4:0`

---

### 6.4 Document Types Summary

| Code | Description | Use Case |
|------|-------------|----------|
| `A53` | Outage publication document | Fall-backs for balancing processes |
| `A76` | Load unavailability | Consumption unit outages |
| `A77` | Production unit unavailability | Production unit outages |
| `A78` | Transmission unavailability | Transmission infrastructure outages |
| `A79` | Offshore grid infrastructure unavailability | Offshore grid outages |
| `A80` | Generation unavailability | Generation unit outages |

### 6.5 Business Types in Outages Domain

| Code | Description |
|------|-------------|
| `A53` | Planned maintenance |
| `A54` | Forced unavailability (unplanned outage) |
| `A83` | Auction cancellation (algorithm failure / no solution) |
| `C47` | Disconnection |

### 6.6 Document Status Codes

| Code | Description |
|------|-------------|
| `A05` | Active |
| `A09` | Cancelled |
| `A13` | Withdrawn |

**Note:** When `DocStatus` is not specified, only Active and Cancelled outages are returned by default.

### 6.7 Process Types for Fall-backs

| Code | Description |
|------|-------------|
| `A47` | Manual Frequency Restoration Reserve (mFRR) |
| `A51` | Automatic Frequency Restoration Reserve (aFRR) |
| `A63` | Imbalance Netting (IN) |

### 6.8 Common Query Patterns

**Get all active outages for a bidding zone:**
```bash
documentType=A77
BiddingZone_Domain=[EIC_CODE]
periodStart=[START]
periodEnd=[END]
DocStatus=A05
```

**Get updated outages since last query:**
```bash
documentType=A77
BiddingZone_Domain=[EIC_CODE]
periodStart=[START]
periodEnd=[END]
PeriodStartUpdate=[LAST_QUERY_TIME]
PeriodEndUpdate=[NOW]
```

**Get specific outage history (all versions):**
```bash
documentType=A77
mRID=[OUTAGE_MRID]
```

---

## Chapter 7: Balancing

The Balancing domain provides access to balancing market data including activated balancing energy prices, imbalance prices, balancing energy bids, reserve procurement, and system operation data. This is one of the most extensive domains in the ENTSO-E Transparency Platform.

### 7.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`Balancing_MarketDocument`, `ReserveBid_MarketDocument`, `BidAvailability_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-6:balancingdocument:4:x` (x = version 1-5) |
| **Units** | MAW (MW), MWH (MWh), EUR (currency) |

### 7.2 Reserve Types (Business Types)

| Code | Description |
|------|-------------|
| `A95` | Frequency Containment Reserve (FCR) |
| `A96` | Automatic Frequency Restoration Reserve (aFRR) |
| `A97` | Manual Frequency Restoration Reserve (mFRR) |
| `A98` | Replacement Reserve (RR) |

### 7.3 Process Types

| Code | Description |
|------|-------------|
| `A16` | Realised |
| `A46` | Replacement reserve |
| `A47` | Manual frequency restoration reserve (mFRR) |
| `A51` | Automatic frequency restoration reserve (aFRR) |
| `A52` | Frequency containment reserve (FCR) |
| `A60` | Scheduled activation mFRR |
| `A61` | Direct activation mFRR |
| `A63` | Imbalance Netting |
| `A67` | Central Selection aFRR |
| `A68` | Local Selection aFRR |

### 7.4 Endpoints - Balancing Energy Prices

---

#### 7.4.1 Prices of Activated Balancing Energy (17.1.F)

Returns prices for activated balancing energy.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A84` | Activated balancing prices |
| `processType` | **[M]** | Code | A16 = Realised; A60 = Scheduled mFRR; A61 = Direct mFRR; A68 = Local Selection aFRR |
| `controlArea_Domain` | **[M]** | EIC Code | LFA, IPA, or SCA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `businessType` | [O] | Code | A95 = FCR; A96 = aFRR; A97 = mFRR; A98 = RR |
| `PsrType` | [O] | Code | A04 = Generation; A05 = Load |
| `Standard_MarketProduct` | [O] | `A01` | Standard product |
| `Original_MarketProduct` | [O] | Code | A02 = Specific; A04 = Local |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A84&processType=A16&controlArea_Domain=10YBE----------2&periodStart=202309032200&periodEnd=202309042200&businessType=A96'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- Returns `activation_Price.amount` in EUR/MWh
- `imbalance_Price.category`: Price direction indicator
- `flowDirection.direction`: A01 = Up; A02 = Down

---

#### 7.4.2 Cross Border Marginal Prices (CBMPs) for aFRR Central Selection (IF aFRR 3.16)

Returns cross-border marginal prices from aFRR central selection optimization.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A84` | Activated balancing prices |
| `processType` | **[M]** | `A67` | Central Selection aFRR |
| `businessType` | **[M]** | `A96` | Automatic frequency restoration reserve |
| `Standard_MarketProduct` | **[M]** | `A01` | Standard |
| `controlArea_Domain` | **[M]** | EIC Code | LFA, SCA, or IPA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A84&processType=A67&businessType=A96&Standard_MarketProduct=A01&controlArea_Domain=10YDE-VE-------2&periodStart=202311082300&periodEnd=202311092300'
```

**Response Structure:**
- Resolution: `PT4S` (4-second intervals for aFRR)
- High-frequency price data from central optimization

---

#### 7.4.3 Imbalance Prices (17.1.G)

Returns imbalance settlement prices.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A85` | Imbalance prices |
| `controlArea_Domain` | **[M]** | EIC Code | Scheduling Area or Market Balance Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | A04 = Generation; A05 = Load |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A85&controlArea_Domain=10YNL----------L&periodStart=202310312300&periodEnd=202311012300'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `imbalance_Price.amount`: Price in EUR/MWh
- `imbalance_Price.category`: A04 = generation direction; A05 = consumption direction
- `businessType`: `A19` (Balance Energy Deviation)

---

### 7.5 Endpoints - Balancing Energy Bids

---

#### 7.5.1 Balancing Energy Bids (12.3.B&C)

Returns individual balancing energy bids (within 93-day retention period).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |
| **Data Retention** | 93 days |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A37` | Reserve bid document |
| `businessType` | **[M]** | `B74` | Offer |
| `processType` | **[M]** | Code | A46 = RR; A47 = mFRR; A51 = aFRR |
| `connecting_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Must be within 93-day retention |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | Must be within 93-day retention |
| `offset` | [O] | Integer | Pagination [0-4800], returns n+1 to n+100 |
| `Standard_MarketProduct` | [O] | Code | A01 = Standard; A05 = mFRR scheduled; A07 = mFRR direct |
| `Original_MarketProduct` | [O] | Code | A02 = Specific; A03 = Integrated; A04 = Local |
| `Direction` | [O] | Code | A01 = Up; A02 = Down |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A37&businessType=B74&processType=A47&connecting_Domain=10YCZ-CEPS-----N&periodStart=202410012200&periodEnd=202410022200'
```

---

#### 7.5.2 Balancing Energy Bids Archives (12.3.B&C)

Returns archived balancing energy bids (older than 93 days).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | Nested ZIP files |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A37` | Reserve bid document |
| `businessType` | **[M]** | `B74` | Offer |
| `processType` | **[M]** | Code | A46 = RR; A47 = mFRR; A51 = aFRR |
| `connecting_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Must be outside 93-day retention |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | Must be outside 93-day retention |
| `storageType` | **[M]** | `archive` | Request archived data |
| `offset` | [O] | Integer | Pagination [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A37&businessType=B74&processType=A47&connecting_Domain=10YBE----------2&periodStart=202310072200&periodEnd=202310082200&storageType=archive'
```

---

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

#### 7.5.4 Aggregated Balancing Energy Bids (12.3.E GL EB)

Returns aggregated balancing energy bid data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A24` | Bid document |
| `processType` | **[M]** | Code | A51 = aFRR; A46 = RR; A47 = mFRR; A60/A61 = mFRR variants; A67/A68 = aFRR variants |
| `area_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A24&processType=A51&area_Domain=10YAT-APG------L&periodStart=202309022200&periodEnd=202309032200'
```

**Response Structure:**
- `businessType`: `A14` (Aggregated offers)
- Returns `quantity`, `secondaryQuantity`, and `unavailable_Quantity.quantity`

---

#### 7.5.5 Elastic Demands (IFs aFRR 3.4 & mFRR 3.4)

Returns elastic demand data for balancing markets.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A37` | Reserve bid document |
| `businessType` | **[M]** | `B75` | Need |
| `processType` | **[M]** | Code | A51 = aFRR; A47 = mFRR |
| `Acquiring_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `offset` | [O] | Integer | Pagination [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A37&businessType=B75&processType=A47&Acquiring_Domain=10YCZ-CEPS-----N&periodStart=202311302300&periodEnd=202312012300'
```

---

### 7.6 Endpoints - Volumes

---

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

#### 7.6.3 Total Imbalance Volumes (17.1.H)

Returns total system imbalance volumes.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A86` | Imbalance volume |
| `controlArea_Domain` | **[M]** | EIC Code | Scheduling Area or Market Balance Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `businessType` | [O] | `A19` | Balance Energy Deviation (default) |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A86&controlArea_Domain=10YAT-APG------L&periodStart=202311032300&periodEnd=202311042300'
```

---

#### 7.6.4 Current Balancing State / Area Control Error (12.3.A GL EB)

Returns Area Control Error (ACE) data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A86` | Imbalance volume |
| `businessType` | **[M]** | `B33` | Area Control Error |
| `area_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A86&businessType=B33&area_Domain=10YHU-MAVIR----U&periodStart=202405292200&periodEnd=202405302200'
```

**Response Structure:**
- Resolution: `PT1M` (1-minute intervals)
- Returns ACE values in MW

---

### 7.7 Endpoints - Reserve Procurement

---

#### 7.7.1 Volumes and Prices of Contracted Reserves (17.1.B&C)

Returns contracted reserve volumes and prices.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A81` | Contracted reserves |
| `businessType` | **[M]** | `B95` | Procured capacity |
| `Type_MarketAgreement.Type` | **[M]** | Code | A01 = Daily; A02 = Weekly; A03 = Monthly; A04 = Yearly; A06 = Long term; A13 = Hourly |
| `controlArea_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `processType` | [O] | Code | A51 = aFRR; A52 = FCR; A47 = mFRR; A46 = RR |
| `psrType` | [O] | Code | A03 = Mixed; A04 = Generation; A05 = Load |
| `offset` | [O] | Integer | Pagination [0-4800] |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A81&businessType=B95&processType=A52&Type_MarketAgreement.Type=A01&controlArea_Domain=10YCZ-CEPS-----N&periodStart=202309242200&periodEnd=202309252200'
```

---

#### 7.7.2 Procured Balancing Capacity (12.3.F GL EB)

Returns procured balancing capacity data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A15` | Acquiring system operator reserve schedule |
| `processType` | **[M]** | Code | A46 = RR; A47 = mFRR; A51 = aFRR; A52 = FCR |
| `area_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime (min 1 hour interval) |
| `offset` | [O] | Integer | Pagination [0-4800] |
| `Type_MarketAgreement.Type` | [O] | Code | A01 = Daily; A02 = Weekly; A03 = Monthly; A04 = Yearly; A05 = Total; A06 = Long term; A07 = Intraday; A13 = Hourly |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A15&processType=A51&area_Domain=10YDE-VE-------2&periodStart=202306150000&periodEnd=202306150100'
```

---

### 7.8 Endpoints - FCR (Frequency Containment Reserve)

---

#### 7.8.1 FCR Total Capacity (187.2 SO GL)

Returns total FCR capacity for a synchronous area.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | `A25` | General Capacity Information |
| `area_Domain` | **[M]** | EIC Code | Synchronous Area (e.g., 10YEU-CONT-SYNC0) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A26&businessType=A25&area_Domain=10YEU-CONT-SYNC0&periodStart=202312312300&periodEnd=202412312300'
```

---

#### 7.8.2 Shares of FCR Capacity (187.2 SO GL)

Returns FCR capacity shares per LFC block.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | `B32` | FCR sharing |
| `area_Domain` | **[M]** | EIC Code | LFC Block |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

#### 7.8.3 Sharing of FCR between Synchronous Areas (190.2 SO GL)

Returns FCR exchange data between synchronous areas.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | `A95` | Frequency Containment Reserve |
| `Acquiring_Domain` | **[M]** | EIC Code | Synchronous Area |
| `Connecting_Domain` | **[M]** | EIC Code | Synchronous Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

### 7.9 Endpoints - FRR/RR Capacity

---

#### 7.9.1 FRR & RR Capacity Outlook (188.3 & 189.2 SO GL)

Returns year-ahead FRR and RR capacity outlook.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | Code | A96 = aFRR; A97 = mFRR; A98 = RR |
| `processType` | **[M]** | `A33` | Year ahead |
| `area_Domain` | **[M]** | EIC Code | LFC Block |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

#### 7.9.2 FRR and RR Actual Capacity (188.4 & 189.3 SO GL)

Returns actual FRR and RR capacity data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A26` | Capacity document |
| `businessType` | **[M]** | Code | A96 = aFRR; A97 = mFRR; A98 = RR |
| `processType` | **[M]** | `A16` | Realised |
| `area_Domain` | **[M]** | EIC Code | LFC Block |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

### 7.10 Endpoints - Cross-Border & Capacity Allocation

---

#### 7.10.1 Allocation and Use of Cross-Zonal Balancing Capacity (12.3.H&I)

Returns cross-zonal balancing capacity allocation data.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A38` | Allocation result document |
| `processType` | **[M]** | Code | A51 = aFRR; A47 = mFRR; A46 = RR |
| `Acquiring_Domain` | **[M]** | EIC Code | Scheduling Area |
| `Connecting_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

#### 7.10.2 Balancing Border Capacity Limitations (IFs 4.3 & 4.4)

Returns capacity limitations on balancing borders.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `B42` | Capacity Allocation Document |
| `Acquiring_Domain` | **[M]** | EIC Code | LFA/SCA |
| `Connecting_Domain` | **[M]** | EIC Code | LFA/SCA |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

---

### 7.11 Endpoints - Financial & System Operation

---

#### 7.11.1 Financial Expenses and Income for Balancing (17.1.I)

Returns financial data related to balancing operations.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A87` | Financial situation |
| `controlArea_Domain` | **[M]** | EIC Code | Control Area or Market Balance Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A87&controlArea_Domain=10YHU-MAVIR----U&periodStart=202301312300&periodEnd=202302282300'
```

---

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

#### 8.2.1 Production and Generation Units

Returns configuration data for commissioned production units in a given bidding zone on a specific date.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A95` | Configuration document |
| `businessType` | **[M]** | `B11` | Production unit |
| `BiddingZone_Domain` | **[M]** | EIC Code | Bidding Zone or Control Area |
| `Implementation_DateAndOrTime` | **[M]** | `yyyy-MM-dd` | Date (e.g., 2017-01-01) |
| `psrType` | [O] | Code | Filter by production type (B01-B20) |

**PSR Types (Production Source Types):**

| Code | Description |
|------|-------------|
| `B01` | Biomass |
| `B02` | Fossil Brown coal/Lignite |
| `B03` | Fossil Coal-derived gas |
| `B04` | Fossil Gas |
| `B05` | Fossil Hard coal |
| `B06` | Fossil Oil |
| `B07` | Fossil Oil shale |
| `B08` | Fossil Peat |
| `B09` | Geothermal |
| `B10` | Hydro Pumped Storage |
| `B11` | Hydro Run-of-river and poundage |
| `B12` | Hydro Water Reservoir |
| `B13` | Marine |
| `B14` | Nuclear |
| `B15` | Other renewable |
| `B16` | Solar |
| `B17` | Waste |
| `B18` | Wind Offshore |
| `B19` | Wind Onshore |
| `B20` | Other |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A95&businessType=B11&BiddingZone_Domain=10YBE----------2&Implementation_DateAndOrTime=2017-01-01'
```

**Example with PSR Type filter (Fossil Gas only):**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A95&businessType=B11&BiddingZone_Domain=10YBE----------2&Implementation_DateAndOrTime=2017-01-01&psrType=B04'
```

**Response Structure:**

The response contains one `TimeSeries` element per production unit with:

| Element | Description |
|---------|-------------|
| `mRID` | Unique identifier for the TimeSeries |
| `businessType` | `B11` (Production unit) |
| `implementation_DateAndOrTime.date` | Commissioning date |
| `biddingZone_Domain.mRID` | EIC code of the bidding zone |
| `registeredResource.mRID` | EIC code of the production unit |
| `registeredResource.name` | Name of the production unit |
| `registeredResource.location.name` | Location (usually country) |
| `ControlArea_Domain/mRID` | Control area EIC code |
| `Provider_MarketParticipant/mRID` | Market participant EIC code |
| `MktPSRType/psrType` | Production type code (B01-B20) |
| `MktPSRType/production_PowerSystemResources.highVoltageLimit` | Connection voltage in KVT |
| `MktPSRType/nominalIP_PowerSystemResources.nominalP` | Total nominal power in MAW |
| `GeneratingUnit_PowerSystemResources` | Individual generating units (one or more) |

**Generating Unit Details:**

Each `GeneratingUnit_PowerSystemResources` element contains:

| Element | Description |
|---------|-------------|
| `mRID` | EIC code of the generating unit |
| `name` | Name of the generating unit |
| `nominalP` | Nominal power in MAW |
| `generatingUnit_PSRType.psrType` | Production type |
| `generatingUnit_Location.name` | Location |

**Example Response Data:**
```xml
<Configuration_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:configurationdocument:3:0">
    <mRID>e52e35a2c0844e8ca98cd46999f0e39d</mRID>
    <type>A95</type>
    <process.processType>A39</process.processType>
    <TimeSeries>
        <mRID>b362105694c34556</mRID>
        <businessType>B11</businessType>
        <implementation_DateAndOrTime.date>2014-10-01</implementation_DateAndOrTime.date>
        <biddingZone_Domain.mRID codingScheme="A01">10YBE----------2</biddingZone_Domain.mRID>
        <registeredResource.mRID codingScheme="A01">22WSAINT-000221B</registeredResource.mRID>
        <registeredResource.name>SAINT-GHISLAIN STEG</registeredResource.name>
        <registeredResource.location.name>Belgium</registeredResource.location.name>
        <ControlArea_Domain>
            <mRID codingScheme="A01">10YBE----------2</mRID>
        </ControlArea_Domain>
        <Provider_MarketParticipant>
            <mRID codingScheme="A01">10X1001A1001A094</mRID>
        </Provider_MarketParticipant>
        <MktPSRType>
            <psrType>B04</psrType>
            <production_PowerSystemResources.highVoltageLimit unit="KVT">150</production_PowerSystemResources.highVoltageLimit>
            <nominalIP_PowerSystemResources.nominalP unit="MAW">350</nominalIP_PowerSystemResources.nominalP>
            <GeneratingUnit_PowerSystemResources>
                <mRID codingScheme="A01">22WSAINT-150221B</mRID>
                <name>SAINT-GHISLAIN STEG</name>
                <nominalP unit="MAW">350</nominalP>
                <generatingUnit_PSRType.psrType>B04</generatingUnit_PSRType.psrType>
                <generatingUnit_Location.name>Belgium</generatingUnit_Location.name>
            </GeneratingUnit_PowerSystemResources>
        </MktPSRType>
    </TimeSeries>
    <!-- Additional TimeSeries for other production units -->
</Configuration_MarketDocument>
```

**Example: Multi-Unit Production Facility (Pumped Storage):**
```xml
<TimeSeries>
    <mRID>d70176d8ff70447c</mRID>
    <businessType>B11</businessType>
    <registeredResource.mRID codingScheme="A01">22WCOOXII000070C</registeredResource.mRID>
    <registeredResource.name>COO II T</registeredResource.name>
    <MktPSRType>
        <psrType>B10</psrType>
        <nominalIP_PowerSystemResources.nominalP unit="MAW">690</nominalIP_PowerSystemResources.nominalP>
        <!-- Multiple generating units within the same production unit -->
        <GeneratingUnit_PowerSystemResources>
            <mRID codingScheme="A01">22WCOOX5X000061A</mRID>
            <name>COO 5 T</name>
            <nominalP unit="MAW">230</nominalP>
        </GeneratingUnit_PowerSystemResources>
        <GeneratingUnit_PowerSystemResources>
            <mRID codingScheme="A01">22WCOOX6X000064W</mRID>
            <name>COO 6 T</name>
            <nominalP unit="MAW">230</nominalP>
        </GeneratingUnit_PowerSystemResources>
        <GeneratingUnit_PowerSystemResources>
            <mRID codingScheme="A01">22WCOOX4X0000588</mRID>
            <name>COO 4 T</name>
            <nominalP unit="MAW">230</nominalP>
        </GeneratingUnit_PowerSystemResources>
    </MktPSRType>
</TimeSeries>
```

---

### 8.3 Document Types Summary

| Code | Description |
|------|-------------|
| `A95` | Configuration document |

### 8.4 Business Types in Master Data

| Code | Description |
|------|-------------|
| `B11` | Production unit |

### 8.5 Use Cases

1. **Get all production units in a bidding zone:**
   - Query without `psrType` to retrieve all commissioned units

2. **Get specific technology type:**
   - Add `psrType` parameter to filter (e.g., `psrType=B14` for nuclear)

3. **Historical analysis:**
   - Change `Implementation_DateAndOrTime` to see which units were commissioned at different dates

4. **Cross-reference with generation data:**
   - Use `registeredResource.mRID` from master data to filter actual generation queries

---

## Chapter 9: OMI (Other Market Information)

The OMI (Other Market Information) domain provides access to general market announcements and transparency information that doesn't fit into other specific categories. This includes announcements about infrastructure delays, market events, and other relevant information published by TSOs.

### 9.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`OtherTransparencyMarketInformation_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-n:otmidocument:1:0` |
| **Response Type** | ZIP file containing XML documents |

### 9.2 Endpoints

---

#### 9.2.1 Other Market Information

Returns other market information documents (announcements, notifications, events).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |
| **Max Results** | 200 documents per request |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `B47` | Other market information |
| `ControlArea_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) - mandatory if period not defined |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) - mandatory if period not defined |
| `Offset` | [O] | Integer | Pagination [0-4800], returns n+1 to n+200 |
| `mRID` | [O] | String | Query individual versions of a specific event |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=B47&ControlArea_Domain=10YDE-EON------1&periodStart=202409232200&periodEnd=202409242200'
```

**Example Request with Update Filter:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=B47&ControlArea_Domain=10YDE-EON------1&PeriodStartUpdate=202402221000&PeriodEndUpdate=202402231200'
```

**Response Structure:**

| Element | Description |
|---------|-------------|
| `mRID` | Unique document identifier (Base64 encoded) |
| `revisionNumber` | Version number of the document |
| `type` | `B47` (Other market information) |
| `sender_MarketParticipant.mRID` | EIC code of the publishing TSO |
| `sender_MarketParticipant.marketRole.type` | `A39` (Data provider) |
| `docStatus/value` | Document status (A05, A09, A13) |
| `publication_DateAndOrTime.dateTime` | Publication timestamp |
| `start_DateAndOrTime.dateTime` | Event start time |
| `end_DateAndOrTime.dateTime` | Event end time |
| `reason.code` | Reason code (e.g., A95 = Congestion in real time) |
| `reason.text` | Human-readable description of the event |

**Example Response Data:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<OtherTransparencyMarketInformation_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-n:otmidocument:1:0">
    <mRID>ZWQ5ODdjZjZhYWFkZDA5Yzk0MThkYjUwOGMxNDgxZTk=</mRID>
    <revisionNumber>1</revisionNumber>
    <type>B47</type>
    <sender_MarketParticipant.mRID codingScheme="A01">10XDE-EON-NETZ-C</sender_MarketParticipant.mRID>
    <sender_MarketParticipant.marketRole.type>A39</sender_MarketParticipant.marketRole.type>
    <receiver_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450</receiver_MarketParticipant.mRID>
    <receiver_MarketParticipant.marketRole.type>A39</receiver_MarketParticipant.marketRole.type>
    <createdDateTime>2024-10-08T11:34:58Z</createdDateTime>
    <docStatus>
        <value>A05</value>
    </docStatus>
    <publication_DateAndOrTime.dateTime>2024-09-19T09:11:00Z</publication_DateAndOrTime.dateTime>
    <start_DateAndOrTime.dateTime>2024-09-18T10:00</start_DateAndOrTime.dateTime>
    <end_DateAndOrTime.dateTime>2025-12-15T10:59</end_DateAndOrTime.dateTime>
    <reason.code>A95</reason.code>
    <reason.text>Delay in the completion of the DolWin5 grid connection system until probably 15 December 2025</reason.text>
</OtherTransparencyMarketInformation_MarketDocument>
```

---

### 9.3 Document Types Summary

| Code | Description |
|------|-------------|
| `B47` | Other market information |

### 9.4 Document Status Codes

| Code | Description |
|------|-------------|
| `A05` | Active |
| `A09` | Cancelled |
| `A13` | Withdrawn |

### 9.5 Use Cases

1. **Get all active announcements:**
   - Use `DocStatus=A05` to filter only active events

2. **Track updates since last query:**
   - Use `PeriodStartUpdate` and `PeriodEndUpdate` to get only new/updated information

3. **Get history of a specific event:**
   - Use `mRID` parameter to retrieve all versions of a particular announcement

4. **Monitor infrastructure delays:**
   - Query specific TSO control areas for grid connection and infrastructure updates

---

## Appendix A: Quick Reference

### Example API Call (cURL)

```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A16&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202308232200&periodEnd=202308242200'
```

### Common Query Patterns

**Get Actual Load for a Country**:
```
documentType=A65
processType=A16
outBiddingZone_Domain=[EIC_CODE]
periodStart=[START]
periodEnd=[END]
```

**Get Actual Generation by Type**:
```
documentType=A75
processType=A16
in_Domain=[EIC_CODE]
periodStart=[START]
periodEnd=[END]
```

**Get Day-Ahead Prices**:
```
documentType=A44
in_Domain=[EIC_CODE]
out_Domain=[EIC_CODE]
periodStart=[START]
periodEnd=[END]
```

