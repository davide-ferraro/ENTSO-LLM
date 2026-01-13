# ENTSO-E API Examples Menu

> **Purpose**: Quick reference for finding the right API example. Use keywords to match your query to the correct endpoint.

---

## E01 — Total Nominated Capacity (12.1.B)
- **Keywords**: nominated capacity, schedules, cross-border, transmission, nominations
- **documentType**: A26, **businessType**: B08
- **Domains**: out_Domain → in_Domain (border direction)

## E02 — Implicit Allocations - Offered Transfer Capacity (11.1)
- **Keywords**: implicit allocation, NTC, ATC, day-ahead capacity, intraday capacity, market coupling
- **documentType**: A31, **auction.Type**: A01
- **Domains**: out_Domain → in_Domain

## E03 — Transfer Capacities with Third Countries (12.1.H)
- **Keywords**: third country, non-EU, Russia, explicit allocation
- **documentType**: A94, **auction.Type**: A02
- **Domains**: out_Domain → in_Domain

## E04 — Total Capacity Already Allocated (12.1.C)
- **Keywords**: already allocated, allocated capacity, border capacity
- **documentType**: A26, **businessType**: A29
- **Domains**: out_Domain → in_Domain

## E05 — Explicit Allocations - Offered Transfer Capacity (11.1.A)
- **Keywords**: explicit auction, capacity auction, offered capacity
- **documentType**: A31, **auction.Type**: A02
- **Domains**: out_Domain → in_Domain

## E06 — Explicit Allocations - Use of Transfer Capacity (12.1.A)
- **Keywords**: capacity usage, transfer usage, explicit use
- **documentType**: A25, **businessType**: B05
- **Domains**: out_Domain → in_Domain

## E07 — Explicit Allocations - Auction Revenue (12.1.A)
- **Keywords**: auction revenue, capacity revenue, border revenue
- **documentType**: A25, **businessType**: B07
- **Domains**: out_Domain → in_Domain

## E08 — Implicit Auction - Net Positions (12.1.E)
- **Keywords**: net position, import, export, net import, net export
- **documentType**: A25, **businessType**: B09
- **Domains**: out_Domain = in_Domain (same zone)

## E09 — Continuous Allocations - Offered Transfer Capacity (11.1)
- **Keywords**: continuous market, continuous intraday, SIDC
- **documentType**: A31, **auction.Type**: A08
- **Domains**: Out_Domain → In_Domain

## E10 — Day-ahead Energy Prices (12.1.D)
- **Keywords**: day-ahead prices, electricity prices, spot prices, price, energy price, DA prices
- **documentType**: A44
- **Domains**: out_Domain = in_Domain (BOTH required, same value for bidding zone)
- **Note**: Both in_Domain AND out_Domain are MANDATORY, set them to the same EIC code

## E11 — Actual Total Load (6.1.A)
- **Keywords**: actual load, electricity consumption, demand, total load, realised load
- **documentType**: A65, **processType**: A16
- **Domains**: outBiddingZone_Domain

## E12 — Day-ahead Total Load Forecast (6.1.B)
- **Keywords**: load forecast, day-ahead forecast, demand forecast
- **documentType**: A65, **processType**: A01
- **Domains**: outBiddingZone_Domain

## E13 — Week-ahead Total Load Forecast (6.1.C)
- **Keywords**: week-ahead forecast, weekly forecast, load forecast
- **documentType**: A65, **processType**: A31
- **Domains**: outBiddingZone_Domain

## E14 — Installed Capacity per Production Type (14.1.A)
- **Keywords**: installed capacity, capacity, installed, generation capacity
- **documentType**: A68, **processType**: A33
- **Domains**: in_Domain

## E15 — Year-ahead Total Load Forecast (6.1.E)
- **Keywords**: year-ahead forecast, yearly forecast, annual forecast
- **documentType**: A65, **processType**: A33
- **Domains**: outBiddingZone_Domain

## E16 — Actual Generation per Generation Unit (16.1.A)
- **Keywords**: generation unit, power plant, per unit generation
- **documentType**: A73, **processType**: A16
- **Domains**: in_Domain

## E17 — Actual Generation per Production Type (16.1.B&C)
- **Keywords**: generation by type, solar generation, wind generation, nuclear, gas, coal, actual generation, generation mix
- **documentType**: A75, **processType**: A16
- **Domains**: in_Domain
- **Optional**: psrType for specific fuel (B16=Solar, B19=Wind Onshore, B14=Nuclear, B04=Gas)

