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
| `A85` | Imbalance volume |
| `A86` | Imbalance prices |

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
| **16.1.B&C** | Actual Generation per Production Type | Aggregated actual generation by production type | `A73` / `A74` |
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
| **17.1.G** | Imbalance Prices | System imbalance prices per imbalance price area | `A85` |

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