> Each bullet below is a *natural-language version* of one of the working (or documented “no data”) examples in the reference.  
> Dates/times are expressed using the same `periodStart/periodEnd` values (UTC) as in the examples.
---

## E01 — Total Nominated Capacity (12.1.B) — `documentType=A26`, `businessType=B08`
- Request **total nominated schedules** from **Great Britain → Belgium** for `202601072200` to `202601082200` (UTC).
- Request **total nominated schedules** from **France → Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E02 — Implicit Allocations: Offered Transfer Capacity (11.1) — `documentType=A31`, `auction.Type=A01`
- Request **implicit day-ahead offered transfer capacity (daily)** from **DK1 → Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).
- Request **implicit intraday offered transfer capacity** from **Belgium → Netherlands** for `202601072200` to `202601082200` (UTC).

## E03 — Transfer Capacities with Third Countries (12.1.H) — `documentType=A94`, `auction.Type=A02`
- Request **explicit intraday NTC** from **Finland → Russia** for `202601072200` to `202601082200` (UTC).
- Request **explicit intraday NTC** from **Russia → Finland** (reverse direction) for `202601072200` to `202601082200` (UTC).

## E04 — Total Capacity Already Allocated (12.1.C) — `documentType=A26`, `businessType=A29`
- Request **already allocated daily capacity** from **Croatia → Bosnia and Herzegovina** for `202601072200` to `202601082200` (UTC).
- Request **already allocated daily capacity** from **Austria → Hungary** for `202601072200` to `202601082200` (UTC).

## E05 — Explicit Allocations: Offered Transfer Capacity (11.1.A) — `documentType=A31`, `auction.Type=A02`
- Request **explicit day-ahead (daily) offered capacity** from **Great Britain → Belgium** for `202601072200` to `202601082200` (UTC).
- Request **explicit month-ahead offered capacity** from **Great Britain → Belgium** for `202601012200` to `202601082200` (UTC).

## E06 — Explicit Allocations: Use of Transfer Capacity (12.1.A) — `documentType=A25`, `businessType=B05`
- Request **usage of explicitly allocated intraday capacity** from **Great Britain → Belgium** for `202601072200` to `202601082200` (UTC).
- Request **usage of explicitly allocated intraday capacity** from **Belgium → Great Britain** (reverse direction) for `202601072200` to `202601082200` (UTC).

## E07 — Explicit Allocations: Auction Revenue (12.1.A) — `documentType=A25`, `businessType=B07`
- Request **auction revenue from explicit capacity allocation** on **Croatia → Bosnia and Herzegovina** (daily) for `202601072200` to `202601082200` (UTC).
- Request **auction revenue from explicit capacity allocation** on **Great Britain → Belgium** (daily) for `202601072200` to `202601082200` (UTC).

## E08 — Implicit Auction: Net Positions (12.1.E) — `documentType=A25`, `businessType=B09`
- Request **net import/export position** for **Belgium** (intraday contract) for `202601072200` to `202601082200` (UTC).
- Request **net import/export position** for **Austria** (intraday contract) for `202601072200` to `202601082200` (UTC).

## E09 — Continuous Allocations: Offered Transfer Capacity (11.1) — `documentType=A31`, `auction.Type=A08`
- Request **continuous intraday offered capacity** from **Belgium → Netherlands** for `202601072200` to `202601082200` (UTC).
- Request **continuous intraday offered capacity** from **Netherlands → Belgium** (reverse direction) for `202601072200` to `202601082200` (UTC).

## E10 — Day-ahead Energy Prices (12.1.D) — `documentType=A44`
- Request **day-ahead energy prices** for **Austria** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead energy prices** for **Spain** for `202601072200` to `202601082200` (UTC).

