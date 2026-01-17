# ENTSO-E API Examples Menu (Router-Optimized)

> **Purpose (Router Only):**
> Pick the correct endpoint ID(s) from keywords and intent.
> Do **NOT** decide EIC codes or fill parameters here — generator handles that.

---

## Global Router Rules

1. Pick **1 endpoint** (no multiples).
2. Decide by **intent** first (prices vs load vs generation vs flows vs outages vs balancing).
3. Then by **time nature** (actual vs forecast vs capacity vs schedules).
4. Geography is **NOT routing** (country/zone is chosen later).
5. “Between two areas/borders” → prefer endpoints with **out_Domain → in_Domain**.
6. “In one zone” → prefer endpoints with **one domain param** or **in=out**.

---

## ✅ Working vs ⚠️ Sparse Endpoints

- ✅ Generally working across many zones: most endpoints except the list below.
- ⚠️ Sparse / “no data” commonly observed:






# Market — Capacity, Allocations, Prices

---

## 12.1.B - Total Nominated Capacity

DATA DOMAIN: Market / Transmission  
DATA NATURE: Scheduled / Nominated Capacity  

### WHEN TO USE
- User asks for **nominated capacity** between two areas
- Mentions: nominated schedules, nominated capacity, border nominations
- Questions about **how much capacity was nominated** on a border

### DO NOT USE IF
- User asks for offered capacity (use E02, E05, E09)
- User asks for physical flows (use E20)
- User asks for prices (use E10)

---

## 11.1 - Implicit Allocations – Offered Transfer Capacity

DATA DOMAIN: Market / Transmission  
DATA NATURE: Offered Capacity (Implicit Allocation)  

### WHEN TO USE
- User asks for **available transfer capacity** in **day-ahead or intraday market coupling**
- Mentions: implicit allocation, market coupling, ATC, NTC offered
- Asks “how much capacity is available” before trading

### DO NOT USE IF
- User asks for explicit auctions (use E05)
- User asks for already allocated or used capacity (use E04 or E06)
- User asks for physical flows (use E20)

---

## 12.1.H - Transfer Capacities with Third Countries

DATA DOMAIN: Market / Transmission  
DATA NATURE: Offered Capacity (Explicit, Third Countries)  

### WHEN TO USE
- User asks for **transfer capacity with non-EU / third countries**
- Mentions: Russia, Ukraine, third country border capacity
- Explicit allocation context for non-EU borders

### DO NOT USE IF
- Both areas are EU countries (use E02, E05, or E21)
- User asks for physical flows (use E20)

---

## 12.1.C - Total Capacity Already Allocated

DATA DOMAIN: Market / Transmission  
DATA NATURE: Allocated Capacity (Post-allocation)  

### WHEN TO USE
- User asks how much capacity is **already allocated**
- Mentions: allocated capacity, capacity already used by market
- Border-focused, post-allocation information

### DO NOT USE IF
- User asks for nominated capacity (use E01)
- User asks for capacity usage (use E06)
- User asks for offered capacity (use E02 or E05)

---

## 11.1.A - Explicit Allocations – Offered Transfer Capacity

DATA DOMAIN: Market / Transmission  
DATA NATURE: Offered Capacity (Explicit Auctions)  

### WHEN TO USE
- User asks for **explicit auction capacity**
- Mentions: explicit allocation, explicit auction, capacity auction
- Border capacity not part of implicit market coupling

### DO NOT USE IF
- User asks for implicit market coupling capacity (use E02)
- User asks for allocated or used capacity (use E04 or E06)

---

## 12.1.A - Explicit Allocations – Use of Transfer Capacity

DATA DOMAIN: Market / Transmission  
DATA NATURE: Capacity Usage  

### WHEN TO USE
- User asks how much **explicitly allocated capacity was actually used**
- Mentions: capacity usage, used capacity, utilization of allocated capacity

### DO NOT USE IF
- User asks how much capacity was offered (use E02 or E05)
- User asks for nominated capacity (use E01)

---

## 12.1.A — Explicit Allocations – Auction Revenue

DATA DOMAIN: Market / Transmission  
DATA NATURE: Financial / Revenue  

### WHEN TO USE
- User asks about **auction revenue** from capacity auctions
- Mentions: auction revenue, border revenue, capacity income

### DO NOT USE IF
- User asks for congestion income from implicit markets (use E50)
- User asks for prices (use E10)

---

## 12.1.E - Implicit Auction – Net Positions

DATA DOMAIN: Market  
DATA NATURE: Net Position (Import / Export)  