## E18 — Generation Forecast - Day Ahead (14.1.C)
- **Keywords**: generation forecast, day-ahead generation, scheduled generation
- **documentType**: A71, **processType**: A01
- **Domains**: in_Domain

## E19 — Wind and Solar Forecast (14.1.D)
- **Keywords**: wind forecast, solar forecast, renewable forecast, wind solar
- **documentType**: A69, **processType**: A01 or A40
- **Domains**: in_Domain

## E20 — Cross-Border Physical Flows (12.1.G)
- **Keywords**: physical flows, cross-border, interconnector, power flow, flows between
- **documentType**: A11
- **Domains**: out_Domain → in_Domain (direction matters)

## E21 — Forecasted Transfer Capacities (11.1.A)
- **Keywords**: NTC forecast, transfer capacity forecast, forecasted NTC
- **documentType**: A61, **contract_MarketAgreement.Type**: A01
- **Domains**: out_Domain → in_Domain

## E22 — Commercial Schedules (12.1.F)
- **Keywords**: commercial schedules, scheduled exchanges, nominations
- **documentType**: A09
- **Domains**: out_Domain → in_Domain

## E23 — DC Link / Intraday Nominated Capacity (11.3 / 12.1.B)
- **Keywords**: DC link, HVDC, intraday capacity, DC interconnector
- **documentType**: A26 or A31
- **Domains**: out_Domain → in_Domain

## E24 — Unavailability of Generation Units (15.1.A&B)
- **Keywords**: generation outage, power plant outage, unavailability, maintenance, planned outage
- **documentType**: A80
- **Domains**: biddingZone_Domain

## E25 — Unavailability of Transmission Infrastructure (10.1.A&B)
- **Keywords**: transmission outage, line outage, grid outage, infrastructure unavailability
- **documentType**: A78
- **Domains**: in_Domain or out_Domain

## E26 — Imbalance Prices (17.1.G)
- **Keywords**: imbalance price, balancing price, settlement price
- **documentType**: A85
- **Domains**: controlArea_Domain

## E27 — Total Imbalance Volumes (17.1.H)
- **Keywords**: imbalance volume, system imbalance, balancing volume
- **documentType**: A86
- **Domains**: controlArea_Domain

## E28 — Current Balancing State / ACE (12.3.A)
- **Keywords**: ACE, area control error, balancing state, frequency control
- **documentType**: A86
- **Domains**: controlArea_Domain

## E29 — FCR Total Capacity
- **Keywords**: FCR, frequency containment reserve, primary reserve
- **documentType**: A26
- **Note**: Sparse data - may return no results

## E30 — Prices of Activated Balancing Energy (17.1.F)
- **Keywords**: activated balancing, balancing energy price, aFRR price, mFRR price
- **documentType**: A84
- **Domains**: controlArea_Domain

## E37 — Unavailability of Production Units (15.1.C-D)
- **Keywords**: production unit outage, generator unavailability
- **documentType**: A77
- **Domains**: biddingZone_Domain

## E41 — Cross Border Marginal Prices (CBMPs) for aFRR
- **Keywords**: CBMP, cross border marginal price, aFRR marginal
- **documentType**: A84
- **Domains**: controlArea_Domain

## E43 — Aggregated Balancing Energy Bids (12.3.E)
- **Keywords**: balancing bids, merit order, aggregated bids
- **documentType**: A24
- **Domains**: controlArea_Domain

## E46 — Day-ahead Prices - Central European Countries
- **Keywords**: prices Germany, prices France, prices Austria, prices Belgium, prices Netherlands
- **documentType**: A44
- **Domains**: out_Domain = in_Domain (same value)

## E47 — Day-ahead Prices - Nordic and Balkan Countries
- **Keywords**: prices Norway, prices Sweden, prices Denmark, prices Finland, prices Serbia
- **documentType**: A44
- **Domains**: out_Domain = in_Domain (same value)

## E48 — Imbalance Prices - Additional Countries (17.1.G)
- **Keywords**: imbalance Germany, imbalance France, imbalance Spain
- **documentType**: A85
- **Domains**: controlArea_Domain

