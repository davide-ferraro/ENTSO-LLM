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