### WHEN TO USE
- User asks if an area was **net importer or exporter**
- Mentions: net position, net import, net export
- Single area focus (not directional flows)

### DO NOT USE IF
- User asks for physical flows between areas (use E20)
- User asks for prices (use E10)

---

## 11.1 - Continuous Allocations – Offered Transfer Capacity

DATA DOMAIN: Market / Transmission  
DATA NATURE: Offered Capacity (Continuous Intraday)  

### WHEN TO USE
- User asks for **continuous intraday capacity**
- Mentions: continuous market, XBID, SIDC, intraday continuous capacity

### DO NOT USE IF
- User asks for day-ahead capacity (use E02)
- User asks for explicit auctions (use E05)

---

## 12.1.D - Day-ahead Energy Prices

DATA DOMAIN: Prices  
DATA NATURE: Day-ahead  

### WHEN TO USE
- User asks for **electricity prices**
- Mentions: day-ahead prices, spot prices, market prices
- Single bidding zone price information

### DO NOT USE IF
- User asks for imbalance prices (use E26)
- User asks for balancing energy prices (use E30)
- User asks for capacity or flows (use E01–E09 or E20)

# Load — Electricity Consumption & Demand (Chapter 3)

---

## 6.1.A - Actual Total Load

DATA DOMAIN: Load  
DATA NATURE: Actual / Realised  

### WHEN TO USE
- User asks for **actual electricity demand or consumption**
- Mentions: actual load, realised load, demand, consumption
- Historical or past periods (yesterday, last week, last year)
- User says “historical load” or “actual load”

### DO NOT USE IF
- User asks for any kind of forecast (use E12, E13, or E15)
- User asks for margins between load and generation (use forecast margin endpoint)

---

## 6.1.B - Day-ahead Total Load Forecast

DATA DOMAIN: Load  
DATA NATURE: Forecast (Day-ahead)  

### WHEN TO USE
- User asks for **expected load tomorrow**
- Mentions: day-ahead load forecast, expected demand tomorrow
- Short-term forward-looking demand

### DO NOT USE IF
- User asks for actual / realised load (use E11)
- User asks for week-ahead or longer forecasts (use E13 or E15)

---

## E13 — Week-ahead Total Load Forecast (6.1.C)

DATA DOMAIN: Load  
DATA NATURE: Forecast (Week-ahead)  

### WHEN TO USE
- User asks for **load forecast for the coming week**
- Mentions: week-ahead forecast, weekly load forecast

### DO NOT USE IF
- User asks for day-ahead forecast (use E12)
- User asks for year-ahead or long-term forecast (use E15)
- User asks for actual load (use E11)

---

## 6.1.E - Year-ahead Total Load Forecast

DATA DOMAIN: Load  
DATA NATURE: Forecast (Year-ahead / Long-term)  

### WHEN TO USE
- User asks for **long-term or yearly load forecast**
- Mentions: year-ahead forecast, annual demand forecast
- Structural or planning-oriented demand questions

### DO NOT USE IF
- User asks for short-term forecasts (use E12 or E13)
- User asks for actual / historical load (use E11)

---

## 6.1.A - Actual Total Load (Additional Countries)

DATA DOMAIN: Load  
DATA NATURE: Actual / Realised  

### WHEN TO USE
- Same intent as **E11**
- User asks for actual load **in countries or zones where E11 examples are sparse**
- Typically used as a fallback when E11 returns no data

### DO NOT USE IF
- User asks for forecasts (use E12, E13, or E15)
- User asks for margins or generation-related data

### ROUTING NOTE
- Prefer **E11** first
- Use **E51 only if E11 is known to be sparse for the requested area**

---

## Router Disambiguation Rules for Load

- If the user says **“actual”, “realised”, “historical”** → E11
- If the user says **“forecast”**:
  - “tomorrow” → E12
  - “next week” → E13
  - “next year / long-term” → E15
- If no time qualifier is given, **prefer E11**

# Generation — Electricity Production & Capacity (Chapter 4)

---

## 14.1.A — Installed Capacity per Production Type

DATA DOMAIN: Generation  
DATA NATURE: Structural / Installed Capacity  

### WHEN TO USE
- User asks for **installed generation capacity**
- Mentions: installed capacity, generation capacity, capacity by fuel type
- Structural, planning, or long-term questions
- No specific time resolution required beyond yearly

### DO NOT USE IF
- User asks for actual electricity production (use 16.1.A or 16.1.B/C)
- User asks for generation forecasts (use 14.1.C or 14.1.D)

---

## 16.1.A — Actual Generation per Generation Unit

DATA DOMAIN: Generation  
DATA NATURE: Actual / Realised  
DATA GRANULARITY: Per generation unit (power plant level)