## E49 — Physical Flows - Additional Borders (12.1.G)
- **Keywords**: flows Germany France, flows Spain Portugal
- **documentType**: A11
- **Domains**: out_Domain → in_Domain

## E50 — Congestion Income (12.1.E)
- **Keywords**: congestion, congestion income, congestion revenue
- **documentType**: A25, **businessType**: B10
- **Note**: Sparse data

## E51 — Actual Load - Additional Countries (6.1.A)
- **Keywords**: load Spain, load Italy, load Poland, consumption
- **documentType**: A65, **processType**: A16
- **Domains**: outBiddingZone_Domain

## E52 — Actual Generation by Type - Additional (16.1.B&C)
- **Keywords**: generation Spain, generation Italy, generation mix, solar Spain
- **documentType**: A75, **processType**: A16
- **Domains**: in_Domain

## E53 — Wind/Solar Forecast - Additional (14.1.D)
- **Keywords**: wind forecast Spain, solar forecast Germany
- **documentType**: A69
- **Domains**: in_Domain

## E54 — NTC Forecast - Additional Borders (11.1.A)
- **Keywords**: NTC Spain France, transfer capacity forecast
- **documentType**: A61
- **Domains**: out_Domain → in_Domain

## E55 — Imbalance Volumes - Additional (17.1.H)
- **Keywords**: imbalance volume Germany, imbalance volume France
- **documentType**: A86
- **Domains**: controlArea_Domain

## E56 — Day-ahead Prices - Italian Zones (12.1.D)
- **Keywords**: Italy North, Italy South, Italy Sicily, Italy Sardinia, Italian price
- **documentType**: A44
- **Domains**: out_Domain = in_Domain (same value)

## E57 — Day-ahead Prices - Nordic Zones (12.1.D)
- **Keywords**: Norway NO1 NO2 NO3, Sweden SE1 SE2 SE3 SE4, Nordic price
- **documentType**: A44
- **Domains**: out_Domain = in_Domain (same value)

## E58 — Day-ahead Prices - Baltic & Eastern (12.1.D)
- **Keywords**: Estonia, Latvia, Lithuania, Baltic, Romania, Bulgaria
- **documentType**: A44
- **Domains**: out_Domain = in_Domain (same value)

## E59 — Physical Flows - Nordic Borders (12.1.G)
- **Keywords**: flows Norway Sweden, flows Denmark Germany
- **documentType**: A11
- **Domains**: out_Domain → in_Domain

## E60 — Physical Flows - Eastern Europe (12.1.G)
- **Keywords**: flows Poland Germany, flows Czech Austria
- **documentType**: A11
- **Domains**: out_Domain → in_Domain

## E61 — Installed Capacity - Additional (14.1.A)
- **Keywords**: capacity Spain, capacity Poland, installed capacity Italy
- **documentType**: A68, **processType**: A33
- **Domains**: in_Domain

## E62 — Generation Outages - Additional (15.1.A&B)
- **Keywords**: outages France, outages Germany, nuclear outage
- **documentType**: A80
- **Domains**: biddingZone_Domain

## E63 — Transmission Outages - Additional (10.1.A&B)
- **Keywords**: line outage Germany, grid outage France
- **documentType**: A78
- **Domains**: in_Domain or out_Domain

## E64 — ACE (Area Control Error) - Additional (12.3.A)
- **Keywords**: ACE Germany, ACE France, frequency deviation
- **documentType**: A86
- **Domains**: controlArea_Domain

## E65 — Activated Balancing Prices - Additional (17.1.F)
- **Keywords**: balancing price Germany, mFRR price France
- **documentType**: A84
- **Domains**: controlArea_Domain

---

## Quick Reference: Common Use Cases

| User Query | Best Endpoint |
|------------|---------------|
| "day-ahead prices for Germany" | E10-E46 (documentType=A44, in_Domain=out_Domain) |
| "solar generation in Spain" | E17/E52 (documentType=A75, psrType=B16) |
| "actual load in France" | E11/E51 (documentType=A65, processType=A16) |
| "wind forecast for Germany" | E19/E53 (documentType=A69) |
| "physical flows from France to Spain" | E20/E49 (documentType=A11) |
| "imbalance prices in Spain" | E26/E48 (documentType=A85) |
| "generation outages in France" | E24/E62 (documentType=A80) |