## E11 — Actual Total Load (6.1.A) — `documentType=A65`, `processType=A16`
- Request **actual total load** for **Czech Republic** for `202601072200` to `202601082200` (UTC).
- Request **actual total load** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E12 — Day-ahead Total Load Forecast (6.1.B) — `documentType=A65`, `processType=A01`
- Request **day-ahead load forecast** for **Czech Republic** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead load forecast** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E13 — Week-ahead Total Load Forecast (6.1.C) — `documentType=A65`, `processType=A31`
- Request **week-ahead load forecast** for **Czech Republic** for `202601012200` to `202601082200` (UTC).
- Request **week-ahead load forecast** for **Germany-Luxembourg** for `202601012200` to `202601082200` (UTC).

## E14 — Installed Capacity per Production Type (14.1.A) — `documentType=A68`, `processType=A33`
- Request **installed generation capacity by fuel type** for **Belgium** for `202601072200` to `202601082200` (UTC).
- Request **installed generation capacity by fuel type** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E15 — Year-ahead Total Load Forecast (6.1.E) — `documentType=A65`, `processType=A33`
- Request **year-ahead load forecast** for **Belgium** for `202601072200` to `202601082200` (UTC).
- Request **year-ahead load forecast** for **France** for `202601072200` to `202601082200` (UTC).

## E16 — Actual Generation per Generation Unit (16.1.A) — `documentType=A75`, `processType=A16`
- Request **actual generation per unit (≥100 MW)** for **Germany 50Hertz control area** for `202601072200` to `202601082200` (UTC).
- Request **actual generation per unit (≥100 MW)** for **Germany Amprion control area** for `202601072200` to `202601082200` (UTC).

## E17 — Actual Generation per Production Type (16.1.B&C) — `documentType=A75`, `processType=A16`
- Request **actual generation aggregated by fuel/technology** for **Belgium** for `202601072200` to `202601082200` (UTC).
- Request **actual generation aggregated by fuel/technology** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E18 — Generation Forecast (Day-ahead) (14.1.C) — `documentType=A71`, `processType=A01`
- Request **day-ahead generation forecast** for **Belgium** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead generation forecast** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E19 — Wind and Solar Forecast (14.1.D) — `documentType=A69`, `processType=A01`
- Request **day-ahead wind + solar forecast** for **Belgium** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead wind + solar forecast** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E20 — Cross-border Physical Flows (12.1.G) — `documentType=A11`
- Request **actual physical cross-border flows** from **Germany (Amprion) → Belgium** for `202601072200` to `202601082200` (UTC).
- Request **actual physical cross-border flows** from **France → Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E21 — Forecasted Transfer Capacities (11.1.A) — `documentType=A61`
- Request **daily NTC forecast** from **Great Britain → Belgium** for `202601072200` to `202601082200` (UTC).
- Request **daily NTC forecast** from **France → Spain** for `202601072200` to `202601082200` (UTC).

## E22 — Commercial Schedules (12.1.F) — `documentType=A09`
- Request **scheduled commercial exchanges** from **Belgium → France** for `202601072200` to `202601082200` (UTC).
- Request **scheduled commercial exchanges** from **France → Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E23 — DC Link / Intraday Nominated Capacity (11.3 / 12.1.B)
- Request **DC interconnector (A93) flow/limits** from **ElecLink → France** for `202601072200` to `202601082200` (UTC).
- Request **intraday nominated capacity (A26/B08 + intraday contract A07)** from **France → Spain** for `202601072200` to `202601082200` (UTC).

## E24 — Unavailability of Generation Units (15.1.A&B) — `documentType=A80`
- Request **generation unit outages (planned/forced)** for **Belgium** for `202601072200` to `202601082200` (UTC).
- Request **generation unit outages (planned/forced)** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E25 — Unavailability of Transmission Infrastructure (10.1.A&B) — `documentType=A78`
- Request **transmission outages by border** from **France → Belgium** for `202601072200` to `202601082200` (UTC).
- Request **transmission outages by border** from **Germany-Luxembourg → France** for `202601072200` to `202601082200` (UTC).