### WHEN TO USE
- User asks for **output of specific power plants**
- Mentions: generation unit, power plant, unit-level production
- Needs detailed, unit-by-unit generation data

### DO NOT USE IF
- User asks for aggregated generation by fuel type (use 16.1.B / 16.1.C)
- User asks for generation forecasts (use 14.1.C or 14.1.D)

---

## 16.1.B / 16.1.C — Actual Generation per Production Type

DATA DOMAIN: Generation  
DATA NATURE: Actual / Realised  
DATA GRANULARITY: Aggregated by production type  

### WHEN TO USE
- User asks for **generation mix**
- Mentions: solar generation, wind generation, nuclear generation, gas generation
- Wants aggregated production by fuel or technology

### DO NOT USE IF
- User asks for per-unit / per-plant data (use 16.1.A)
- User asks for generation forecasts (use 14.1.C or 14.1.D)

---

## 14.1.C — Generation Forecast (Day-ahead)

DATA DOMAIN: Generation  
DATA NATURE: Forecast (Day-ahead)  

### WHEN TO USE
- User asks for **expected electricity generation tomorrow**
- Mentions: generation forecast, day-ahead generation, scheduled generation
- Short-term forward-looking generation across all technologies

### DO NOT USE IF
- User asks for actual / realised generation (use 16.1.A or 16.1.B/C)
- User asks specifically for wind or solar forecasts (use 14.1.D)

---

## 14.1.D — Wind and Solar Generation Forecast

DATA DOMAIN: Generation  
DATA NATURE: Forecast (Renewables only)  

### WHEN TO USE
- User asks specifically for **wind forecast**, **solar forecast**, or **renewable generation forecast**
- Mentions: wind forecast, solar forecast, renewable forecast
- Focused on intermittent renewable sources only

### DO NOT USE IF
- User asks for total generation forecast across all technologies (use 14.1.C)
- User asks for actual renewable generation (use 16.1.B / 16.1.C)

---

## 16.1.B / 16.1.C — Actual Generation per Production Type (Additional Countries)

DATA DOMAIN: Generation  
DATA NATURE: Actual / Realised  
DATA GRANULARITY: Aggregated by production type  

### WHEN TO USE
- Same intent as **16.1.B / 16.1.C**
- Used for countries or zones where standard examples are sparse
- User asks for generation mix in additional or less-covered countries

### DO NOT USE IF
- User asks for forecasts (use 14.1.C or 14.1.D)
- User asks for per-unit generation (use 16.1.A)

### ROUTING NOTE
- Prefer **16.1.B / 16.1.C** first
- Use this fallback only if standard requests are known to return no data

---

## 14.1.D — Wind and Solar Forecast (Additional Countries)

DATA DOMAIN: Generation  
DATA NATURE: Forecast (Renewables only)  

### WHEN TO USE
- Same intent as **14.1.D**
- Used for countries or zones where wind/solar forecast data is sparse
- User asks for renewable forecasts in additional countries

### DO NOT USE IF
- User asks for actual renewable generation (use 16.1.B / 16.1.C)
- User asks for total generation forecast (use 14.1.C)

### ROUTING NOTE
- Prefer **14.1.D**
- Use fallback only if standard requests return no data

---

## Router Disambiguation Rules for Generation

- If the user says **“installed capacity”** → 14.1.A
- If the user says **“generation mix”** or names fuel types → 16.1.B / 16.1.C
- If the user says **“power plant” or “generation unit”** → 16.1.A
- If the user says **“forecast”**:
  - Mentions wind or solar → 14.1.D
  - Mentions total generation → 14.1.C
- If no time qualifier is given, **prefer ACTUAL over FORECAST**

# Transmission — Physical Flows, Capacities & Schedules (Chapter 5)

---

## 12.1.G — Cross-Border Physical Flows

DATA DOMAIN: Transmission  
DATA NATURE: Actual / Measured  

### WHEN TO USE
- User asks for **actual electricity flows between two areas**
- Mentions: physical flows, cross-border flows, interconnector flows
- Wants measured power flows (not scheduled, not capacity)

### DO NOT USE IF
- User asks for commercial schedules (use 12.1.F)
- User asks for capacity or transfer limits (use 11.1.A or 11.1)
- User asks for prices (use Chapter 2)

---

## 11.1.A — Forecasted Transfer Capacities

DATA DOMAIN: Transmission  
DATA NATURE: Forecast / Capacity  

### WHEN TO USE
- User asks for **NTC or ATC forecasts**
- Mentions: transfer capacity forecast, NTC forecast, ATC forecast
- Forward-looking capacity availability between two areas

