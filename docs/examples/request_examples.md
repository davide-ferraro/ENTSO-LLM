# ENTSO-E API Request Examples Reference

> **Purpose:** This document provides 260 working request examples for the ENTSO-E Transparency Platform API, organized by endpoint type. Use these examples as templates for constructing API queries.

**Base URL:** `https://web-api.tp.entsoe.eu/api`  
**Authentication:** Add `securityToken=YOUR_API_KEY` to all requests

---

## 🔍 Quick Navigation

| Category | Endpoints | Jump To |
|----------|-----------|---------|
| **Transmission Capacity** | E01-E09 | [Nominated Capacity](#-endpoint-1-total-nominated-capacity-121b), [Allocated Capacity](#-endpoint-4-total-capacity-already-allocated-121c), [Transfer Limits](#-endpoint-21-forecasted-transfer-capacities-111a) |
| **Energy Prices** | E10, E46-E58 | [Day-ahead Prices](#-endpoint-10-day-ahead-energy-prices-121d), [Regional Prices](#-endpoint-46-day-ahead-prices---central-european-countries) |
| **Load Data** | E11-E13, E15, E51 | [Actual Load](#-endpoint-11-actual-total-load-61a), [Load Forecasts](#-endpoint-12-day-ahead-total-load-forecast-61b) |
| **Generation** | E14, E16-E19, E52-E53, E61 | [By Unit](#-endpoint-16-actual-generation-per-generation-unit-161a), [By Type](#-endpoint-17-actual-generation-per-production-type-161bc) |
| **Physical Flows** | E20-E23, E49, E54, E59-E60 | [Cross-border Flows](#-endpoint-20-cross-border-physical-flows-121g), [Commercial Schedules](#-endpoint-22-commercial-schedules-121f) |
| **Outages** | E24-E25, E37, E62-E63 | [Generation Outages](#-endpoint-24-unavailability-of-generation-units-151ab), [Transmission Outages](#-endpoint-25-unavailability-of-transmission-infrastructure-101ab) |
| **Balancing** | E26-E30, E41, E43, E48, E55, E64-E65 | [Imbalance Prices](#-endpoint-26-imbalance-prices-171g), [ACE](#-endpoint-28-current-balancing-state--ace-123a) |
| **⚠️ Sparse Data** | E29, E31-E36, E38-E40, E42, E44-E45, E50 | [No Data Endpoints](#-endpoints-with-no-successful-requests) |

---

## 📊 Coverage Summary

| Data Availability | Endpoints | Examples |
|-------------------|-----------|----------|
| ✅ **Working examples** | 51 endpoints | 204 requests |
| ⚠️ **No data available** | 14 endpoints | 56 requests (documented for reference) |

### Endpoint Categories

| Category | Endpoint Numbers | Data Status |
|----------|------------------|-------------|
| Market/Transmission | E01-E10 | ✅ All working |
| Load | E11-E13, E15, E51 | ✅ All working |
| Generation | E14, E16-E19, E52-E53, E61 | ✅ All working |
| Physical Flows | E20-E23, E49, E54, E59-E60 | ✅ All working |
| Day-ahead Prices | E46-E58 | ✅ All working |
| Outages | E24-E25, E37, E62-E63 | ✅ All working |
| Balancing | E26-E28, E30, E41, E43, E48, E55, E64-E65 | ✅ All working |
| Sparse Data | E29, E31-E36, E38-E40, E42, E44-E45, E50 | ⚠️ See [explanations](#-endpoints-with-no-successful-requests) |

---

## 📝 How to Use These Examples

### Request Structure
All API requests use this format:
```
GET {Base_URL}?securityToken={API_KEY}&{parameters}
```

### Example Request (cURL)
```bash
curl "https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A16&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202601072200&periodEnd=202601082200"
```

### Parameter Format Notes
- **periodStart/periodEnd:** Format `YYYYMMDDHHMM` in UTC
- **Domain codes:** 16-character EIC codes (see reference at end)
- **documentType:** 3-character code (e.g., `A65`, `A44`)

---

## 📋 Endpoint 1: Total Nominated Capacity (12.1.B)

**Document Type:** `A26`  
**Business Type:** `B08`  
**Description:** Total nominated schedules between areas

### ✅ Variant 1.1: GB → BE (1 day)
📄 Response: 6.5 KB | **File:** `E01_v1_nominated_GB_BE_1day.xml`

```python
{
    "documentType": "A26",
    "businessType": "B08",
    "out_Domain": "10YGB----------A",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 1.2: FR → DE-LU (1 day)
📄 Response: 1.9 KB | **File:** `E01_v2_nominated_FR_DE_1day.xml`

```python
{
    "documentType": "A26",
    "businessType": "B08",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 1.3: ES → FR (1 day)
📄 Response: 2.9 KB | **File:** `E01_v3_fix3_nominated_ES_FR_1day.xml`

```python
{
    "documentType": "A26",
    "businessType": "B08",
    "out_Domain": "10YES-REE------0",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 1.4: AT → IT (Dec 2025)
📄 Response: 2.9 KB | **File:** `E01_v4_nominated_AT_IT_dec2025.xml`

```python
{
    "documentType": "A26",
    "businessType": "B08",
    "out_Domain": "10YAT-APG------L",
    "in_Domain": "10YIT-GRTN-----B",
    "periodStart": "202512010000",
    "periodEnd": "202512070000"
}
```

---

## 📋 Endpoint 2: Implicit Allocations - Offered Transfer Capacity (11.1)

**Document Type:** `A31`  
**Auction Type:** `A01` (implicit)  
**Description:** NTC/ATC for implicit capacity allocation (day-ahead/intraday)

### ✅ Variant 2.1: DK1 → DE-LU (day-ahead, daily, 1 day)
📄 Response: 2.0 KB | **File:** `E02_v1_implicit_DK1_DE_dayahead_1day.xml`

```python
{
    "documentType": "A31",
    "auction.Type": "A01",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YDK-1--------W",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 2.2: BE → NL (day-ahead, intraday, 1 day)
📄 Response: 45.8 KB | **File:** `E02_v2_implicit_BE_NL_intraday_1day.xml`

```python
{
    "documentType": "A31",
    "auction.Type": "A01",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YBE----------2",
    "in_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 2.3: FR → ES (day-ahead, daily, 7 days)
📄 Response: 7.7 KB | **File:** `E02_v3_implicit_FR_ES_dayahead_7days.xml`

```python
{
    "documentType": "A31",
    "auction.Type": "A01",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 2.4: NL → DE (implicit, intraday, 1 day)
📄 Response: 44.8 KB | **File:** `E02_v4_fix4_implicit_NL_DE_intraday.xml`

```python
{
    "documentType": "A31",
    "auction.Type": "A01",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YNL----------L",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 3: Transfer Capacities with Third Countries (12.1.H)

**Document Type:** `A94`  
**Auction Type:** `A02` (explicit)  
**Description:** NTC with non-EU countries

### ✅ Variant 3.1: FI → RU (explicit, intraday, 1 day)
📄 Response: 2.1 KB | **File:** `E03_v1_third_FI_RU_1day.xml`

```python
{
    "documentType": "A94",
    "auction.Type": "A02",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YFI-1--------U",
    "in_Domain": "10Y1001A1001A49F",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 3.2: RU → FI (explicit, intraday, 1 day) - Reverse Direction
📄 Response: 2.1 KB | **File:** `E03_v2_third_RU_FI_1day.xml`

```python
{
    "documentType": "A94",
    "auction.Type": "A02",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10Y1001A1001A49F",
    "in_Domain": "10YFI-1--------U",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 3.3: FI → RU (explicit, intraday, 7 days)
📄 Response: 4.1 KB | **File:** `E03_v3_third_FI_RU_7days.xml`

```python
{
    "documentType": "A94",
    "auction.Type": "A02",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YFI-1--------U",
    "in_Domain": "10Y1001A1001A49F",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 3.4: FI → RU (explicit, Dec 2025)
📄 Response: 3.8 KB | **File:** `E03_v4_third_FI_RU_dec2025.xml`

```python
{
    "documentType": "A94",
    "auction.Type": "A02",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YFI-1--------U",
    "in_Domain": "10Y1001A1001A49F",
    "periodStart": "202512010000",
    "periodEnd": "202512070000"
}
```

---

## 📋 Endpoint 4: Total Capacity Already Allocated (12.1.C)

**Document Type:** `A26`  
**Business Type:** `A29`  
**Description:** Already allocated capacity per border

### ✅ Variant 4.1: HR → BA (daily, 1 day)
📄 Response: 2.1 KB | **File:** `E04_v1_allocated_HR_BA_1day.xml`

```python
{
    "documentType": "A26",
    "businessType": "A29",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YHR-HEP------M",
    "in_Domain": "10YBA-JPCC-----D",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 4.2: AT → HU (daily, 1 day)
📄 Response: 1.8 KB | **File:** `E04_v2_allocated_AT_HU_1day.xml`

```python
{
    "documentType": "A26",
    "businessType": "A29",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YAT-APG------L",
    "in_Domain": "10YHU-MAVIR----U",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 4.3: HR → BA (daily, 7 days)
📄 Response: 4.8 KB | **File:** `E04_v3_allocated_HR_BA_7days.xml`

```python
{
    "documentType": "A26",
    "businessType": "A29",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YHR-HEP------M",
    "in_Domain": "10YBA-JPCC-----D",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 4.4: SI → HR (daily, Dec 2025)
📄 Response: 3.1 KB | **File:** `E04_v4_allocated_SI_HR_dec2025.xml`

```python
{
    "documentType": "A26",
    "businessType": "A29",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YSI-ELES-----O",
    "in_Domain": "10YHR-HEP------M",
    "periodStart": "202512010000",
    "periodEnd": "202512070000"
}
```

---

## 📋 Endpoint 5: Explicit Allocations - Offered Transfer Capacity (11.1.A)

**Document Type:** `A31`  
**Auction Type:** `A02` (explicit)  
**Description:** Transfer capacity for explicit auctions

### ✅ Variant 5.1: GB → BE (daily, 1 day)
📄 Response: 3.6 KB | **File:** `E05_v1_explicit_GB_BE_daily_1day.xml`

```python
{
    "documentType": "A31",
    "auction.Type": "A02",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YGB----------A",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 5.2: GB → BE (monthly, 7 days)
📄 Response: 1.8 KB | **File:** `E05_v2_explicit_GB_BE_monthly_7days.xml`

```python
{
    "documentType": "A31",
    "auction.Type": "A02",
    "contract_MarketAgreement.Type": "A03",
    "out_Domain": "10YGB----------A",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 5.3: HR → BA (daily, 1 day)
📄 Response: 2.7 KB | **File:** `E05_v3_fix2_explicit_HR_BA_1day.xml`

```python
{
    "documentType": "A31",
    "auction.Type": "A02",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YHR-HEP------M",
    "in_Domain": "10YBA-JPCC-----D",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 5.4: BE → GB (daily, Dec 2025) - Reverse Direction
📄 Response: 7.0 KB | **File:** `E05_v4_explicit_BE_GB_dec2025.xml`

```python
{
    "documentType": "A31",
    "auction.Type": "A02",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YBE----------2",
    "in_Domain": "10YGB----------A",
    "periodStart": "202512010000",
    "periodEnd": "202512070000"
}
```

---

## 📋 Endpoint 6: Explicit Allocations - Use of Transfer Capacity (12.1.A)

**Document Type:** `A25`  
**Business Type:** `B05`  
**Description:** Usage of explicitly allocated transfer capacity

### ✅ Variant 6.1: GB → BE (intraday, 1 day)
📄 Response: 11.9 KB | **File:** `E06_v1_use_GB_BE_intraday_1day.xml`

```python
{
    "documentType": "A25",
    "businessType": "B05",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YGB----------A",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 6.2: BE → GB (intraday, 1 day) - Reverse Direction
📄 Response: 11.7 KB | **File:** `E06_v2_use_BE_GB_intraday_1day.xml`

```python
{
    "documentType": "A25",
    "businessType": "B05",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YBE----------2",
    "in_Domain": "10YGB----------A",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 6.3: GB → BE (daily, 7 days)
📄 Response: 38.9 KB | **File:** `E06_v3_use_GB_BE_daily_7days.xml`

```python
{
    "documentType": "A25",
    "businessType": "B05",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YGB----------A",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 6.4: HR → BA (intraday, 1 day)
📄 Response: 10.0 KB | **File:** `E06_v4_fix1_use_HR_BA_1day.xml`

```python
{
    "documentType": "A25",
    "businessType": "B05",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YHR-HEP------M",
    "in_Domain": "10YBA-JPCC-----D",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 7: Explicit Allocations - Auction Revenue (12.1.A)

**Document Type:** `A25`  
**Business Type:** `B07`  
**Description:** Revenue from explicit capacity auctions

### ✅ Variant 7.1: HR → BA (daily, 1 day)
📄 Response: 2.2 KB | **File:** `E07_v1_revenue_HR_BA_1day.xml`

```python
{
    "documentType": "A25",
    "businessType": "B07",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YHR-HEP------M",
    "in_Domain": "10YBA-JPCC-----D",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 7.2: GB → BE (daily, 1 day)
📄 Response: 6.2 KB | **File:** `E07_v2_revenue_GB_BE_1day.xml`

```python
{
    "documentType": "A25",
    "businessType": "B07",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YGB----------A",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 7.3: HR → BA (daily, 7 days)
📄 Response: 10.1 KB | **File:** `E07_v3_revenue_HR_BA_7days.xml`

```python
{
    "documentType": "A25",
    "businessType": "B07",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YHR-HEP------M",
    "in_Domain": "10YBA-JPCC-----D",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 7.4: BA → HR (daily, 1 day)
📄 Response: 1.9 KB | **File:** `E07_v4_fix4_revenue_BA_HR_1day.xml`

```python
{
    "documentType": "A25",
    "businessType": "B07",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YBA-JPCC-----D",
    "in_Domain": "10YHR-HEP------M",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 8: Implicit Auction - Net Positions (12.1.E)

**Document Type:** `A25`  
**Business Type:** `B09`  
**Description:** Net import/export positions per bidding zone

### ✅ Variant 8.1: Belgium (intraday, 1 day)
📄 Response: 15.1 KB | **File:** `E08_v1_netpos_BE_1day.xml`

```python
{
    "documentType": "A25",
    "businessType": "B09",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YBE----------2",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 8.2: Austria (intraday, 1 day)
📄 Response: 7.3 KB | **File:** `E08_v2_fix1_netpos_AT_1day.xml`

```python
{
    "documentType": "A25",
    "businessType": "B09",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YAT-APG------L",
    "in_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 8.3: France (intraday, 7 days)
📄 Response: 28.5 KB | **File:** `E08_v3_netpos_FR_7days.xml`

```python
{
    "documentType": "A25",
    "businessType": "B09",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 8.4: Netherlands (intraday, Dec 2025)
📄 Response: 58.6 KB | **File:** `E08_v4_netpos_NL_dec2025.xml`

```python
{
    "documentType": "A25",
    "businessType": "B09",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YNL----------L",
    "in_Domain": "10YNL----------L",
    "periodStart": "202512010000",
    "periodEnd": "202512070000"
}
```

---

## 📋 Endpoint 9: Continuous Allocations - Offered Transfer Capacity (11.1)

**Document Type:** `A31`  
**Auction Type:** `A08` (continuous)  
**Description:** Transfer capacity for continuous intraday markets

### ✅ Variant 9.1: BE → NL (1 day)
📄 Response: 19.1 KB | **File:** `E09_v1_continuous_BE_NL_1day.xml`

```python
{
    "DocumentType": "A31",
    "Auction.Type": "A08",
    "Out_Domain": "10YBE----------2",
    "In_Domain": "10YNL----------L",
    "Contract_MarketAgreement.Type": "A07",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 9.2: NL → BE (1 day) - Reverse Direction
📄 Response: 14.9 KB | **File:** `E09_v2_continuous_NL_BE_1day.xml`

```python
{
    "DocumentType": "A31",
    "Auction.Type": "A08",
    "Out_Domain": "10YNL----------L",
    "In_Domain": "10YBE----------2",
    "Contract_MarketAgreement.Type": "A07",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 9.3: DE → NL (7 days)
📄 Response: 69.5 KB | **File:** `E09_v3_continuous_DE_NL_7days.xml`

```python
{
    "DocumentType": "A31",
    "Auction.Type": "A08",
    "Out_Domain": "10Y1001A1001A82H",
    "In_Domain": "10YNL----------L",
    "Contract_MarketAgreement.Type": "A07",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 9.4: FR → BE (Dec 2025)
📄 Response: 41.9 KB | **File:** `E09_v4_continuous_FR_BE_dec2025.xml`

```python
{
    "DocumentType": "A31",
    "Auction.Type": "A08",
    "Out_Domain": "10YFR-RTE------C",
    "In_Domain": "10YBE----------2",
    "Contract_MarketAgreement.Type": "A07",
    "periodStart": "202512010000",
    "periodEnd": "202512070000"
}
```

---

## 📋 Endpoint 10: Day-ahead Energy Prices (12.1.D)

**Document Type:** `A44`  
**Description:** Day-ahead and intraday energy prices per bidding zone

### ✅ Variant 10.1: Austria (1 day)
📄 Response: 55.0 KB | **File:** `E10_v1_prices_AT_1day.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YAT-APG------L",
    "in_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 10.2: Spain (1 day)
📄 Response: 92.7 KB | **File:** `E10_v2_prices_ES_1day.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YES-REE------0",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 10.3: Italy North (7 days)
📄 Response: 97.4 KB | **File:** `E10_v3_prices_IT_North_7days.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10Y1001A1001A73I",
    "in_Domain": "10Y1001A1001A73I",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 10.4: Poland (Dec 2025)
📄 Response: 93.3 KB | **File:** `E10_v4_prices_PL_dec2025.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YPL-AREA-----S",
    "in_Domain": "10YPL-AREA-----S",
    "periodStart": "202512010000",
    "periodEnd": "202512070000"
}
```

---

---

## 📋 Endpoint 11: Actual Total Load (6.1.A)

**Document Type:** `A65`  
**Process Type:** `A16` (Realised)  
**Description:** Actual total electricity load per bidding zone

### ✅ Variant 11.1: Czech Republic (1 day)
📄 Response: 11.0 KB | **File:** `E11_v1_load_CZ_1day.xml`

```python
{
    "documentType": "A65",
    "processType": "A16",
    "outBiddingZone_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 11.2: Germany-Luxembourg (1 day)
📄 Response: 10.9 KB | **File:** `E11_v2_load_DE_1day.xml`

```python
{
    "documentType": "A65",
    "processType": "A16",
    "outBiddingZone_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 11.3: France (1 day)
📄 Response: 11.0 KB | **File:** `E11_v3_load_FR_1day.xml`

```python
{
    "documentType": "A65",
    "processType": "A16",
    "outBiddingZone_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 11.4: Spain (1 day)
📄 Response: 10.9 KB | **File:** `E11_v4_load_ES_1day.xml`

```python
{
    "documentType": "A65",
    "processType": "A16",
    "outBiddingZone_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 12: Day-ahead Total Load Forecast (6.1.B)

**Document Type:** `A65`  
**Process Type:** `A01` (Day-ahead)  
**Description:** Day-ahead forecast of total electricity load

### ✅ Variant 12.1: Czech Republic (1 day)
📄 Response: 12.6 KB | **File:** `E12_v1_loadfc_CZ_1day.xml`

```python
{
    "documentType": "A65",
    "processType": "A01",
    "outBiddingZone_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 12.2: Germany-Luxembourg (1 day)
📄 Response: 13.3 KB | **File:** `E12_v2_loadfc_DE_1day.xml`

```python
{
    "documentType": "A65",
    "processType": "A01",
    "outBiddingZone_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 12.3: France (1 day)
📄 Response: 12.7 KB | **File:** `E12_v3_loadfc_FR_1day.xml`

```python
{
    "documentType": "A65",
    "processType": "A01",
    "outBiddingZone_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 12.4: Spain (1 day)
📄 Response: 12.6 KB | **File:** `E12_v4_loadfc_ES_1day.xml`

```python
{
    "documentType": "A65",
    "processType": "A01",
    "outBiddingZone_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 13: Week-ahead Total Load Forecast (6.1.C)

**Document Type:** `A65`  
**Process Type:** `A31` (Week-ahead)  
**Description:** Week-ahead forecast of total electricity load

### ✅ Variant 13.1: Czech Republic (7 days)
📄 Response: 4.1 KB | **File:** `E13_v1_loadwa_CZ_7days.xml`

```python
{
    "documentType": "A65",
    "processType": "A31",
    "outBiddingZone_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 13.2: Germany-Luxembourg (7 days)
📄 Response: 4.4 KB | **File:** `E13_v2_loadwa_DE_7days.xml`

```python
{
    "documentType": "A65",
    "processType": "A31",
    "outBiddingZone_Domain": "10Y1001A1001A82H",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 13.3: France (7 days)
📄 Response: 4.3 KB | **File:** `E13_v3_loadwa_FR_7days.xml`

```python
{
    "documentType": "A65",
    "processType": "A31",
    "outBiddingZone_Domain": "10YFR-RTE------C",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 13.4: Spain (7 days)
📄 Response: 4.3 KB | **File:** `E13_v4_loadwa_ES_7days.xml`

```python
{
    "documentType": "A65",
    "processType": "A31",
    "outBiddingZone_Domain": "10YES-REE------0",
    "periodStart": "202601012200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 14: Installed Capacity per Production Type (14.1.A)

**Document Type:** `A68`  
**Process Type:** `A33` (Year-ahead)  
**Description:** Installed generation capacity by fuel type

### ✅ Variant 14.1: Belgium
📄 Response: 10.4 KB | **File:** `E14_v1_instcap_BE.xml`

```python
{
    "documentType": "A68",
    "processType": "A33",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 14.2: Germany-Luxembourg
📄 Response: 16.8 KB | **File:** `E14_v2_instcap_DE.xml`

```python
{
    "documentType": "A68",
    "processType": "A33",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 14.3: Spain
📄 Response: 17.6 KB | **File:** `E14_v4_instcap_ES.xml`

```python
{
    "documentType": "A68",
    "processType": "A33",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 14.4: Netherlands
📄 Response: 16.7 KB | **File:** `E14_v6_instcap_NL.xml`

```python
{
    "documentType": "A68",
    "processType": "A33",
    "in_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 15: Year-ahead Total Load Forecast (6.1.E)

**Document Type:** `A65`  
**Process Type:** `A33` (Year-ahead)  
**Description:** Year-ahead forecast of total electricity load

> **Note:** Originally tested Water Reservoirs (16.1.D) but no data was available. Substituted with Year-ahead Load Forecast.

### ✅ Variant 15.1: Belgium
📄 Response: 2.3 KB | **File:** `E15_alt1_yearahead_BE.xml`

```python
{
    "documentType": "A65",
    "processType": "A33",
    "outBiddingZone_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 15.2: France
📄 Response: 2.3 KB | **File:** `E15_alt3_yearahead_FR.xml`

```python
{
    "documentType": "A65",
    "processType": "A33",
    "outBiddingZone_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 15.3: Spain
📄 Response: 2.3 KB | **File:** `E15_alt4_yearahead_ES.xml`

```python
{
    "documentType": "A65",
    "processType": "A33",
    "outBiddingZone_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 15.4: Italy
📄 Response: 2.3 KB | **File:** `E15_alt5_yearahead_IT.xml`

```python
{
    "documentType": "A65",
    "processType": "A33",
    "outBiddingZone_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 16: Actual Generation per Generation Unit (16.1.A)

**Document Type:** `A75`  
**Process Type:** `A16` (Realised)  
**Description:** Actual generation output per individual generation unit (≥100 MW)

### ✅ Variant 16.1: Germany 50Hertz Control Area (1 day)
📄 Response: 126.8 KB | **File:** `E16_v1_genunit_DE50Hz_1day.xml`

```python
{
    "documentType": "A73",
    "processType": "A16",
    "in_Domain": "10YDE-VE-------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 16.2: Germany Amprion Control Area (1 day)
📄 Response: 85.1 KB | **File:** `E16_v2_genunit_DEAmprion_1day.xml`

```python
{
    "documentType": "A73",
    "processType": "A16",
    "in_Domain": "10YDE-RWENET---I",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 16.3: Germany TenneT Control Area (1 day)
📄 Response: 105.7 KB | **File:** `E16_v3_genunit_DETenneT_1day.xml`

```python
{
    "documentType": "A73",
    "processType": "A16",
    "in_Domain": "10YDE-EON------1",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 16.4: Germany TransnetBW Control Area (1 day)
📄 Response: 101.4 KB | **File:** `E16_v4_genunit_DETransnet_1day.xml`

```python
{
    "documentType": "A73",
    "processType": "A16",
    "in_Domain": "10YDE-ENBW-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 17: Actual Generation per Production Type (16.1.B&C)

**Document Type:** `A75`  
**Process Type:** `A16` (Realised)  
**Description:** Aggregated actual generation per fuel/technology type

### ✅ Variant 17.1: Belgium (1 day)
📄 Response: 34.7 KB | **File:** `E17_v1_gentype_BE_1day.xml`

```python
{
    "documentType": "A75",
    "processType": "A16",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 17.2: Germany-Luxembourg (1 day)
📄 Response: 155.5 KB | **File:** `E17_v2_gentype_DE_1day.xml`

```python
{
    "documentType": "A75",
    "processType": "A16",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 17.3: France (1 day)
📄 Response: 156.6 KB | **File:** `E17_v3_gentype_FR_1day.xml`

```python
{
    "documentType": "A75",
    "processType": "A16",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 17.4: Spain (1 day)
📄 Response: 96.1 KB | **File:** `E17_v4_gentype_ES_1day.xml`

```python
{
    "documentType": "A75",
    "processType": "A16",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200",
    "psrType": "B12"
}
```

### ✅ Variant 17.5: Italy North (wind onshore)
📄 Response: Sample | **File:** `E17_v5_gentype_ITN_wind_onshore.xml`

```python
{
    "documentType": "A75",
    "processType": "A16",
    "in_Domain": "10Y1001A1001A73I",
    "periodStart": "202601072200",
    "periodEnd": "202601082200",
    "psrType": "B19"
}
```

---

## 📋 Endpoint 18: Generation Forecast - Day Ahead (14.1.C)

**Document Type:** `A71`  
**Process Type:** `A01` (Day-ahead) 
**Description:** Day-ahead scheduled generation forecast

### ✅ Variant 18.1: Belgium (1 day)
📄 Response: 6.1 KB | **File:** `E18_v1_genfc_BE_1day.xml`

```python
{
    "documentType": "A71",
    "processType": "A01",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 18.2: Germany-Luxembourg (1 day)
📄 Response: 19.9 KB | **File:** `E18_v2_genfc_DE_1day.xml`

```python
{
    "documentType": "A71",
    "processType": "A01",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 18.3: France (1 day)
📄 Response: 19.2 KB | **File:** `E18_v3_genfc_FR_1day.xml`

```python
{
    "documentType": "A71",
    "processType": "A01",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 18.4: Spain (1 day)
📄 Response: 27.0 KB | **File:** `E18_v4_genfc_ES_1day.xml`

```python
{
    "documentType": "A71",
    "processType": "A01",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 19: Wind and Solar Forecast (14.1.D)

**Document Type:** `A69`  
**Process Type:** `A01` (Day-ahead) / `A40` (Intraday) / `A18` (Current)  
**Description:** Day-ahead wind and solar generation forecast

### ✅ Variant 19.1: Belgium (1 day)
📄 Response: 11.2 KB | **File:** `E19_v1_windsolar_BE_1day.xml`

```python
{
    "documentType": "A69",
    "processType": "A01",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 19.2: Germany-Luxembourg (1 day)
📄 Response: 36.0 KB | **File:** `E19_v2_windsolar_DE_1day.xml`

```python
{
    "documentType": "A69",
    "processType": "A01",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 19.3: France (1 day)
📄 Response: 11.4 KB | **File:** `E19_v3_windsolar_FR_1day.xml`

```python
{
    "documentType": "A69",
    "processType": "A01",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 19.4: Spain (1 day)
📄 Response: 27.3 KB | **File:** `E19_v4_windsolar_ES_1day.xml`

```python
{
    "documentType": "A69",
    "processType": "A01",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 20: Cross-Border Physical Flows (12.1.G)

**Document Type:** `A11`  
**Description:** Actual physical power flows between bidding zones

### ✅ Variant 20.1: Germany → Belgium (1 day)
📄 Response: 2.9 KB | **File:** `E20_v1_flows_DE_BE_1day.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YDE-RWENET---I",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 20.2: France → Germany (1 day)
📄 Response: 11.2 KB | **File:** `E20_v2_flows_FR_DE_1day.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 20.3: France → Spain (1 day)
📄 Response: 2.1 KB | **File:** `E20_v3_flows_FR_ES_1day.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 20.4: Italy → France (1 day)
📄 Response: 1.5 KB | **File:** `E20_v4_flows_IT_FR_1day.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YIT-GRTN-----B",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 21: Forecasted Transfer Capacities (11.1.A)

**Document Type:** `A61`  
**Description:** Net Transfer Capacity (NTC) forecasts per border

### ✅ Variant 21.1: GB → Belgium (daily, 1 day)
📄 Response: 1.5 KB | **File:** `E21_v1_ntc_GB_BE_1day.xml`

```python
{
    "documentType": "A61",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YGB----------A",
    "in_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 21.2: France → Spain (daily, 1 day)
📄 Response: 2.2 KB | **File:** `E21_v2_ntc_FR_ES_1day.xml`

```python
{
    "documentType": "A61",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 21.3: Austria → Italy (daily, 1 day)
📄 Response: 2.9 KB | **File:** `E21_v3_ntc_AT_IT_1day.xml`

```python
{
    "documentType": "A61",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YAT-APG------L",
    "in_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 21.4: Germany → Netherlands (daily, 1 day)
📄 Response: 1.7 KB | **File:** `E21_v4_ntc_DE_NL_1day.xml`

```python
{
    "documentType": "A61",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10Y1001A1001A82H",
    "in_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 22: Commercial Schedules (12.1.F)

**Document Type:** `A09`  
**Description:** Scheduled commercial exchanges between bidding zones

### ✅ Variant 22.1: Belgium → France (1 day)
📄 Response: 16.6 KB | **File:** `E22_v1_sched_BE_FR_1day.xml`

```python
{
    "documentType": "A09",
    "out_Domain": "10YBE----------2",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 22.2: France → Germany (1 day)
📄 Response: 28.7 KB | **File:** `E22_v2_sched_FR_DE_1day.xml`

```python
{
    "documentType": "A09",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 22.3: Germany → Austria (1 day)
📄 Response: 30.9 KB | **File:** `E22_v3_sched_DE_AT_1day.xml`

```python
{
    "documentType": "A09",
    "out_Domain": "10Y1001A1001A82H",
    "in_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 22.4: Spain → Portugal (1 day)
📄 Response: 27.5 KB | **File:** `E22_v4_sched_ES_PT_1day.xml`

```python
{
    "documentType": "A09",
    "out_Domain": "10YES-REE------0",
    "in_Domain": "10YPT-REN------W",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 23: DC Link / Intraday Nominated Capacity (11.3 / 12.1.B)

**Description:** DC Link transfer limits or Intraday nominated capacity

> **Note:** DC Link data (A93) is sparse. Variants include both DC Link and Intraday Nominated Capacity (A26 with contract_MarketAgreement.Type A07).

### ✅ Variant 23.1: ElecLink → France (DC Link, 1 day)
📄 Response: 3.5 KB | **File:** `E23_v1_dc_ElecLink_FR_1day.xml`

```python
{
    "documentType": "A93",
    "out_Domain": "11Y0-0000-0265-K",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 23.2: France → ElecLink (DC Link, 1 day)
📄 Response: 2.0 KB | **File:** `E23_fix7_dc_FR_ElecLink.xml`

```python
{
    "documentType": "A93",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "11Y0-0000-0265-K",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 23.3: France → Spain (Intraday Nominated, 1 day)
📄 Response: 2.9 KB | **File:** `E23_alt1_intranominated_FR_ES.xml`

```python
{
    "documentType": "A26",
    "businessType": "B08",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 23.4: Austria → Italy (Intraday Nominated, 1 day)
📄 Response: 2.9 KB | **File:** `E23_alt2_intranominated_AT_IT.xml`

```python
{
    "documentType": "A26",
    "businessType": "B08",
    "contract_MarketAgreement.Type": "A07",
    "out_Domain": "10YAT-APG------L",
    "in_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 24: Unavailability of Generation Units (15.1.A&B)

**Document Type:** `A80`  
**Description:** Planned and forced outages of generation units

### ✅ Variant 24.1: Belgium (1 day)
📄 Response: 30.3 KB | **File:** `E24_v1_genout_BE_1day.xml`

```python
{
    "documentType": "A80",
    "BiddingZone_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 24.2: Germany-Luxembourg (1 day)
📄 Response: 77.7 KB | **File:** `E24_v2_genout_DE_1day.xml`

```python
{
    "documentType": "A80",
    "BiddingZone_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 24.3: France (1 day)
📄 Response: 52.5 KB | **File:** `E24_v3_genout_FR_1day.xml`

```python
{
    "documentType": "A80",
    "BiddingZone_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 24.4: Spain (1 day)
📄 Response: 38.6 KB | **File:** `E24_v4_genout_ES_1day.xml`

```python
{
    "documentType": "A80",
    "BiddingZone_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 25: Unavailability of Transmission Infrastructure (10.1.A&B)

**Document Type:** `A78`  
**Description:** Planned and forced outages of transmission lines

### ✅ Variant 25.1: France → Belgium (1 day)
📄 Response: 2.8 KB | **File:** `E25_v1_transout_FR_BE_1day.xml`

```python
{
    "documentType": "A78",
    "Out_Domain": "10YFR-RTE------C",
    "In_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 25.2: Germany → France (1 day)
📄 Response: 0.9 KB | **File:** `E25_v2_transout_DE_FR_1day.xml`

```python
{
    "documentType": "A78",
    "Out_Domain": "10Y1001A1001A82H",
    "In_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 25.3: France → Spain (1 day)
📄 Response: 1.1 KB | **File:** `E25_v3_transout_FR_ES_1day.xml`

```python
{
    "documentType": "A78",
    "Out_Domain": "10YFR-RTE------C",
    "In_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 25.4: Austria → Italy (1 day)
📄 Response: 6.7 KB | **File:** `E25_v4_transout_AT_IT_1day.xml`

```python
{
    "documentType": "A78",
    "Out_Domain": "10YAT-APG------L",
    "In_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 26: Imbalance Prices (17.1.G)

**Document Type:** `A85`  
**Description:** Settlement prices for imbalances

### ✅ Variant 26.1: Netherlands (1 day)
📄 Response: 0.8 KB | **File:** `E26_v1_imbprice_NL_1day.xml`

```python
{
    "documentType": "A85",
    "controlArea_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 26.2: Belgium (1 day)
📄 Response: 2.2 KB | **File:** `E26_v2_imbprice_BE_1day.xml`

```python
{
    "documentType": "A85",
    "controlArea_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 26.3: Austria (1 day)
📄 Response: 1.9 KB | **File:** `E26_v3_imbprice_AT_1day.xml`

```python
{
    "documentType": "A85",
    "controlArea_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 26.4: France (1 day)
📄 Response: 2.0 KB | **File:** `E26_v4_imbprice_FR_1day.xml`

```python
{
    "documentType": "A85",
    "controlArea_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 27: Total Imbalance Volumes (17.1.H)

**Document Type:** `A86`  
**Description:** Total system imbalance volumes

### ✅ Variant 27.1: Belgium (1 day)
📄 Response: 1.8 KB | **File:** `E27_v1_imbvol_BE_1day.xml`

```python
{
    "documentType": "A86",
    "controlArea_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 27.2: Austria (1 day)
📄 Response: 1.9 KB | **File:** `E27_v3_imbvol_AT_1day.xml`

```python
{
    "documentType": "A86",
    "controlArea_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 27.3: France (1 day)
📄 Response: 1.5 KB | **File:** `E27_v4_imbvol_FR_1day.xml`

```python
{
    "documentType": "A86",
    "controlArea_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 27.4: Spain (1 day)
📄 Response: 2.6 KB | **File:** `E27_v5_imbvol_ES_1day.xml`

```python
{
    "documentType": "A86",
    "controlArea_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 28: Current Balancing State / ACE (12.3.A)

**Document Type:** `A86`  
**Business Type:** `B33`  
**Description:** Area Control Error (ACE) - system frequency deviation

### ✅ Variant 28.1: Belgium (1 day)
📄 Response: 208.7 KB | **File:** `E28_v1_ace_BE_1day.xml`

```python
{
    "documentType": "A86",
    "businessType": "B33",
    "Area_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 28.2: Netherlands (1 day)
📄 Response: 280.5 KB | **File:** `E28_v2_ace_NL_1day.xml`

```python
{
    "documentType": "A86",
    "businessType": "B33",
    "Area_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 28.3: Austria (1 day)
📄 Response: 188.1 KB | **File:** `E28_v3_ace_AT_1day.xml`

```python
{
    "documentType": "A86",
    "businessType": "B33",
    "Area_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 28.4: France (1 day)
📄 Response: 18.5 KB | **File:** `E28_v4_ace_FR_1day.xml`

```python
{
    "documentType": "A86",
    "businessType": "B33",
    "Area_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 29: FCR Total Capacity

**Document Type:** `A26`  
**Business Type:** `A25`  
**Description:** Frequency Containment Reserve total capacity

> **⚠️ DATA AVAILABILITY NOTE:** FCR Total Capacity data was not available for any tested zone/period combination when tested on 2026-01-08. The following requests returned "no data available" responses.

### ⚠️ Variant 29.1: Continental Europe (1 day)
**Status:** No Data | **File:** `E29_v1_fcr_CE_1day.xml`

```python
{
    "documentType": "A26",
    "businessType": "A25",
    "Area_Domain": "10YEU-CONT-SYNC0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ⚠️ Variant 29.2: Nordic (1 day)
**Status:** No Data | **File:** `E29_v2_fcr_Nordic_1day.xml`

```python
{
    "documentType": "A26",
    "businessType": "A25",
    "Area_Domain": "10Y1001A1001A70O",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ⚠️ Variant 29.3: Great Britain (1 day)
**Status:** No Data | **File:** `E29_v3_fcr_GB_1day.xml`

```python
{
    "documentType": "A26",
    "businessType": "A25",
    "Area_Domain": "10YGB----------A",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ⚠️ Variant 29.4: Germany-Luxembourg (day-ahead, 1 day)
**Status:** No Data | **File:** `E29_fix1_fcr_DE_A01.xml`

```python
{
    "documentType": "A26",
    "businessType": "A25",
    "Area_Domain": "10Y1001A1001A82H",
    "processType": "A01",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 30: Prices of Activated Balancing Energy (17.1.F)

**Document Type:** `A84`  
**Process Type:** `A16` (Realised)  
**Description:** Prices of activated balancing energy (aFRR, mFRR, RR)

### ✅ Variant 30.1: Austria aFRR (1 day)
📄 Response: 42.6 KB | **File:** `E30_v3_actprice_AT_aFRR.xml`

```python
{
    "documentType": "A84",
    "processType": "A16",
    "controlArea_Domain": "10YAT-APG------L",
    "businessType": "A96",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 30.2: Austria mFRR (1 day)
📄 Response: 17.6 KB | **File:** `E30_fix1_actprice_AT_mFRR.xml`

```python
{
    "documentType": "A84",
    "processType": "A16",
    "controlArea_Domain": "10YAT-APG------L",
    "businessType": "A97",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 30.3: France mFRR (1 day)
📄 Response: 6.0 KB | **File:** `E30_fix3_actprice_FR_mFRR.xml`

```python
{
    "documentType": "A84",
    "processType": "A16",
    "controlArea_Domain": "10YFR-RTE------C",
    "businessType": "A97",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

### ✅ Variant 30.4: France RR (Replacement Reserve, 1 day)
📄 Response: 8.1 KB | **File:** `E30_fix6_actprice_FR_RR.xml`

```python
{
    "documentType": "A84",
    "processType": "A16",
    "controlArea_Domain": "10YFR-RTE------C",
    "businessType": "A98",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📈 Endpoint Success Rates

| Endpoint | Description | ✅ Success | ⚠️ No Data | ❌ Failed |
|----------|-------------|-----------|------------|----------|
| E01 | Total Nominated Capacity | 4/4 | 0/4 | 0/4 |
| E02 | Implicit Allocations OTC | 4/4 | 0/4 | 0/4 |
| E03 | Third Countries | 4/4 | 0/4 | 0/4 |
| E04 | Allocated Capacity | 4/4 | 0/4 | 0/4 |
| E05 | Explicit OTC | 4/4 | 0/4 | 0/4 |
| E06 | Explicit Use | 4/4 | 0/4 | 0/4 |
| E07 | Auction Revenue | 4/4 | 0/4 | 0/4 |
| E08 | Net Positions | 4/4 | 0/4 | 0/4 |
| E09 | Continuous OTC | 4/4 | 0/4 | 0/4 |
| E10 | Day-ahead Prices | 4/4 | 0/4 | 0/4 |
| E11 | Actual Total Load | 4/4 | 0/4 | 0/4 |
| E12 | Day-ahead Load Forecast | 4/4 | 0/4 | 0/4 |
| E13 | Week-ahead Load Forecast | 4/4 | 0/4 | 0/4 |
| E14 | Installed Capacity | 4/4 | 0/4 | 0/4 |
| E15 | Year-ahead Load Forecast | 4/4 | 0/4 | 0/4 |
| E16 | Generation per Unit | 4/4 | 0/4 | 0/4 |
| E17 | Generation per Type | 4/4 | 0/4 | 0/4 |
| E18 | Generation Forecast DA | 4/4 | 0/4 | 0/4 |
| E19 | Wind/Solar Forecast | 4/4 | 0/4 | 0/4 |
| E20 | Physical Flows | 4/4 | 0/4 | 0/4 |
| E21 | NTC Forecast | 4/4 | 0/4 | 0/4 |
| E22 | Commercial Schedules | 4/4 | 0/4 | 0/4 |
| E23 | DC Link / Intraday Nominated | 4/4 | 0/4 | 0/4 |
| E24 | Generation Outages | 4/4 | 0/4 | 0/4 |
| E25 | Transmission Outages | 4/4 | 0/4 | 0/4 |
| E26 | Imbalance Prices | 4/4 | 0/4 | 0/4 |
| E27 | Imbalance Volumes | 4/4 | 0/4 | 0/4 |
| E28 | ACE (Balancing State) | 4/4 | 0/4 | 0/4 |
| E29 | FCR Total Capacity | 0/4 | 4/4 | 0/4 |
| E30 | Activated Energy Prices | 4/4 | 0/4 | 0/4 |
| E31 | Net Position (Schedules) | 0/4 | 4/4 | 0/4 |
| E32 | Congestion Mgmt Costs | 0/4 | 4/4 | 0/4 |
| E33 | Redispatching Internal | 0/4 | 4/4 | 0/4 |
| E34 | Redispatching Cross-Border | 0/4 | 4/4 | 0/4 |
| E35 | Expansion Projects | 0/4 | 4/4 | 0/4 |
| E36 | Countertrading | 0/4 | 4/4 | 0/4 |
| E37 | Production Units Outages | 4/4 | 0/4 | 0/4 |
| E38 | Consumption Units Outages | 0/4 | 4/4 | 0/4 |
| E39 | Trans Outages (Control Area) | 0/4 | 4/4 | 0/4 |
| E40 | Offshore Grid Outages | 0/4 | 4/4 | 0/4 |
| E41 | CBMPs aFRR | 4/4 | 0/4 | 0/4 |
| E42 | Balancing Energy Bids | 0/4 | 4/4 | 0/4 |
| E43 | Aggregated Bids | 4/4 | 0/4 | 0/4 |
| E44 | Contracted Reserves | 0/4 | 4/4 | 0/4 |
| E45 | Procured Capacity | 0/4 | 4/4 | 0/4 |
| E46 | DA Prices (Central Europe) | 4/4 | 0/4 | 0/4 |
| E47 | DA Prices (Nordic/Balkan) | 4/4 | 0/4 | 0/4 |
| E48 | Imbalance Prices (Additional) | 4/4 | 0/4 | 0/4 |
| E49 | Physical Flows (Additional) | 4/4 | 0/4 | 0/4 |
| E50 | Congestion Income | 0/4 | 4/4 | 0/4 |
| E51 | Actual Load (Additional) | 4/4 | 0/4 | 0/4 |
| E52 | Gen by Type (Additional) | 4/4 | 0/4 | 0/4 |
| E53 | Wind/Solar (Additional) | 4/4 | 0/4 | 0/4 |
| E54 | NTC Forecast (Additional) | 4/4 | 0/4 | 0/4 |
| E55 | Imbalance Vol (Additional) | 4/4 | 0/4 | 0/4 |
| E56 | DA Prices (Italian Zones) | 4/4 | 0/4 | 0/4 |
| E57 | DA Prices (Nordic Zones) | 4/4 | 0/4 | 0/4 |
| E58 | DA Prices (Baltic/Eastern) | 4/4 | 0/4 | 0/4 |
| E59 | Physical Flows (Nordic) | 4/4 | 0/4 | 0/4 |
| E60 | Physical Flows (Eastern) | 4/4 | 0/4 | 0/4 |
| E61 | Installed Cap (Additional) | 4/4 | 0/4 | 0/4 |
| E62 | Gen Outages (Additional) | 4/4 | 0/4 | 0/4 |
| E63 | Trans Outages (Additional) | 4/4 | 0/4 | 0/4 |
| E64 | ACE (Additional) | 4/4 | 0/4 | 0/4 |
| E65 | Activated Prices (Additional) | 4/4 | 0/4 | 0/4 |
| **Total (E01-E65)** | | **204/260** | **56/260** | **0/260** |

---

## 📋 Endpoint 31: Net Position via Commercial Schedules (12.1.F)

**Document Type:** `A09` (same in/out domain)  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 31.1: Austria
```python
{"documentType": "A09", "out_Domain": "10YAT-APG------L", "in_Domain": "10YAT-APG------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 31.2: Belgium
```python
{"documentType": "A09", "out_Domain": "10YBE----------2", "in_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 31.3: Germany-Luxembourg
```python
{"documentType": "A09", "out_Domain": "10Y1001A1001A82H", "in_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 31.4: France
```python
{"documentType": "A09", "out_Domain": "10YFR-RTE------C", "in_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 32: Congestion Management Costs (13.1.C)

**Document Type:** `A92`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 32.1: Belgium
```python
{"documentType": "A92", "out_Domain": "10YBE----------2", "in_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 32.2: Germany-Luxembourg
```python
{"documentType": "A92", "out_Domain": "10Y1001A1001A82H", "in_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 32.3: France
```python
{"documentType": "A92", "out_Domain": "10YFR-RTE------C", "in_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 32.4: Netherlands
```python
{"documentType": "A92", "out_Domain": "10YNL----------L", "in_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 33: Redispatching - Internal (13.1.A)

**Document Type:** `A63` | **Business Type:** `A85`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 33.1: Netherlands
```python
{"documentType": "A63", "businessType": "A85", "out_Domain": "10YNL----------L", "in_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 33.2: Belgium
```python
{"documentType": "A63", "businessType": "A85", "out_Domain": "10YBE----------2", "in_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 33.3: Germany-Luxembourg
```python
{"documentType": "A63", "businessType": "A85", "out_Domain": "10Y1001A1001A82H", "in_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 33.4: France
```python
{"documentType": "A63", "businessType": "A85", "out_Domain": "10YFR-RTE------C", "in_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 34: Redispatching - Cross Border (13.1.A)

**Document Type:** `A63` | **Business Type:** `A46`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 34.1: Austria → France
```python
{"documentType": "A63", "businessType": "A46", "out_Domain": "10YAT-APG------L", "in_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 34.2: Germany → France
```python
{"documentType": "A63", "businessType": "A46", "out_Domain": "10Y1001A1001A82H", "in_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 34.3: Germany → Netherlands
```python
{"documentType": "A63", "businessType": "A46", "out_Domain": "10Y1001A1001A82H", "in_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 34.4: France → Belgium
```python
{"documentType": "A63", "businessType": "A46", "out_Domain": "10YFR-RTE------C", "in_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 35: Expansion and Dismantling Projects (9.1)

**Document Type:** `A90`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 35.1: Hungary → Slovakia
```python
{"documentType": "A90", "out_Domain": "10YHU-MAVIR----U", "in_Domain": "10YSK-SEPS-----K", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 35.2: Austria → Germany
```python
{"documentType": "A90", "out_Domain": "10YAT-APG------L", "in_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 35.3: Germany → Netherlands
```python
{"documentType": "A90", "out_Domain": "10Y1001A1001A82H", "in_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 35.4: France → Spain
```python
{"documentType": "A90", "out_Domain": "10YFR-RTE------C", "in_Domain": "10YES-REE------0", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 36: Countertrading (13.1.B)

**Document Type:** `A91`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 36.1: Spain → France
```python
{"documentType": "A91", "out_Domain": "10YES-REE------0", "in_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 36.2: Germany → France
```python
{"documentType": "A91", "out_Domain": "10Y1001A1001A82H", "in_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 36.3: Austria → Italy
```python
{"documentType": "A91", "out_Domain": "10YAT-APG------L", "in_Domain": "10YIT-GRTN-----B", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 36.4: Germany → Netherlands
```python
{"documentType": "A91", "out_Domain": "10Y1001A1001A82H", "in_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 37: Unavailability of Production Units (15.1.C-D)

**Document Type:** `A77`  
**Description:** Planned/forced unavailability of production units

### ✅ Variant 37.1: France (1 day)
📄 Response: 2.1 KB | **File:** `E37_v3_prodout_FR.xml`

```python
{
    "documentType": "A77",
    "BiddingZone_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 37.2: Spain (1 day)
📄 Response: 33.2 KB | **File:** `E37_v4_prodout_ES.xml`

```python
{
    "documentType": "A77",
    "BiddingZone_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 37.3: Netherlands (1 day)
📄 Response: 1.0 KB | **File:** `E37_v6_prodout_NL.xml`

```python
{
    "documentType": "A77",
    "BiddingZone_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 37.4: Austria (1 day)
📄 Response: 5.2 KB | **File:** `E37_fix1_prodout_AT.xml`

```python
{
    "documentType": "A77",
    "BiddingZone_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 38: Aggregated Unavailability of Consumption Units (7.1.A-B)

**Document Type:** `A76`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 38.1: Germany-Luxembourg
```python
{"documentType": "A76", "BiddingZone_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 38.2: France
```python
{"documentType": "A76", "BiddingZone_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 38.3: Belgium
```python
{"documentType": "A76", "BiddingZone_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 38.4: Netherlands
```python
{"documentType": "A76", "BiddingZone_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 39: Transmission Outages - Control Area (10.1.A&B)

**Document Type:** `A78` with `ControlArea_Domain`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 39.1: France
```python
{"documentType": "A78", "ControlArea_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 39.2: Germany-Luxembourg
```python
{"documentType": "A78", "ControlArea_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 39.3: Belgium
```python
{"documentType": "A78", "ControlArea_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 39.4: Netherlands
```python
{"documentType": "A78", "ControlArea_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 40: Offshore Grid Infrastructure Unavailability (10.1.C)

**Document Type:** `A79`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 40.1: Germany-Luxembourg
```python
{"documentType": "A79", "BiddingZone_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 40.2: Netherlands
```python
{"documentType": "A79", "BiddingZone_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 40.3: Belgium
```python
{"documentType": "A79", "BiddingZone_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 40.4: Denmark DK1
```python
{"documentType": "A79", "BiddingZone_Domain": "10YDK-1--------W", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 41: Cross Border Marginal Prices (CBMPs) for aFRR

**Document Type:** `A84` | **Process Type:** `A67`  
**Description:** Cross-border marginal prices for automatic frequency restoration reserve

### ✅ Variant 41.1: Germany 50Hertz (1 day)
📄 Response: 3439.0 KB | **File:** `E41_v1_cbmp_DE50Hz.xml`

```python
{
    "documentType": "A84",
    "processType": "A67",
    "businessType": "A96",
    "Standard_MarketProduct": "A01",
    "controlArea_Domain": "10YDE-VE-------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 41.2: Germany TenneT (1 day)
📄 Response: 3439.0 KB | **File:** `E41_v3_cbmp_DETenneT.xml`

```python
{
    "documentType": "A84",
    "processType": "A67",
    "businessType": "A96",
    "Standard_MarketProduct": "A01",
    "controlArea_Domain": "10YDE-EON------1",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 41.3: Austria (1 day)
📄 Response: 3358.4 KB | **File:** `E41_v4_cbmp_AT.xml`

```python
{
    "documentType": "A84",
    "processType": "A67",
    "businessType": "A96",
    "Standard_MarketProduct": "A01",
    "controlArea_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 41.4: Netherlands (1 day)
📄 Response: 2586.6 KB | **File:** `E41_v5_cbmp_NL.xml`

```python
{
    "documentType": "A84",
    "processType": "A67",
    "businessType": "A96",
    "Standard_MarketProduct": "A01",
    "controlArea_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 42: Balancing Energy Bids (12.3.B&C)

**Document Type:** `A37` | **Business Type:** `B74`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 42.1: Czech Republic (mFRR)
```python
{"documentType": "A37", "businessType": "B74", "processType": "A47", "connecting_Domain": "10YCZ-CEPS-----N", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 42.2: Czech Republic (aFRR)
```python
{"documentType": "A37", "businessType": "B74", "processType": "A51", "connecting_Domain": "10YCZ-CEPS-----N", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 42.3: Germany-Luxembourg (mFRR)
```python
{"documentType": "A37", "businessType": "B74", "processType": "A47", "connecting_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 42.4: Austria (mFRR)
```python
{"documentType": "A37", "businessType": "B74", "processType": "A47", "connecting_Domain": "10YAT-APG------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 43: Aggregated Balancing Energy Bids (12.3.E)

**Document Type:** `A24`  
**Description:** Aggregated balancing energy bids

### ✅ Variant 43.1: Austria aFRR (1 day)
📄 Response: 34.9 KB | **File:** `E43_v3_aggbids_AT.xml`

```python
{
    "documentType": "A24",
    "processType": "A51",
    "Area_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 43.2: Belgium mFRR (1 day)
📄 Response: 34.9 KB | **File:** `E43_v6_aggbids_BE_mFRR.xml`

```python
{
    "documentType": "A24",
    "processType": "A47",
    "Area_Domain": "10YBE----------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 43.3: Austria mFRR (1 day)
📄 Response: 18.4 KB | **File:** `E43_fix1_aggbids_AT_mFRR.xml`

```python
{
    "documentType": "A24",
    "processType": "A47",
    "Area_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 43.4: France mFRR (1 day)
📄 Response: 31.2 KB | **File:** `E43_fix2_aggbids_FR_mFRR.xml`

```python
{
    "documentType": "A24",
    "processType": "A47",
    "Area_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 44: Volumes and Prices of Contracted Reserves (17.1.B&C)

**Document Type:** `A81` | **Process Type:** `A52`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 44.1: Germany-Luxembourg
```python
{"documentType": "A81", "processType": "A52", "controlArea_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 44.2: Austria
```python
{"documentType": "A81", "processType": "A52", "controlArea_Domain": "10YAT-APG------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 44.3: France
```python
{"documentType": "A81", "processType": "A52", "controlArea_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 44.4: Netherlands
```python
{"documentType": "A81", "processType": "A52", "controlArea_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 45: Procured Balancing Capacity (12.3.F)

**Document Type:** `A82`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 45.1: Netherlands (aFRR)
```python
{"documentType": "A82", "processType": "A51", "controlArea_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 45.2: Austria (aFRR)
```python
{"documentType": "A82", "processType": "A51", "controlArea_Domain": "10YAT-APG------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 45.3: Germany-Luxembourg (aFRR)
```python
{"documentType": "A82", "processType": "A51", "controlArea_Domain": "10Y1001A1001A82H", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 45.4: Belgium (aFRR)
```python
{"documentType": "A82", "processType": "A51", "controlArea_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 46: Day-ahead Prices - Central European Countries

**Document Type:** `A44`  
**Description:** Day-ahead energy prices for additional countries

### ✅ Variant 46.1: Switzerland (1 day)
📄 Response: 8.8 KB | **File:** `E46_v1_prices_CH.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YCH-SWISSGRIDZ",
    "in_Domain": "10YCH-SWISSGRIDZ",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 46.2: Czech Republic (1 day)
📄 Response: 28.3 KB | **File:** `E46_v2_prices_CZ.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YCZ-CEPS-----N",
    "in_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 46.3: Denmark DK1 (1 day)
📄 Response: 28.2 KB | **File:** `E46_v3_prices_DK1.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YDK-1--------W",
    "in_Domain": "10YDK-1--------W",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 46.4: Sweden SE3 (1 day)
📄 Response: 27.9 KB | **File:** `E46_v4_prices_SE3.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10Y1001A1001A46L",
    "in_Domain": "10Y1001A1001A46L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 47: Day-ahead Prices - Nordic and Balkan Countries

**Document Type:** `A44`  
**Description:** Day-ahead energy prices for Nordic and Balkan regions

### ✅ Variant 47.1: Norway NO1 (1 day)
📄 Response: 27.8 KB | **File:** `E47_v1_prices_NO1.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YNO-1--------2",
    "in_Domain": "10YNO-1--------2",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 47.2: Norway NO2 (1 day)
📄 Response: 28.1 KB | **File:** `E47_v2_prices_NO2.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YNO-2--------T",
    "in_Domain": "10YNO-2--------T",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 47.3: Greece (1 day)
📄 Response: 25.2 KB | **File:** `E47_v3_prices_GR.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YGR-HTSO-----Y",
    "in_Domain": "10YGR-HTSO-----Y",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 47.4: Romania (1 day)
📄 Response: 28.3 KB | **File:** `E47_v4_prices_RO.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YRO-TEL------P",
    "in_Domain": "10YRO-TEL------P",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 48: Imbalance Prices - Additional Countries (17.1.G)

**Document Type:** `A85`  
**Description:** Settlement prices for imbalances in additional countries

### ✅ Variant 48.1: Spain (1 day)
📄 Response: 2.6 KB | **File:** `E48_v2_imbprice_ES.xml`

```python
{
    "documentType": "A85",
    "controlArea_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 48.2: Czech Republic (1 day)
📄 Response: 2.4 KB | **File:** `E48_v4_imbprice_CZ.xml`

```python
{
    "documentType": "A85",
    "controlArea_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 48.3: Poland (1 day)
📄 Response: 2.7 KB | **File:** `E48_v5_imbprice_PL.xml`

```python
{
    "documentType": "A85",
    "controlArea_Domain": "10YPL-AREA-----S",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 48.4: Switzerland (1 day)
📄 Response: 1.8 KB | **File:** `E48_v6_imbprice_CH.xml`

```python
{
    "documentType": "A85",
    "controlArea_Domain": "10YCH-SWISSGRIDZ",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 49: Physical Flows - Additional Borders (12.1.G)

**Document Type:** `A11`  
**Description:** Actual physical power flows for additional borders

### ✅ Variant 49.1: Switzerland → Italy (1 day)
📄 Response: 2.6 KB | **File:** `E49_v1_flows_CH_IT.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YCH-SWISSGRIDZ",
    "in_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 49.2: Switzerland → Germany (1 day)
📄 Response: 7.6 KB | **File:** `E49_v2_flows_CH_DE.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YCH-SWISSGRIDZ",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 49.3: Switzerland → France (1 day)
📄 Response: 1.5 KB | **File:** `E49_v3_flows_CH_FR.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YCH-SWISSGRIDZ",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 49.4: Poland → Germany (1 day)
📄 Response: 1.5 KB | **File:** `E49_v4_flows_PL_DE.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YPL-AREA-----S",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 50: Congestion Income (12.1.E)

**Document Type:** `A25` | **Business Type:** `B10`  
**Status:** ⚠️ No data available - all 4 variants returned empty responses

### ⚠️ Variant 50.1: Belgium
```python
{"documentType": "A25", "businessType": "B10", "contract_MarketAgreement.Type": "A07", "out_Domain": "10YBE----------2", "in_Domain": "10YBE----------2", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 50.2: Netherlands
```python
{"documentType": "A25", "businessType": "B10", "contract_MarketAgreement.Type": "A07", "out_Domain": "10YNL----------L", "in_Domain": "10YNL----------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 50.3: Austria
```python
{"documentType": "A25", "businessType": "B10", "contract_MarketAgreement.Type": "A07", "out_Domain": "10YAT-APG------L", "in_Domain": "10YAT-APG------L", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

### ⚠️ Variant 50.4: France
```python
{"documentType": "A25", "businessType": "B10", "contract_MarketAgreement.Type": "A07", "out_Domain": "10YFR-RTE------C", "in_Domain": "10YFR-RTE------C", "periodStart": "202601072200", "periodEnd": "202601082200"}
```

---

## 📋 Endpoint 51: Actual Load - Additional Countries (6.1.A)

**Document Type:** `A65` | **Process Type:** `A16`  
**Description:** Actual total electricity load for additional European countries

### ✅ Variant 51.1: Portugal (1 day)
📄 Response: 3.8 KB | **File:** `E51_v1_load_PT.xml`

```python
{
    "documentType": "A65",
    "processType": "A16",
    "outBiddingZone_Domain": "10YPT-REN------W",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 51.2: Greece (1 day)
📄 Response: 11.0 KB | **File:** `E51_v2_load_GR.xml`

```python
{
    "documentType": "A65",
    "processType": "A16",
    "outBiddingZone_Domain": "10YGR-HTSO-----Y",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 51.3: Romania (1 day)
📄 Response: 11.2 KB | **File:** `E51_v3_load_RO.xml`

```python
{
    "documentType": "A65",
    "processType": "A16",
    "outBiddingZone_Domain": "10YRO-TEL------P",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 51.4: Hungary (1 day)
📄 Response: 11.4 KB | **File:** `E51_v4_load_HU.xml`

```python
{
    "documentType": "A65",
    "processType": "A16",
    "outBiddingZone_Domain": "10YHU-MAVIR----U",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 52: Actual Generation by Type - Additional (16.1.B&C)

**Document Type:** `A73` | **Process Type:** `A16`  
**Description:** Aggregated actual generation per fuel/technology type

### ✅ Variant 52.1: Austria (1 day)
📄 Response: 75.1 KB | **File:** `E52_v1_gentype_AT.xml`

```python
{
    "documentType": "A73",
    "processType": "A16",
    "in_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200",
    "psrType": "B12"
}
```

### ✅ Variant 52.2: Netherlands (1 day)
📄 Response: 131.2 KB | **File:** `E52_v2_gentype_NL.xml`

```python
{
    "documentType": "A73",
    "processType": "A16",
    "in_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 52.3: Poland (1 day)
📄 Response: 135.9 KB | **File:** `E52_v3_gentype_PL.xml`

```python
{
    "documentType": "A73",
    "processType": "A16",
    "in_Domain": "10YPL-AREA-----S",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 52.4: Switzerland (1 day)
📄 Response: 18.8 KB | **File:** `E52_v4_gentype_CH.xml`

```python
{
    "documentType": "A73",
    "processType": "A16",
    "in_Domain": "10YCH-SWISSGRIDZ",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 53: Wind/Solar Forecast - Additional (14.1.D)

**Document Type:** `A69` | **Process Type:** `A01`  
**Description:** Day-ahead wind and solar generation forecast

### ✅ Variant 53.1: Austria (1 day)
📄 Response: 20.0 KB | **File:** `E53_v1_windsolar_AT.xml`

```python
{
    "documentType": "A69",
    "processType": "A01",
    "in_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 53.2: Netherlands (1 day)
📄 Response: 34.2 KB | **File:** `E53_v2_windsolar_NL.xml`

```python
{
    "documentType": "A69",
    "processType": "A01",
    "in_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 53.3: Poland (1 day)
📄 Response: 21.8 KB | **File:** `E53_v3_windsolar_PL.xml`

```python
{
    "documentType": "A69",
    "processType": "A01",
    "in_Domain": "10YPL-AREA-----S",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 53.4: Denmark DK1 (1 day)
📄 Response: 34.7 KB | **File:** `E53_v4_windsolar_DK1.xml`

```python
{
    "documentType": "A69",
    "processType": "A01",
    "in_Domain": "10YDK-1--------W",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 54: NTC Forecast - Additional Borders (11.1.A)

**Document Type:** `A61` | **Contract Type:** `A01` (daily)  
**Description:** Net Transfer Capacity forecasts for additional borders

### ✅ Variant 54.1: Switzerland → Italy (1 day)
📄 Response: 2.9 KB | **File:** `E54_v1_ntc_CH_IT.xml`

```python
{
    "documentType": "A61",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YCH-SWISSGRIDZ",
    "in_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 54.2: Switzerland → Germany (1 day)
📄 Response: 3.8 KB | **File:** `E54_v2_ntc_CH_DE.xml`

```python
{
    "documentType": "A61",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YCH-SWISSGRIDZ",
    "in_Domain": "10Y1001A1001A82H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 54.3: Switzerland → France (1 day)
📄 Response: 3.2 KB | **File:** `E54_fix1_ntc_CH_FR.xml`

```python
{
    "documentType": "A61",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YCH-SWISSGRIDZ",
    "in_Domain": "10YFR-RTE------C",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 54.4: France → Switzerland (1 day)
📄 Response: 2.2 KB | **File:** `E54_fix2_ntc_FR_CH.xml`

```python
{
    "documentType": "A61",
    "contract_MarketAgreement.Type": "A01",
    "out_Domain": "10YFR-RTE------C",
    "in_Domain": "10YCH-SWISSGRIDZ",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 55: Imbalance Volumes - Additional (17.1.H)

**Document Type:** `A86`  
**Description:** Total system imbalance volumes

### ✅ Variant 55.1: Italy (1 day)
📄 Response: 2.7 KB | **File:** `E55_v1_imbvol_IT.xml`

```python
{
    "documentType": "A86",
    "controlArea_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 55.2: Czech Republic (1 day)
📄 Response: 1.2 KB | **File:** `E55_v2_imbvol_CZ.xml`

```python
{
    "documentType": "A86",
    "controlArea_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 55.3: Poland (1 day)
📄 Response: 2.8 KB | **File:** `E55_v3_imbvol_PL.xml`

```python
{
    "documentType": "A86",
    "controlArea_Domain": "10YPL-AREA-----S",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 55.4: Hungary (1 day)
📄 Response: 1.5 KB | **File:** `E55_v4_imbvol_HU.xml`

```python
{
    "documentType": "A86",
    "controlArea_Domain": "10YHU-MAVIR----U",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 56: Day-ahead Prices - Italian Zones (12.1.D)

**Document Type:** `A44`  
**Description:** Day-ahead energy prices for Italian and neighboring zones

### ✅ Variant 56.1: Italy North (1 day)
📄 Response: 26.4 KB | **File:** `E56_v1_prices_IT_North.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10Y1001A1001A73I",
    "in_Domain": "10Y1001A1001A73I",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 56.2: Italy South (1 day)
📄 Response: 23.5 KB | **File:** `E56_v2_prices_IT_South.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10Y1001A1001A788",
    "in_Domain": "10Y1001A1001A788",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 56.3: Slovenia (1 day)
📄 Response: 28.3 KB | **File:** `E56_v4_prices_SI.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YSI-ELES-----O",
    "in_Domain": "10YSI-ELES-----O",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 56.4: Croatia (1 day)
📄 Response: 28.3 KB | **File:** `E56_v5_prices_HR.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YHR-HEP------M",
    "in_Domain": "10YHR-HEP------M",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 57: Day-ahead Prices - Nordic Zones (12.1.D)

**Document Type:** `A44`  
**Description:** Day-ahead energy prices for Nordic bidding zones

### ✅ Variant 57.1: Norway NO3 (1 day)
📄 Response: 28.1 KB | **File:** `E57_v1_prices_NO3.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YNO-3--------J",
    "in_Domain": "10YNO-3--------J",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 57.2: Norway NO4 (1 day)
📄 Response: 25.7 KB | **File:** `E57_v2_prices_NO4.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YNO-4--------9",
    "in_Domain": "10YNO-4--------9",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 57.3: Norway NO5 (1 day)
📄 Response: 28.2 KB | **File:** `E57_v3_prices_NO5.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10Y1001A1001A48H",
    "in_Domain": "10Y1001A1001A48H",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 57.4: Sweden SE1 (1 day)
📄 Response: 28.2 KB | **File:** `E57_v4_prices_SE1.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10Y1001A1001A44P",
    "in_Domain": "10Y1001A1001A44P",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 58: Day-ahead Prices - Baltic & Eastern (12.1.D)

**Document Type:** `A44`  
**Description:** Day-ahead energy prices for Baltic states and Eastern Europe

### ✅ Variant 58.1: Estonia (1 day)
📄 Response: 27.3 KB | **File:** `E58_v1_prices_EE.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10Y1001A1001A39I",
    "in_Domain": "10Y1001A1001A39I",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 58.2: Latvia (1 day)
📄 Response: 27.3 KB | **File:** `E58_v2_prices_LV.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YLV-1001A00074",
    "in_Domain": "10YLV-1001A00074",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 58.3: Lithuania (1 day)
📄 Response: 27.3 KB | **File:** `E58_v3_prices_LT.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YLT-1001A0008Q",
    "in_Domain": "10YLT-1001A0008Q",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 58.4: Finland (1 day)
📄 Response: 27.5 KB | **File:** `E58_v4_prices_FI.xml`

```python
{
    "documentType": "A44",
    "out_Domain": "10YFI-1--------U",
    "in_Domain": "10YFI-1--------U",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 59: Physical Flows - Nordic Borders (12.1.G)

**Document Type:** `A11`  
**Description:** Actual physical power flows between Nordic countries

### ✅ Variant 59.1: Norway NO1 → Sweden SE3 (1 day)
📄 Response: 8.7 KB | **File:** `E59_v1_flows_NO1_SE3.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YNO-1--------2",
    "in_Domain": "10Y1001A1001A46L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 59.2: Sweden SE3 → Finland (1 day)
📄 Response: 11.0 KB | **File:** `E59_v2_flows_SE3_FI.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10Y1001A1001A46L",
    "in_Domain": "10YFI-1--------U",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 59.3: Denmark DK1 → Norway NO2 (1 day)
📄 Response: 4.2 KB | **File:** `E59_v3_flows_DK1_NO2.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YDK-1--------W",
    "in_Domain": "10YNO-2--------T",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 59.4: Denmark DK1 → Sweden SE3 (1 day)
📄 Response: 2.3 KB | **File:** `E59_v4_flows_DK1_SE3.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YDK-1--------W",
    "in_Domain": "10Y1001A1001A46L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 60: Physical Flows - Eastern Europe (12.1.G)

**Document Type:** `A11`  
**Description:** Actual physical power flows in Eastern Europe

### ✅ Variant 60.1: Poland → Czech Republic (1 day)
📄 Response: 9.3 KB | **File:** `E60_v1_flows_PL_CZ.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YPL-AREA-----S",
    "in_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 60.2: Czech Republic → Austria (1 day)
📄 Response: 11.2 KB | **File:** `E60_v2_flows_CZ_AT.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YCZ-CEPS-----N",
    "in_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 60.3: Austria → Hungary (1 day)
📄 Response: 11.2 KB | **File:** `E60_v3_flows_AT_HU.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YAT-APG------L",
    "in_Domain": "10YHU-MAVIR----U",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 60.4: Hungary → Slovakia (1 day)
📄 Response: 1.5 KB | **File:** `E60_v4_flows_HU_SK.xml`

```python
{
    "documentType": "A11",
    "out_Domain": "10YHU-MAVIR----U",
    "in_Domain": "10YSK-SEPS-----K",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 61: Installed Capacity - Additional (14.1.A)

**Document Type:** `A68` | **Process Type:** `A33`  
**Description:** Installed generation capacity by fuel type

### ✅ Variant 61.1: Poland (1 day)
📄 Response: 10.4 KB | **File:** `E61_v2_instcap_PL.xml`

```python
{
    "documentType": "A68",
    "processType": "A33",
    "in_Domain": "10YPL-AREA-----S",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 61.2: Czech Republic (1 day)
📄 Response: 12.8 KB | **File:** `E61_v3_instcap_CZ.xml`

```python
{
    "documentType": "A68",
    "processType": "A33",
    "in_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 61.3: Austria (1 day)
📄 Response: 17.5 KB | **File:** `E61_v4_instcap_AT.xml`

```python
{
    "documentType": "A68",
    "processType": "A33",
    "in_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 61.4: Switzerland (1 day)
📄 Response: 4.0 KB | **File:** `E61_v5_instcap_CH.xml`

```python
{
    "documentType": "A68",
    "processType": "A33",
    "in_Domain": "10YCH-SWISSGRIDZ",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 62: Generation Outages - Additional (15.1.A&B)

**Document Type:** `A80`  
**Description:** Planned and forced outages of generation units

### ✅ Variant 62.1: Italy (1 day)
📄 Response: 73.7 KB | **File:** `E62_v1_genout_IT.xml`

```python
{
    "documentType": "A80",
    "BiddingZone_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 62.2: Poland (1 day)
📄 Response: 45.8 KB | **File:** `E62_v2_genout_PL.xml`

```python
{
    "documentType": "A80",
    "BiddingZone_Domain": "10YPL-AREA-----S",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 62.3: Czech Republic (1 day)
📄 Response: 32.7 KB | **File:** `E62_v3_genout_CZ.xml`

```python
{
    "documentType": "A80",
    "BiddingZone_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 62.4: Austria (1 day)
📄 Response: 11.3 KB | **File:** `E62_v4_genout_AT.xml`

```python
{
    "documentType": "A80",
    "BiddingZone_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 63: Transmission Outages - Additional (10.1.A&B)

**Document Type:** `A78`  
**Description:** Planned and forced outages of transmission lines

### ✅ Variant 63.1: Germany → Poland (1 day)
📄 Response: 12.0 KB | **File:** `E63_v1_transout_DE_PL.xml`

```python
{
    "documentType": "A78",
    "Out_Domain": "10Y1001A1001A82H",
    "In_Domain": "10YPL-AREA-----S",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 63.2: Czech Republic → Austria (1 day)
📄 Response: 0.9 KB | **File:** `E63_v2_transout_CZ_AT.xml`

```python
{
    "documentType": "A78",
    "Out_Domain": "10YCZ-CEPS-----N",
    "In_Domain": "10YAT-APG------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 63.3: Switzerland → Italy (1 day)
📄 Response: 0.8 KB | **File:** `E63_v3_transout_CH_IT.xml`

```python
{
    "documentType": "A78",
    "Out_Domain": "10YCH-SWISSGRIDZ",
    "In_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 63.4: Belgium → Netherlands (1 day)
📄 Response: 1.9 KB | **File:** `E63_v5_transout_BE_NL.xml`

```python
{
    "documentType": "A78",
    "Out_Domain": "10YBE----------2",
    "In_Domain": "10YNL----------L",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 64: ACE (Area Control Error) - Additional (12.3.A)

**Document Type:** `A86` | **Business Type:** `B33`  
**Description:** Area Control Error - system frequency deviation

### ✅ Variant 64.1: Italy (1 day)
📄 Response: 175.4 KB | **File:** `E64_v1_ace_IT.xml`

```python
{
    "documentType": "A86",
    "businessType": "B33",
    "Area_Domain": "10YIT-GRTN-----B",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 64.2: Spain (1 day)
📄 Response: 197.5 KB | **File:** `E64_v2_ace_ES.xml`

```python
{
    "documentType": "A86",
    "businessType": "B33",
    "Area_Domain": "10YES-REE------0",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 64.3: Poland (1 day)
📄 Response: 179.0 KB | **File:** `E64_v4_ace_PL.xml`

```python
{
    "documentType": "A86",
    "businessType": "B33",
    "Area_Domain": "10YPL-AREA-----S",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 64.4: Czech Republic (1 day)
📄 Response: 176.8 KB | **File:** `E64_v5_ace_CZ.xml`

```python
{
    "documentType": "A86",
    "businessType": "B33",
    "Area_Domain": "10YCZ-CEPS-----N",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 📋 Endpoint 65: Activated Balancing Prices - Additional (17.1.F)

**Document Type:** `A84` | **Process Type:** `A16` | **Business Type:** `A96` (aFRR)  
**Description:** Prices of activated balancing energy (aFRR)

### ✅ Variant 65.1: Czech Republic aFRR (1 day)
📄 Response: 43.2 KB | **File:** `E65_v4_actprice_CZ_aFRR.xml`

```python
{
    "documentType": "A84",
    "processType": "A16",
    "controlArea_Domain": "10YCZ-CEPS-----N",
    "businessType": "A96",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 65.2: Poland aFRR (1 day)
📄 Response: 34.2 KB | **File:** `E65_fix3_actprice_PL_aFRR.xml`

```python
{
    "documentType": "A84",
    "processType": "A16",
    "controlArea_Domain": "10YPL-AREA-----S",
    "businessType": "A96",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 65.3: Romania aFRR (1 day)
📄 Response: 42.2 KB | **File:** `E65_fix4_actprice_RO_aFRR.xml`

```python
{
    "documentType": "A84",
    "processType": "A16",
    "controlArea_Domain": "10YRO-TEL------P",
    "businessType": "A96",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

### ✅ Variant 65.4: Finland aFRR (1 day)
📄 Response: 35.2 KB | **File:** `E65_fix5_actprice_FI_aFRR.xml`

```python
{
    "documentType": "A84",
    "processType": "A16",
    "controlArea_Domain": "10YFI-1--------U",
    "businessType": "A96",
    "periodStart": "202601072200",
    "periodEnd": "202601082200"
}
```

---

## 🔑 Key Parameter Reference

### Contract/Market Agreement Types

| Code | Type | Description |
|------|------|-------------|
| `A01` | Daily | Day-ahead contracts |
| `A02` | Weekly | Week-ahead contracts |
| `A03` | Monthly | Month-ahead contracts |
| `A04` | Yearly | Year-ahead contracts |
| `A07` | Intraday | Intraday contracts |

### Auction Types

| Code | Type | Description |
|------|------|-------------|
| `A01` | Implicit | Day-ahead implicit auctions |
| `A02` | Explicit | Explicit capacity auctions |
| `A08` | Continuous | Continuous intraday |

### EIC Codes Used

| Code | Country/Area |
|------|--------------|
| `10YAT-APG------L` | Austria |
| `10YBA-JPCC-----D` | Bosnia Herzegovina |
| `10YBE----------2` | Belgium |
| `10YCZ-CEPS-----N` | Czech Republic |
| `10YDK-1--------W` | Denmark West (DK1) |
| `10YES-REE------0` | Spain |
| `10YFI-1--------U` | Finland |
| `10YFR-RTE------C` | France |
| `10YGB----------A` | Great Britain |
| `10YHR-HEP------M` | Croatia |
| `10YHU-MAVIR----U` | Hungary |
| `10YIT-GRTN-----B` | Italy (Terna) |
| `10Y1001A1001A73I` | Italy North |
| `10YNL----------L` | Netherlands |
| `10YPL-AREA-----S` | Poland |
| `10YPT-REN------W` | Portugal |
| `10Y1001A1001A49F` | Russia |
| `10Y1001A1001A46L` | Sweden SE3 |
| `10YSK-SEPS-----K` | Slovakia |
| `10YSI-ELES-----O` | Slovenia |
| `10Y1001A1001A82H` | Germany-Luxembourg |

### German TSO Control Areas

| Code | TSO |
|------|-----|
| `10YDE-VE-------2` | 50Hertz |
| `10YDE-RWENET---I` | Amprion |
| `10YDE-EON------1` | TenneT TSO |
| `10YDE-ENBW-----N` | TransnetBW |

### DC Link / Interconnector Codes

| Code | Link |
|------|------|
| `11Y0-0000-0265-K` | ElecLink (GB-FR) |

### Synchronous Area Codes

| Code | Area |
|------|------|
| `10YEU-CONT-SYNC0` | Continental Europe |
| `10Y1001A1001A70O` | Nordic |

### Business Types (Balancing)

| Code | Type |
|------|------|
| `A96` | aFRR (Automatic Frequency Restoration Reserve) |
| `A97` | mFRR (Manual Frequency Restoration Reserve) |
| `A98` | RR (Replacement Reserve) |
| `B33` | ACE (Area Control Error) |

---

## 📁 File Locations

All variant results are saved in: `results/variants/`

Naming convention: `E{endpoint}_{variant}_{description}.xml`

---

## 📝 Notes

### Successful Endpoint Categories
- **Load Data (E11-E13, E15, E51):** Excellent coverage across all major European zones
- **Generation Data (E14, E16-E19, E52-E53, E61):** Comprehensive data for all tested countries
- **Day-ahead Prices (E10, E46-E47, E56-E58):** Available for 30+ bidding zones including all Nordic, Baltic, and Central European zones
- **Physical Flows (E20-E23, E49, E54, E59-E60):** Good coverage for major interconnectors
- **Outages (E24-E25, E37, E62-E63):** Generation and transmission outage data widely available
- **Balancing (E26-E28, E41, E43, E64-E65):** ACE, CBMPs, and aggregated bids available for key markets

### Endpoints with No Data (14 endpoints)
These endpoints returned "no data available" for all tested zones/periods:

| Endpoint | Type | Notes |
|----------|------|-------|
| E29 | FCR Total Capacity | May require specific LFC blocks or time periods |
| E31 | Net Position via Schedules | Use E22 (Commercial Schedules) instead |
| E32 | Congestion Management Costs | Sparse reporting |
| E33-E34 | Redispatching (Internal/XB) | Limited data publication |
| E35 | Expansion Projects | Long-term planning data |
| E36 | Countertrading | Sparse occurrences |
| E38 | Consumption Units Outages | Limited reporting |
| E39 | Trans Outages (Control Area) | Use E25 (border-based) instead |
| E40 | Offshore Grid Outages | Limited offshore infrastructure |
| E42 | Balancing Energy Bids | Use E43 (Aggregated) instead |
| E44 | Contracted Reserves | Check specific TSO requirements |
| E45 | Procured Capacity | Check specific TSO requirements |
| E50 | Congestion Income | May need different businessType |

### Recommendations
- **E15:** Originally tested Water Reservoirs (16.1.D) - substituted with Year-ahead Load Forecast (6.1.E)
- **E23:** DC Link Transfer Limits sparse - combined with Intraday Nominated Capacity
- **E30/E65:** Activated Energy Prices work well for AT, FR, CZ, PL, RO, FI

---

## 🌍 EIC Codes - Additional Countries

| Code | Country/Area |
|------|--------------|
| `10YCH-SWISSGRIDZ` | Switzerland |
| `10YGR-HTSO-----Y` | Greece |
| `10YRO-TEL------P` | Romania |
| `10Y1001A1001A788` | Italy South |
| `10YNO-2--------T` | Norway NO2 |
| `10YNO-3--------J` | Norway NO3 |
| `10YNO-4--------9` | Norway NO4 |
| `10Y1001A1001A48H` | Norway NO5 |
| `10Y1001A1001A44P` | Sweden SE1 |
| `10Y1001A1001A45N` | Sweden SE2 |
| `10Y1001A1001A47J` | Sweden SE4 |
| `10YDK-2--------M` | Denmark DK2 |
| `10Y1001A1001A39I` | Estonia |
| `10Y1001A00074` | Latvia |
| `10YLT-1001A0008Q` | Lithuania |

---

# ⚠️ Endpoints with No Data Available

> **Important for LLMs:** The following 14 endpoints consistently return "no data available" responses. This section explains **why** and provides **alternative endpoints** to use instead.

## Why Some Endpoints Return No Data

The ENTSO-E API has endpoints defined in EU regulations that may return empty responses due to:
1. **Sparse data** - Events like countertrading or redispatching are rare
2. **Publication delays** - Some data is only published monthly/yearly
3. **TSO-specific** - Not all TSOs publish through these specific endpoints
4. **Superseded** - Aggregated endpoints often contain the same data

## Quick Reference: No Data Endpoints & Alternatives

| Endpoint | Returns No Data | Use Instead |
|----------|-----------------|-------------|
| E29 | FCR Total Capacity | Platform-specific (PICASSO, MARI) |
| E31 | Net Position (Schedules) | **E8** (Net Positions) or **E22** (Schedules) |
| E32 | Congestion Costs | TSO annual reports |
| E33 | Redispatching Internal | Historical data only |
| E34 | Redispatching Cross-border | Historical data only |
| E35 | Expansion Projects | ENTSO-E TYNDP |
| E36 | Countertrading | Rare events |
| E38 | Consumption Outages | **E11-E15** (Load data) |
| E39 | Trans Outages (Area) | **E25** (by border) ✅ |
| E40 | Offshore Outages | **E25** (transmission outages) |
| E42 | Detailed Bids | **E43** (Aggregated Bids) ✅ |
| E44 | Contracted Reserves | Add BusinessType parameter |
| E45 | Procured Capacity | Try different processType |
| E50 | Congestion Income | **E7** (Auction Revenue) |

---

## Detailed Explanations

### E29: FCR Total Capacity

**Document Type:** `A26` | **Business Type:** `B22`  
**Article Reference:** 17.1.A - FCR Procurement

### Why No Data?
- **Frequency Containment Reserve (FCR)** data is typically aggregated at the **synchronous area level** (e.g., Continental Europe, Nordic)
- Most TSOs don't publish granular FCR capacity data through this endpoint
- Data may only be available for specific platforms (e.g., FCR Cooperation)

### Tested Parameters
- Synchronous areas: Continental Europe, Nordic, Great Britain
- Individual countries: Germany-Luxembourg
- Process types: A51 (aFRR), A47 (mFRR)

### Recommendation
Use **Endpoint 45 (Procured Balancing Capacity)** or check TSO-specific platforms for FCR data.

---

## E31: Net Position via Commercial Schedules (12.1.F)

**Document Type:** `A09` (same in/out domain)  
**Article Reference:** 12.1.F - Net positions from day-ahead market

### Why No Data?
- This endpoint calculates net position from **aggregated commercial schedules**
- Many TSOs publish this data through **different document types** or aggregated endpoints
- The `A09` document type with same in/out domain is rarely used

### Tested Parameters
- Countries: Austria, Belgium, Germany-Luxembourg, France, Spain, Netherlands

### Recommendation
Use **Endpoint 22 (Commercial Schedules - A09)** with different in/out domains, or **Endpoint 8 (Net Positions - A25)** for implicit auction results.

---

## E32: Congestion Management Costs (13.1.C)

**Document Type:** `A92`  
**Article Reference:** 13.1.C - Costs of congestion management

### Why No Data?
- Congestion management cost data is **published infrequently** (often monthly or yearly)
- Not all TSOs report through this specific endpoint
- May require **longer time ranges** (months/years) to find data

### Tested Parameters
- Countries: Belgium, Germany-Luxembourg, France, Netherlands, Austria, Spain, Italy, Poland

### Recommendation
Try extended time periods (full year) or check TSO annual reports for congestion cost data.

---

## E33: Redispatching - Internal (13.1.A)

**Document Type:** `A63` | **Business Type:** `A85`  
**Article Reference:** 13.1.A - Internal redispatching measures

### Why No Data?
- Internal redispatching data is **sensitive operational information**
- Published with **significant delays** (often T+1 month or later)
- Not all countries have active internal redispatching markets

### Tested Parameters
- Countries: Netherlands, Belgium, Germany-Luxembourg, France, Austria, Spain, Italy, Poland

### Recommendation
Check historical data (older periods) or TSO-specific transparency portals.

---

## E34: Redispatching - Cross Border (13.1.A)

**Document Type:** `A63` | **Business Type:** `A46`  
**Article Reference:** 13.1.A - Cross-border redispatching

### Why No Data?
- Cross-border redispatching is **relatively rare**
- Requires coordination between multiple TSOs
- Data publication may be restricted or aggregated

### Tested Parameters
- Borders: AT→FR, DE→FR, DE→NL, FR→BE, DE→AT, AT→IT, FR→ES, PL→DE

### Recommendation
Focus on borders with known congestion issues and check for data in monthly/yearly aggregations.

---

## E35: Expansion and Dismantling Projects (9.1)

**Document Type:** `A90`  
**Article Reference:** 9.1 - Grid expansion projects

### Why No Data?
- This is **long-term planning data**, not operational data
- Updates are infrequent (project-based)
- May require specific border/project identifiers

### Tested Parameters
- Borders: HU→SK, AT→DE, DE→NL, FR→ES, AT→IT, DE→PL, FR→BE, CZ→DE

### Recommendation
Check ENTSO-E's **Ten-Year Network Development Plan (TYNDP)** for infrastructure project data.

---

## E36: Countertrading (13.1.B)

**Document Type:** `A91`  
**Article Reference:** 13.1.B - Countertrading operations

### Why No Data?
- Countertrading is a **rare congestion management measure**
- Only used when redispatching is insufficient
- Sparse occurrence across European borders

### Tested Parameters
- Borders: ES→FR, DE→FR, AT→IT, DE→NL, FR→BE, DE→AT, PL→CZ, HU→SK

### Recommendation
This data is inherently sparse. Check for specific events in historical periods.

---

## E38: Aggregated Unavailability of Consumption Units (7.1.A-B)

**Document Type:** `A76`  
**Article Reference:** 7.1.A-B - Demand-side unavailability

### Why No Data?
- **Consumption unit outages** are rarely significant enough to report
- Most demand response is not published through this endpoint
- Limited regulatory requirement for this data

### Tested Parameters
- Countries: Germany-Luxembourg, France, Belgium, Netherlands, Spain, Italy, Austria, Poland

### Recommendation
This endpoint has limited practical data. Use load forecasts (E11-E15) for demand-side insights.

---

## E39: Transmission Outages - Control Area (10.1.A&B)

**Document Type:** `A78` with `ControlArea_Domain`  
**Article Reference:** 10.1.A&B - Transmission outages by control area

### Why No Data?
- Most TSOs publish outages by **border** (in/out domain), not by control area
- The `ControlArea_Domain` parameter is less commonly supported
- Use border-based queries for better results

### Tested Parameters
- Control Areas: France, Germany-Luxembourg, Belgium, Netherlands, Spain, Italy

### Recommendation
Use **Endpoint 25 (Transmission Infrastructure Unavailability)** with `in_Domain` and `out_Domain` parameters instead.

---

## E40: Offshore Grid Infrastructure Unavailability (10.1.C)

**Document Type:** `A79`  
**Article Reference:** 10.1.C - Offshore grid outages

### Why No Data?
- **Limited offshore infrastructure** in many European countries
- Only relevant for countries with significant offshore wind (DE, NL, DK, GB)
- Offshore connections often reported through standard transmission outages

### Tested Parameters
- Countries: Germany-Luxembourg, Netherlands, Belgium, Denmark DK1, Great Britain, France

### Recommendation
Check German and Dutch offshore wind connection operators for specific outage data.

---

## E42: Balancing Energy Bids (12.3.B&C)

**Document Type:** `A37` | **Business Type:** `B74`  
**Article Reference:** 12.3.B&C - Detailed balancing energy bids

### Why No Data?
- Detailed bid data is **confidential** in many markets
- Only **aggregated** bid data is typically published
- Archive retention is limited (93 days per documentation)

### Tested Parameters
- Countries: Czech Republic (mFRR/aFRR), Germany, Austria, France, Netherlands

### Recommendation
Use **Endpoint 43 (Aggregated Balancing Energy Bids - A24)** for available bid information.

---

## E44: Volumes and Prices of Contracted Reserves (17.1.B&C)

**Document Type:** `A81` | **Process Type:** `A52`  
**Article Reference:** 17.1.B&C - Reserve contract details

### Why No Data?
- Reserve contracting varies significantly by country
- Some TSOs use **bilateral contracts** not published on transparency platform
- Requires specific `BusinessType` for different reserve types

### Tested Parameters
- Countries: Germany-Luxembourg, Austria, France, Netherlands, Belgium, Spain

### Recommendation
Add `BusinessType` parameter (A95 for FCR, A96 for aFRR, A97 for mFRR) and check TSO-specific procurement results.

---

## E45: Procured Balancing Capacity (12.3.F)

**Document Type:** `A82`  
**Article Reference:** 12.3.F - Procured balancing capacity

### Why No Data?
- The combination of `documentType=A82` with certain `processType` values is **not valid**
- Requires specific TSO participation in common procurement platforms
- May need different parameter combinations

### Tested Parameters
- Countries: Netherlands, Austria, Germany-Luxembourg, Belgium (all with aFRR process type A51)

### Recommendation
Try different process types (A47 for mFRR, A46 for RR) or check platform-specific endpoints (PICASSO, MARI, TERRE).

---

## E50: Congestion Income (12.1.E)

**Document Type:** `A25` | **Business Type:** `B10`  
**Article Reference:** 12.1.E - Congestion revenue

### Why No Data?
- Congestion income is often calculated and published **monthly/yearly**
- The `B10` business type may not be applicable for all regions
- Different contract types may be required

### Tested Parameters
- Countries: Belgium, Netherlands, Austria, France, Germany, Spain (all with daily contract type A07)

### Recommendation
Try monthly (`A06`) or yearly (`A04`) contract types, or use **Endpoint 7 (Auction Revenue - A92)** for explicit allocation revenues.

---

---

# 🔑 Reference: Common EIC Codes

Use these EIC codes in the `in_Domain`, `out_Domain`, `BiddingZone_Domain`, or `controlArea_Domain` parameters.

## Major Bidding Zones

| Code | Country/Zone |
|------|--------------|
| `10YAT-APG------L` | Austria |
| `10YBE----------2` | Belgium |
| `10YCZ-CEPS-----N` | Czech Republic |
| `10Y1001A1001A82H` | Germany-Luxembourg |
| `10YDK-1--------W` | Denmark DK1 |
| `10YDK-2--------M` | Denmark DK2 |
| `10YES-REE------0` | Spain |
| `10YFI-1--------U` | Finland |
| `10YFR-RTE------C` | France |
| `10YGB----------A` | Great Britain |
| `10YGR-HTSO-----Y` | Greece |
| `10YHU-MAVIR----U` | Hungary |
| `10YIT-GRTN-----B` | Italy |
| `10YNL----------L` | Netherlands |
| `10YNO-1--------2` | Norway NO1 |
| `10YNO-2--------T` | Norway NO2 |
| `10YPL-AREA-----S` | Poland |
| `10YPT-REN------W` | Portugal |
| `10YRO-TEL------P` | Romania |
| `10YSK-SEPS-----K` | Slovakia |
| `10YSI-ELES-----O` | Slovenia |
| `10Y1001A1001A44P` | Sweden SE1 |
| `10Y1001A1001A45N` | Sweden SE2 |
| `10Y1001A1001A46L` | Sweden SE3 |
| `10Y1001A1001A47J` | Sweden SE4 |
| `10YCH-SWISSGRIDZ` | Switzerland |

## Italian Zones

| Code | Zone |
|------|------|
| `10Y1001A1001A73I` | Italy North |
| `10Y1001A1001A788` | Italy South |
| `10Y1001A1001A74G` | Italy Centre-North |
| `10Y1001A1001A75E` | Italy Centre-South |

## German Control Areas

| Code | TSO |
|------|-----|
| `10YDE-VE-------2` | 50Hertz |
| `10YDE-RWENET---I` | Amprion |
| `10YDE-EON------1` | TenneT |
| `10YDE-ENBW-----N` | TransnetBW |

## Baltic States

| Code | Country |
|------|---------|
| `10Y1001A1001A39I` | Estonia |
| `10YLV-1001A00074` | Latvia |
| `10YLT-1001A0008Q` | Lithuania |

## DC Links / Special Zones

| Code | Connection |
|------|------------|
| `10Y1001C--00098F` | ElecLink (GB-FR) |
| `10YBA-JPCC-----D` | Bosnia-Herzegovina |
| `10YHR-HEP------M` | Croatia |
| `10YRS-EMS------0` | Serbia |
| `10YCS-CG-TSO---S` | Montenegro |
| `10YMK-MEPSO----8` | North Macedonia |

---

# 📖 Document Type Quick Reference

| Code | Name | Use For |
|------|------|---------|
| `A09` | Finalised schedule | Commercial schedules |
| `A11` | Aggregated energy data | Physical flows |
| `A25` | Allocation result | Net positions, congestion income |
| `A26` | Capacity document | Nominated/allocated capacity |
| `A44` | Price document | Day-ahead prices |
| `A61` | Estimated net transfer capacity | NTC forecasts |
| `A65` | System total load | Actual/forecast load |
| `A68` | Installed generation capacity | Generation capacity |
| `A69` | Wind and solar forecast | Renewable forecasts |
| `A71` | Generation forecast | Day-ahead generation |
| `A73` | Actual generation per unit | Unit-level generation |
| `A75` | Actual generation per type | Aggregated by fuel |
| `A78` | Transmission unavailability | Transmission outages |
| `A80` | Generation unavailability | Generation outages |
| `A84` | Activated balancing energy prices | Balancing prices |
| `A85` | Imbalance prices | Settlement prices |
| `A86` | Imbalance volume | System imbalance |

---

*This reference contains 260 documented API request examples across 65 endpoints. Examples verified January 2026.*