## E26 — Imbalance Prices (17.1.G) — `documentType=A85`
- Request **imbalance settlement prices** for **Netherlands control area** for `202601072200` to `202601082200` (UTC).
- Request **imbalance settlement prices** for **Belgium control area** for `202601072200` to `202601082200` (UTC).

## E27 — Total Imbalance Volumes (17.1.H) — `documentType=A86`
- Request **total system imbalance volumes** for **Belgium control area** for `202601072200` to `202601082200` (UTC).
- Request **total system imbalance volumes** for **Austria control area** for `202601072200` to `202601082200` (UTC).

## E28 — Current Balancing State / ACE (12.3.A) — `documentType=A86`, `businessType=B33`
- Request **ACE (Area Control Error)** for **Belgium area domain** for `202601072200` to `202601082200` (UTC).
- Request **ACE (Area Control Error)** for **Netherlands area domain** for `202601072200` to `202601082200` (UTC).

## E29 — FCR Total Capacity — `documentType=A26`, `businessType=A25` (⚠️ documented “no data”)
- Attempt to request **FCR total capacity** for **Continental Europe synchronous area** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **FCR total capacity** for **Nordic synchronous area** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E30 — Prices of Activated Balancing Energy (17.1.F) — `documentType=A84`, `processType=A16`
- Request **activated balancing energy prices (aFRR, businessType=A96)** for **Austria control area** for `202601072200` to `202601082200` (UTC).
- Request **activated balancing energy prices (mFRR, businessType=A97)** for **Austria control area** for `202601072200` to `202601082200` (UTC).

## E31 — Net Position via Commercial Schedules (12.1.F) — `documentType=A09` (⚠️ documented “no data”)
- Attempt to request **net position from schedules** for **Austria (out=in)** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **net position from schedules** for **Belgium (out=in)** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E32 — Congestion Management Costs (13.1.C) — `documentType=A92` (⚠️ documented “no data”)
- Attempt to request **congestion management costs** for **Belgium** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **congestion management costs** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E33 — Redispatching: Internal (13.1.A) — `documentType=A63`, `businessType=A85` (⚠️ documented “no data”)
- Attempt to request **internal redispatching measures** for **Netherlands (out=in)** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **internal redispatching measures** for **Belgium (out=in)** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E34 — Redispatching: Cross-border (13.1.A) — `documentType=A63`, `businessType=A46` (⚠️ documented “no data”)
- Attempt to request **cross-border redispatching measures** from **Austria → France** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **cross-border redispatching measures** from **Germany-Luxembourg → France** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E35 — Expansion and Dismantling Projects (9.1) — `documentType=A90` (⚠️ documented “no data”)
- Attempt to request **grid expansion/dismantling projects** from **Hungary → Slovakia** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **grid expansion/dismantling projects** from **Austria → Germany-Luxembourg** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E36 — Countertrading (13.1.B) — `documentType=A91` (⚠️ documented “no data”)
- Attempt to request **countertrading operations** from **Spain → France** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **countertrading operations** from **Germany-Luxembourg → France** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E37 — Unavailability of Production Units (15.1.C-D) — `documentType=A77`
- Request **production unit unavailability** for **France** for `202601072200` to `202601082200` (UTC).
- Request **production unit unavailability** for **Spain** for `202601072200` to `202601082200` (UTC).