### DO NOT USE IF
- User asks for actual physical flows (use 12.1.G)
- User asks for already allocated or used capacity (use Chapter 2 endpoints)
- User asks for intraday continuous capacity (use 11.1)

---

## 11.1 — Offered Transfer Capacity (Implicit / Continuous)

DATA DOMAIN: Transmission  
DATA NATURE: Offered Capacity  

### WHEN TO USE
- User asks how much capacity is **offered to the market**
- Mentions: offered capacity, available capacity, ATC, NTC
- Context is implicit allocation or continuous intraday trading

### DO NOT USE IF
- User asks for explicit auctions (use Chapter 2 explicit allocation articles)
- User asks for actual flows (use 12.1.G)
- User asks for forecasts (use 11.1.A)

---

## 12.1.F — Commercial Schedules

DATA DOMAIN: Transmission  
DATA NATURE: Scheduled / Commercial  

### WHEN TO USE
- User asks for **scheduled commercial exchanges**
- Mentions: commercial schedules, scheduled exchanges, nominations
- Wants what was scheduled, not what physically flowed

### DO NOT USE IF
- User asks for actual physical flows (use 12.1.G)
- User asks for nominated capacity totals (use 12.1.B)
- User asks for prices (use Chapter 2)

---

## 11.3 — DC Links / Intraday Transfer Limits

DATA DOMAIN: Transmission  
DATA NATURE: Capacity (HVDC / DC Links)  

### WHEN TO USE
- User asks about **HVDC links or DC interconnectors**
- Mentions: DC link, HVDC, intraday transfer limits
- Capacity constraints specific to DC infrastructure

### DO NOT USE IF
- User asks for AC interconnector capacity (use 11.1 or 11.1.A)
- User asks for physical flows (use 12.1.G)

## 13.1.A — Redispatching (Internal)

DATA DOMAIN: Transmission  
DATA NATURE: Congestion Management / Operational  

### WHEN TO USE
- User asks about **internal redispatching actions**
- Mentions: redispatching, internal congestion management
- Wants information on actions taken **within a single control area**
- Focus is on relieving internal grid congestion

### DO NOT USE IF
- User asks about cross-border redispatching (use 13.1.A — Cross-Border)
- User asks about costs only (use 13.1.C)
- User asks about countertrading (use 13.1.B)

---

## 13.1.A — Redispatching (Cross-Border)

DATA DOMAIN: Transmission  
DATA NATURE: Congestion Management / Operational  

### WHEN TO USE
- User asks about **redispatching involving multiple areas**
- Mentions: cross-border redispatching, international redispatch
- Focus is on congestion management actions affecting borders

### DO NOT USE IF
- User asks only about internal redispatching (use 13.1.A — Internal)
- User asks about costs only (use 13.1.C)
- User asks about countertrading (use 13.1.B)

---

## 13.1.B — Countertrading

DATA DOMAIN: Transmission  
DATA NATURE: Congestion Management / Market-based  

### WHEN TO USE
- User asks about **countertrading actions**
- Mentions: countertrading, market-based congestion management
- Wants information on trades executed to relieve congestion

### DO NOT USE IF
- User asks about redispatching actions (use 13.1.A)
- User asks only for costs (use 13.1.C)
- User asks about physical flows or schedules

---

## 13.1.C — Costs of Congestion Management

DATA DOMAIN: Transmission  
DATA NATURE: Financial / Cost  

### WHEN TO USE
- User asks about **costs incurred for congestion management**
- Mentions: congestion costs, redispatching costs, countertrading costs
- Focus is on financial impact, not operational actions

### DO NOT USE IF
- User asks about the redispatching or countertrading actions themselves
- User asks for congestion income (use Chapter 2 — 12.1.E)
- User asks for prices or tariffs

---

## 9.1 — Expansion and Dismantling Projects

DATA DOMAIN: Transmission  
DATA NATURE: Infrastructure / Structural  

### WHEN TO USE
- User asks about **grid expansion or dismantling projects**
- Mentions: new transmission lines, grid reinforcement, dismantling
- Long-term infrastructure development questions

### DO NOT USE IF
- User asks about operational congestion management (use 13.1.A / 13.1.B)
- User asks about current physical flows or capacities
- User asks about prices or market outcomes

---

## Router Disambiguation Rules for Transmission

- If the user says **“physical flow”** → 12.1.G
- If the user says **“scheduled” or “commercial”** → 12.1.F
- If the user says **“nominated capacity”** → 12.1.B
- If the user says **“capacity forecast”** → 11.1.A
- If the user says **“available / offered capacity”** → 11.1
- If the user says **“HVDC / DC link”** → 11.3
- If unsure between schedules vs flows, **prefer PHYSICAL FLOWS (12.1.G)**
- If the user says **“redispatching”**:
  - Mentions internal only → 13.1.A (Internal)
  - Mentions borders or multiple countries → 13.1.A (Cross-Border)
- If the user says **“countertrading”** → 13.1.B
- If the user says **“costs”** together with congestion, redispatching, or countertrading → 13.1.C
- If the user says **“grid expansion” or “infrastructure projects”** → 9.1

# Outages — Unavailability of Generation, Production & Transmission (Chapter 6)

---

## 15.1.A / 15.1.B — Unavailability of Generation Units

DATA DOMAIN: Outages  
DATA NATURE: Planned / Forced Unavailability  
AFFECTED ASSET: Generation Units (power plants)

### WHEN TO USE
- User asks about **power plant outages**
- Mentions: generation outage, plant outage, unit unavailability
- Wants planned or forced outages of generation units
- Focus is on availability status, not production values

### DO NOT USE IF
- User asks about production units instead of generation units (use 15.1.C / 15.1.D)
- User asks about transmission line outages (use 10.1.A / 10.1.B)
- User asks for actual generation values (use Chapter 4)

---

## 15.1.C / 15.1.D — Unavailability of Production Units

DATA DOMAIN: Outages  
DATA NATURE: Planned / Forced Unavailability  
AFFECTED ASSET: Production Units (aggregated or logical units)

### WHEN TO USE
- User asks about **production unit unavailability**
- Mentions: production unit outage, generator unavailability
- Wants outage information at production-unit level (not individual plants)

### DO NOT USE IF
- User asks for generation unit (power plant) outages (use 15.1.A / 15.1.B)
- User asks for transmission outages (use 10.1.A / 10.1.B)
- User asks for generation output data (use Chapter 4)

---

## 10.1.A / 10.1.B — Unavailability of Transmission Infrastructure

DATA DOMAIN: Outages  
DATA NATURE: Planned / Forced Unavailability  
AFFECTED ASSET: Transmission Infrastructure

### WHEN TO USE
- User asks about **grid outages**
- Mentions: transmission outage, line outage, grid maintenance
- Wants information on unavailable transmission infrastructure

### DO NOT USE IF
- User asks for generation or production outages (use 15.1.x)
- User asks for congestion management actions (use Chapter 5)
- User asks for physical flows or capacities (use Chapter 5)

---

## 10.1.C — Unavailability of Offshore Grid Infrastructure

DATA DOMAIN: Outages  
DATA NATURE: Planned / Forced Unavailability  
AFFECTED ASSET: Offshore Grid Infrastructure

### WHEN TO USE
- User asks about **offshore grid outages**
- Mentions: offshore grid, offshore transmission, offshore maintenance
- Specific focus on offshore infrastructure

### DO NOT USE IF
- User asks about onshore transmission outages (use 10.1.A / 10.1.B)
- User asks about generation outages (use 15.1.x)

---

## Router Disambiguation Rules for Outages

- If the user says **“outage” or “unavailability”**, always check the asset type:
  - Power plant / unit → 15.1.A / 15.1.B
  - Production unit → 15.1.C / 15.1.D
  - Transmission line / grid → 10.1.A / 10.1.B
  - Offshore grid → 10.1.C
- If the user asks for **effects or costs**, do NOT use Chapter 6 (use Chapter 5)
- If the user asks for **actual production or flows**, do NOT use Chapter 6

# Balancing — System Balancing, Imbalances, Bids, Reserves (Chapter 7)

---

## 17.1.F — Prices of Activated Balancing Energy (7.4.1)

DATA DOMAIN: Balancing  
DATA NATURE: Prices / Activated Energy  

### WHEN TO USE
- User asks for prices of activated balancing energy
- Mentions: aFRR price, mFRR price, activated balancing energy price, balancing activation price

### DO NOT USE IF
- User asks for imbalance prices (use 17.1.G)
- User asks for imbalance volumes (use 17.1.H)
- User asks for day-ahead/intraday energy prices (use Chapter 2 prices)

---

## IF aFRR 3.16 — Cross Border Marginal Prices (CBMPs) for aFRR Central Selection (7.4.2)

DATA DOMAIN: Balancing  
DATA NATURE: Cross-border Price / aFRR  

### WHEN TO USE
- User asks specifically for CBMPs / cross-border marginal prices for aFRR
- Mentions: CBMP, cross-border marginal price, aFRR central selection price