## E38 — Aggregated Unavailability of Consumption Units (7.1.A-B) — `documentType=A76` (⚠️ documented “no data”)
- Attempt to request **consumption unit unavailability (aggregated)** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **consumption unit unavailability (aggregated)** for **France** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E39 — Transmission Outages (Control Area) (10.1.A&B) — `documentType=A78` + `ControlArea_Domain` (⚠️ documented “no data”)
- Attempt to request **transmission outages by control area** for **France control area** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **transmission outages by control area** for **Germany-Luxembourg control area** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E40 — Offshore Grid Infrastructure Unavailability (10.1.C) — `documentType=A79` (⚠️ documented “no data”)
- Attempt to request **offshore grid infrastructure outages** for **Germany-Luxembourg** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **offshore grid infrastructure outages** for **Netherlands** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E41 — Cross Border Marginal Prices (CBMPs) for aFRR — `documentType=A84`, `processType=A67`, `businessType=A96`
- Request **cross-border marginal prices for aFRR** for **Germany 50Hertz control area** for `202601072200` to `202601082200` (UTC).
- Request **cross-border marginal prices for aFRR** for **Germany TenneT control area** for `202601072200` to `202601082200` (UTC).

## E42 — Balancing Energy Bids (12.3.B&C) — `documentType=A37`, `businessType=B74` (⚠️ documented “no data”)
- Attempt to request **detailed balancing energy bids (mFRR, A47)** for **Czech Republic connecting domain** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **detailed balancing energy bids (aFRR, A51)** for **Czech Republic connecting domain** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E43 — Aggregated Balancing Energy Bids (12.3.E) — `documentType=A24`
- Request **aggregated balancing bids** for **Austria aFRR (processType=A51)** for `202601072200` to `202601082200` (UTC).
- Request **aggregated balancing bids** for **Belgium mFRR (processType=A47)** for `202601072200` to `202601082200` (UTC).

## E44 — Volumes & Prices of Contracted Reserves (17.1.B&C) — `documentType=A81`, `processType=A52` (⚠️ documented “no data”)
- Attempt to request **contracted reserve volumes/prices** for **Germany-Luxembourg control area** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **contracted reserve volumes/prices** for **Austria control area** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E45 — Procured Balancing Capacity (12.3.F) — `documentType=A82` (⚠️ documented “no data”)
- Attempt to request **procured balancing capacity (aFRR, processType=A51)** for **Netherlands control area** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **procured balancing capacity (aFRR, processType=A51)** for **Austria control area** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E46 — Day-ahead Prices: Central European Countries — `documentType=A44`
- Request **day-ahead prices** for **Switzerland** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead prices** for **Czech Republic** for `202601072200` to `202601082200` (UTC).

## E47 — Day-ahead Prices: Nordic & Balkan Countries — `documentType=A44`
- Request **day-ahead prices** for **Norway NO1** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead prices** for **Norway NO2** for `202601072200` to `202601082200` (UTC).

## E48 — Imbalance Prices: Additional Countries (17.1.G) — `documentType=A85`
- Request **imbalance prices** for **Spain control area** for `202601072200` to `202601082200` (UTC).
- Request **imbalance prices** for **Czech Republic control area** for `202601072200` to `202601082200` (UTC).

## E49 — Physical Flows: Additional Borders (12.1.G) — `documentType=A11`
- Request **actual physical flows** from **Switzerland → Italy** for `202601072200` to `202601082200` (UTC).
- Request **actual physical flows** from **Switzerland → Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E50 — Congestion Income (12.1.E) — `documentType=A25`, `businessType=B10` (⚠️ documented “no data”)
- Attempt to request **congestion income** for **Belgium (out=in, intraday contract A07)** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.
- Attempt to request **congestion income** for **Netherlands (out=in, intraday contract A07)** for `202601072200` to `202601082200` (UTC) *(returned no data in tests)*.

## E51 — Actual Load: Additional Countries (6.1.A) — `documentType=A65`, `processType=A16`
- Request **actual total load** for **Portugal** for `202601072200` to `202601082200` (UTC).
- Request **actual total load** for **Greece** for `202601072200` to `202601082200` (UTC).

## E52 — Actual Generation by Type: Additional (16.1.B&C) — `documentType=A75`, `processType=A16`
- Request **actual generation by production type** for **Austria** for `202601072200` to `202601082200` (UTC).
- Request **actual generation by production type** for **Netherlands** for `202601072200` to `202601082200` (UTC).