### DO NOT USE IF
- User asks for general activated balancing energy prices (use 17.1.F)
- User asks for imbalance prices (use 17.1.G)

---

## 17.1.G — Imbalance Prices (7.4.3)

DATA DOMAIN: Balancing  
DATA NATURE: Prices / Settlement  

### WHEN TO USE
- User asks for imbalance prices
- Mentions: imbalance settlement price, imbalance tariff, imbalance price

### DO NOT USE IF
- User asks for activated balancing energy prices (use 17.1.F)
- User asks for day-ahead/intraday market prices (use Chapter 2)
- User asks for imbalance volumes (use 17.1.H)

---

## 12.3.B & 12.3.C — Balancing Energy Bids (7.5.1)

DATA DOMAIN: Balancing  
DATA NATURE: Bids / Market Offers  

### WHEN TO USE
- User asks for balancing energy bids / offers
- Mentions: bids, bid ladder, bid curves, mFRR bids, aFRR bids, merit order (bids)

### DO NOT USE IF
- User asks for aggregated bids (use 12.3.E)
- User asks for activated prices (use 17.1.F)
- User asks for imbalance prices (use 17.1.G)

---

## 12.3.B & 12.3.C — Balancing Energy Bids Archives (7.5.2)

DATA DOMAIN: Balancing  
DATA NATURE: Bids / Historical Archive  

### WHEN TO USE
- User asks for archived bids, historical bid records, bid archive
- Mentions: archive, historical bids, past bids dataset

### DO NOT USE IF
- User asks for current/regular bids without archive intent (use 12.3.B & 12.3.C)
- User asks for aggregated bids (use 12.3.E)

---

## IFs mFRR 9.9; aFRR 9.6 & 9.8 — Changes to Bid Availability (7.5.3)

DATA DOMAIN: Balancing  
DATA NATURE: Availability / Status Changes  

### WHEN TO USE
- User asks about changes to bid availability or availability updates
- Mentions: bid availability changes, bid status updates, availability modifications

### DO NOT USE IF
- User asks for bids themselves (use 12.3.B & 12.3.C)
- User asks for activation prices (use 17.1.F)

---

## 12.3.E GL EB — Aggregated Balancing Energy Bids (7.5.4)

DATA DOMAIN: Balancing  
DATA NATURE: Aggregated Bids / Market Summary  

### WHEN TO USE
- User asks for aggregated bids / aggregated merit order
- Mentions: aggregated bids, aggregated merit order, total bid volume by price

### DO NOT USE IF
- User asks for individual bids (use 12.3.B & 12.3.C)
- User asks for bid archives specifically (use bids archives)

---

## IFs aFRR 3.4 & mFRR 3.4 — Elastic Demands (7.5.5)

DATA DOMAIN: Balancing  
DATA NATURE: Demand / Elastic Demand  

### WHEN TO USE
- User asks for elastic demand in balancing context
- Mentions: elastic demand, demand curves, flexible demand participation

### DO NOT USE IF
- User asks for bids (use 12.3.B & 12.3.C or 12.3.E)
- User asks for imbalance volumes/prices

---

## IFs 3.10, 3.16 & 3.17 — Netted and Exchanged Volumes (7.6.1)

DATA DOMAIN: Balancing  
DATA NATURE: Cross-border Volumes / Netting & Exchange  

### WHEN TO USE
- User asks for netted volumes, exchanged volumes, imbalance netting volumes
- Mentions: netting, exchanged volumes, cross-border exchange in balancing

### DO NOT USE IF
- User asks per-border breakdown (use 7.6.2)
- User asks for imbalance volumes total (use 17.1.H)

---

## IFs 3.10, 3.16 & 3.17 — Netted and Exchanged Volumes per Border (7.6.2)

DATA DOMAIN: Balancing  
DATA NATURE: Cross-border Volumes / Per Border  

### WHEN TO USE
- User asks for netted/exchanged volumes *per border*
- Mentions: per border, per interconnector, border breakdown

### DO NOT USE IF
- User asks totals (use 7.6.1)
- User asks for physical flows (use Chapter 5 physical flows)

---

## 17.1.H — Total Imbalance Volumes (7.6.3)

DATA DOMAIN: Balancing  
DATA NATURE: Volumes / Imbalance  

### WHEN TO USE
- User asks for imbalance volumes
- Mentions: total imbalance volume, system imbalance volume, imbalance quantity

### DO NOT USE IF
- User asks for imbalance prices (use 17.1.G)
- User asks for activated balancing volumes (different dataset)
- User asks for flows (Chapter 5)

---

## 12.3.A GL EB — Current Balancing State / Area Control Error (7.6.4)

DATA DOMAIN: Balancing  
DATA NATURE: Real-time System State / ACE  

### WHEN TO USE
- User asks for ACE or balancing state
- Mentions: area control error, ACE, current balancing state

### DO NOT USE IF
- User asks for prices or volumes (use the relevant 17.1.x sections)

---

## 17.1.B & 17.1.C — Volumes and Prices of Contracted Reserves (7.7.1)

DATA DOMAIN: Balancing  
DATA NATURE: Reserves / Contracted (Prices + Volumes)  

### WHEN TO USE
- User asks about contracted reserves and their prices/volumes
- Mentions: contracted reserves, reserve contracting, reserve procurement price, reserve contracted volume

### DO NOT USE IF
- User asks for activated energy prices (use 17.1.F)
- User asks for procured balancing capacity (use 12.3.F)

---

## 12.3.F GL EB — Procured Balancing Capacity (7.7.2)

DATA DOMAIN: Balancing  
DATA NATURE: Capacity / Procured  

### WHEN TO USE
- User asks how much balancing capacity was procured
- Mentions: procured capacity, procured aFRR/mFRR capacity, balancing capacity procurement

### DO NOT USE IF
- User asks for contracted reserve prices/volumes (use 17.1.B & 17.1.C)
- User asks for activated energy (use 17.1.F)

---

## 187.2 SO GL — FCR Total Capacity (7.8.1)

DATA DOMAIN: Balancing  
DATA NATURE: Capacity / FCR  

### WHEN TO USE
- User asks for total FCR capacity
- Mentions: FCR total capacity, frequency containment reserve total

### DO NOT USE IF
- User asks for shares of FCR (use 7.8.2)
- User asks for sharing between synchronous areas (use 7.8.3)

---

## 187.2 SO GL — Shares of FCR Capacity (7.8.2)

DATA DOMAIN: Balancing  
DATA NATURE: Capacity / FCR Shares  

### WHEN TO USE
- User asks for shares/allocations of FCR capacity (per area/participant grouping)
- Mentions: share of FCR, FCR shares, contribution shares

### DO NOT USE IF
- User asks total FCR capacity only (use 7.8.1)

---

## 190.2 SO GL — Sharing of FCR between Synchronous Areas (7.8.3)

DATA DOMAIN: Balancing  
DATA NATURE: Cross-area Sharing / FCR  

### WHEN TO USE
- User asks about FCR sharing between synchronous areas
- Mentions: synchronous area sharing, cross-area FCR sharing

### DO NOT USE IF
- User asks total FCR capacity or shares within one area (use 7.8.1 / 7.8.2)

---

## 188.3 & 189.2 SO GL — FRR & RR Capacity Outlook (7.9.1)

DATA DOMAIN: Balancing  
DATA NATURE: Forecast / Outlook (FRR & RR Capacity)  

### WHEN TO USE
- User asks for outlook/forecast of FRR and/or RR capacity
- Mentions: outlook, forecast, expected FRR capacity, expected RR capacity

### DO NOT USE IF
- User asks actual realized capacity (use 7.9.2)

---

## 188.4 & 189.3 SO GL — FRR and RR Actual Capacity (7.9.2)

DATA DOMAIN: Balancing  
DATA NATURE: Actual / Realised Capacity (FRR & RR)  

### WHEN TO USE
- User asks for actual FRR/RR capacity
- Mentions: actual FRR capacity, actual RR capacity, realized reserve capacity

### DO NOT USE IF
- User asks outlook/forecast (use 7.9.1)

---

## 12.3.H & 12.3.I — Allocation and Use of Cross-Zonal Balancing Capacity (7.10.1)

DATA DOMAIN: Balancing  
DATA NATURE: Cross-zonal Capacity / Allocation & Use  

### WHEN TO USE
- User asks about allocation/use of cross-zonal balancing capacity
- Mentions: cross-zonal balancing capacity, allocation, use, CZBC

### DO NOT USE IF
- User asks about capacity limitations (use 7.10.2)
- User asks physical flows (Chapter 5)

---

## IFs 4.3 & 4.4 — Balancing Border Capacity Limitations (7.10.2)

DATA DOMAIN: Balancing  
DATA NATURE: Constraints / Limitations  

### WHEN TO USE
- User asks about limitations/constraints on balancing border capacity
- Mentions: border capacity limitations, constraints, limitation rules

### DO NOT USE IF
- User asks about allocation and use (use 12.3.H & 12.3.I)

---

## 17.1.I — Financial Expenses and Income for Balancing (7.11.1)