## E53 — Wind/Solar Forecast: Additional (14.1.D) — `documentType=A69`, `processType=A01`
- Request **day-ahead wind + solar forecast** for **Austria** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead wind + solar forecast** for **Netherlands** for `202601072200` to `202601082200` (UTC).

## E54 — NTC Forecast: Additional Borders (11.1.A) — `documentType=A61`
- Request **daily NTC forecast** from **Switzerland → Italy** for `202601072200` to `202601082200` (UTC).
- Request **daily NTC forecast** from **Switzerland → Germany-Luxembourg** for `202601072200` to `202601082200` (UTC).

## E55 — Imbalance Volumes: Additional (17.1.H) — `documentType=A86`
- Request **total imbalance volumes** for **Italy control area** for `202601072200` to `202601082200` (UTC).
- Request **total imbalance volumes** for **Czech Republic control area** for `202601072200` to `202601082200` (UTC).

## E56 — Day-ahead Prices: Italian Zones (12.1.D) — `documentType=A44`
- Request **day-ahead prices** for **Italy North** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead prices** for **Italy South** for `202601072200` to `202601082200` (UTC).

## E57 — Day-ahead Prices: Nordic Zones (12.1.D) — `documentType=A44`
- Request **day-ahead prices** for **Norway NO3** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead prices** for **Norway NO4** for `202601072200` to `202601082200` (UTC).

## E58 — Day-ahead Prices: Baltic & Eastern (12.1.D) — `documentType=A44`
- Request **day-ahead prices** for **Estonia** for `202601072200` to `202601082200` (UTC).
- Request **day-ahead prices** for **Latvia** for `202601072200` to `202601082200` (UTC).

## E59 — Physical Flows: Nordic Borders (12.1.G) — `documentType=A11`
- Request **actual physical flows** from **Norway NO1 → Sweden SE3** for `202601072200` to `202601082200` (UTC).
- Request **actual physical flows** from **Sweden SE3 → Finland** for `202601072200` to `202601082200` (UTC).

## E60 — Physical Flows: Eastern Europe (12.1.G) — `documentType=A11`
- Request **actual physical flows** from **Poland → Czech Republic** for `202601072200` to `202601082200` (UTC).
- Request **actual physical flows** from **Czech Republic → Austria** for `202601072200` to `202601082200` (UTC).

## E61 — Installed Capacity: Additional (14.1.A) — `documentType=A68`, `processType=A33`
- Request **installed capacity by fuel type** for **Poland** for `202601072200` to `202601082200` (UTC).
- Request **installed capacity by fuel type** for **Czech Republic** for `202601072200` to `202601082200` (UTC).

## E62 — Generation Outages: Additional (15.1.A&B) — `documentType=A80`
- Request **generation unit outages** for **Italy** for `202601072200` to `202601082200` (UTC).
- Request **generation unit outages** for **Poland** for `202601072200` to `202601082200` (UTC).

## E63 — Transmission Outages: Additional (10.1.A&B) — `documentType=A78`
- Request **transmission outages by border** from **Germany-Luxembourg → Poland** for `202601072200` to `202601082200` (UTC).
- Request **transmission outages by border** from **Czech Republic → Austria** for `202601072200` to `202601082200` (UTC).

## E64 — ACE: Additional (12.3.A) — `documentType=A86`, `businessType=B33`
- Request **ACE (Area Control Error)** for **Italy area domain** for `202601072200` to `202601082200` (UTC).
- Request **ACE (Area Control Error)** for **Spain area domain** for `202601072200` to `202601082200` (UTC).

## E65 — Activated Balancing Prices: Additional (17.1.F) — `documentType=A84`, `processType=A16`, `businessType=A96`
- Request **activated aFRR prices** for **Czech Republic control area** for `202601072200` to `202601082200` (UTC).
- Request **activated aFRR prices** for **Poland control area** for `202601072200` to `202601082200` (UTC).