DATA DOMAIN: Balancing  
DATA NATURE: Financial / Expenses & Income  

### WHEN TO USE
- User asks about balancing financials
- Mentions: financial expenses, income, balancing costs, balancing revenues

### DO NOT USE IF
- User asks about congestion income (use Chapter 2 congestion income)
- User asks for activation prices/volumes (use 17.1.F / 17.1.E)

---

## 185.4 SO GL — Results of Criteria Application Process - Measurements (7.11.2)

DATA DOMAIN: Balancing  
DATA NATURE: Compliance / Measurement Results  

### WHEN TO USE
- User asks for results of criteria application process measurements
- Mentions: criteria application process, measurements, compliance measurement results

### DO NOT USE IF
- User asks for prices/volumes/capacity (use the relevant 17.1 / 12.3 / SO GL sections)

---

## Router Disambiguation Rules for Balancing (Chapter 7)

- If user says **imbalance**:
  - prices → 17.1.G
  - volumes → 17.1.H
- If user says **activated balancing energy**:
  - prices → 17.1.F
- If user says **CBMP / cross-border marginal price / aFRR central selection** → IF aFRR 3.16
- If user says **bids**:
  - individual bids → 12.3.B & 12.3.C
  - bid archives → 12.3.B & 12.3.C (Archives)
  - aggregated bids / merit order summary → 12.3.E
- If user says **ACE / balancing state** → 12.3.A
- If user says **procured balancing capacity** → 12.3.F
- If user says **contracted reserves prices/volumes** → 17.1.B & 17.1.C
- If user says **FCR**:
  - total → 187.2 (Total)
  - shares → 187.2 (Shares)
  - sharing between synchronous areas → 190.2
- If user says **FRR/RR outlook** → 188.3 & 189.2
- If user says **FRR/RR actual** → 188.4 & 189.3
- If user says **cross-zonal balancing capacity**:
  - allocation/use → 12.3.H & 12.3.I
  - limitations → IFs 4.3 & 4.4
- If user says **balancing financials** → 17.1.I
- If user says **criteria application process measurements** → 185.4

# Master Data — Production & Generation Units (Chapter 8)

---

## 8.2.1 — Production and Generation Units

DATA DOMAIN: Master Data  
DATA NATURE: Configuration / Reference Data  
RESPONSE TYPE: XML (Configuration_MarketDocument)

### WHEN TO USE
- User asks for a list of **production units** / **generation units**
- Mentions: “unit registry”, “list of plants”, “unit EIC codes”, “registered units”
- User wants metadata like unit names, identifiers, technology (psrType), nominal power, etc.
- User wants to cross-reference unit identifiers with other datasets (e.g., generation)

### DO NOT USE IF
- User asks for **actual generation values** (use Generation domain Chapter 4, e.g., 16.1.*)
- User asks for **outages** of units (use Outages domain Chapter 6, 15.1.* / 10.1.*)
- User asks for **installed capacity time series** (use Generation domain, e.g., 14.1.*)

### ROUTING NOTES
- This endpoint returns configuration data for commissioned units in a bidding zone on a specific date.
- The API documentation defines it with:
  - `documentType = A95` (Configuration document)
  - `businessType = B11` (Production unit)
  - mandatory zone + implementation date
  - optional `psrType` filter

---

# OMI — Other Market Information (Chapter 9)

---

## 9.2.1 — Other Market Information

DATA DOMAIN: OMI  
DATA NATURE: Announcements / Notifications / Events  
RESPONSE TYPE: ZIP containing XML documents (OtherTransparencyMarketInformation_MarketDocument)

### WHEN TO USE
- User asks for **market information announcements** that don’t fit other domains
- Mentions: “market notice”, “announcement”, “notification”, “event”, “other transparency info”
- Often used for infrastructure delays, operational notices, market events (as published documents)

### DO NOT USE IF
- User asks for prices, flows, load, generation, outages, balancing datasets (use those domains)
- User asks specifically for “grid expansion/dismantling projects” (that’s 9.1 in Transmission chapter, not OMI)

### ROUTING NOTES
- The documentation specifies:
  - response is a **ZIP file with XML documents**
  - up to **200 documents per request**
- Mandatory parameters include:
  - `documentType = B47` (Other market information)
  - `ControlArea_Domain`
  - `periodStart`, `periodEnd`
- Useful optional filters:
  - `DocStatus` (A05 Active / A09 Cancelled / A13 Withdrawn)
  - update-window filters (`PeriodStartUpdate`, `PeriodEndUpdate`)
  - `Offset` pagination
  - `mRID` to query versions of a specific event

---
