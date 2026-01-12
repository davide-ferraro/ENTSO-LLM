# Natural Language Request Examples

> Copy these examples when asking the LLM to fetch ENTSO-E data.

---

## 🔌 Load & Consumption

**Local (one-time)**
- Get actual load data for France for the last week
- Show me day-ahead load forecast for Germany
- Fetch total consumption in Spain for January 2025
- Get the load forecast error for Belgium yesterday

**Historical (20 years)**
- Get historical load data for France
- I need all historical consumption data for Italy
- Fetch the complete load history for the Netherlands

**Modal (scheduled)**
- Set up a cron job to monitor load in Germany every 2 hours
- Track French electricity consumption every hour
- Create a scheduled fetch for UK load data every 6 hours

---

## ☀️ Renewable Generation

**Local (one-time)**
- Get solar generation in Spain for the last week
- Show me wind power output in Germany yesterday
- Fetch offshore wind generation in Denmark for December
- Get all renewable generation by type in Portugal

**Historical (20 years)**
- Get historical solar generation for Spain
- I need 20 years of wind generation data for Germany
- Fetch complete historical renewable generation for France

**Modal (scheduled)**
- Monitor solar generation in Spain every 2 hours
- Set up hourly tracking of wind power in Germany
- Create a cron job for offshore wind in Denmark every 6 hours

---

## ⚛️ Conventional Generation

**Local (one-time)**
- Get nuclear generation in France for the last month
- Show me gas-fired power output in the Netherlands
- Fetch coal generation in Poland for this week
- Get generation by fuel type in Belgium

**Historical (20 years)**
- Get historical nuclear generation for France
- I need all historical gas generation data for Germany

**Modal (scheduled)**
- Track nuclear output in France every hour
- Monitor gas generation in Netherlands every 2 hours

---

## 💶 Day-Ahead Prices

**Local (one-time)**
- Get day-ahead prices for Germany for the last week
- Show me electricity prices in France yesterday
- Fetch day-ahead prices for all Nordic countries
- Get price data for Italy North zone

**Historical (20 years)**
- Get historical day-ahead prices for Germany
- I need 20 years of electricity price data for Spain
- Fetch complete price history for France

**Modal (scheduled)**
- Monitor day-ahead prices in Germany every hour
- Track electricity prices in France every 2 hours
- Set up daily price monitoring for Spain

---

## 🔀 Cross-Border Flows

**Local (one-time)**
- Get physical flows from France to Germany
- Show me cross-border flows between Spain and Portugal
- Fetch scheduled exchanges from Netherlands to Belgium
- Get all flows on the NordLink cable (Norway-Germany)

**Historical (20 years)**
- Get historical cross-border flows between France and Germany
- I need 20 years of flow data for the Spain-France interconnector

**Modal (scheduled)**
- Monitor France-Germany flows every hour
- Track Spain-Portugal exchanges every 2 hours

---

## ⚡ Balancing & Reserves

**Local (one-time)**
- Get the current Area Control Error (ACE) for the Netherlands
- Show me aFRR activation prices in Germany for yesterday
- Fetch mFRR activated energy volumes in Austria for the last 3 days
- Get cross-border balancing energy exchanges between France and Spain
- Show me imbalance prices for Finland this week

**Historical (20 years)**
- Get historical imbalance prices for Germany
- I need all historical balancing data for the Netherlands

**Modal (scheduled)**
- Monitor imbalance prices in Germany every 15 minutes
- Track ACE data for Netherlands every hour

---

## 📊 Capacity & Infrastructure

**Local (one-time)**
- Show me installed generation capacity by fuel type in Poland
- Get the planned expansion and dismantling of generation units in Italy
- What's the total transfer capacity between Norway and Sweden?
- Fetch net transfer capacity day-ahead for the France-UK interconnector
- Get transmission capacity between Germany and Austria

**Historical (20 years)**
- Get historical installed capacity data for Germany
- I need 20 years of transfer capacity data for France borders

---

## 🚧 Outages & Unavailability

**Local (one-time)**
- Get planned outages for generation units in Germany
- Show me transmission unavailability in France
- Fetch forced outages in Spain for the last month
- Get offshore grid unavailability in the North Sea

**Modal (scheduled)**
- Monitor generation outages in Germany every 6 hours
- Track transmission unavailability in France daily

---

## 🌊 Hydro & Reservoirs

**Local (one-time)**
- Get water reservoir filling levels in Norway
- Show me hydro pump consumption in Austria
- Fetch run-of-river generation in Switzerland
- Get hydro reservoir generation in Sweden

**Historical (20 years)**
- Get historical hydro generation for Norway
- I need all historical reservoir data for Switzerland

---

## 💰 Markets & Congestion

**Local (one-time)**
- Get congestion income from explicit auctions between Italy and Slovenia
- Show me day-ahead prices for all Italian bidding zones
- Fetch intraday continuous market prices for the Nordic region
- Get auction results for the Germany-Netherlands border

---

## 📋 Master Data

**Local (one-time)**
- List all production units registered in Spain
- Get the master data for generation units in the Czech Republic
- Show me all registered power plants in Germany
- Fetch the list of generation units in France

---

## 🔮 Forecasts (Various Horizons)

**Local (one-time)**
- Get the week-ahead load forecast for Portugal
- Show me the month-ahead wind generation forecast for Denmark
- Fetch year-ahead total load forecast for Germany
- Get day-ahead solar forecast for Spain
- Show me intraday wind forecast for the UK

---

## 🌍 Cross-Border (Unusual Pairs)

**Local (one-time)**
- Get physical flows between Lithuania and Poland
- Show me scheduled commercial exchanges between Hungary and Romania
- Fetch DC link scheduled flows on the NorNed cable (Norway-Netherlands)
- Get flows between Greece and Bulgaria
- Show me Switzerland to Italy cross-border exchanges

---

## ⏰ Modal Cron Job Examples

### Every Hour
- Monitor load in Germany every hour
- Track day-ahead prices in France hourly
- Set up hourly solar generation monitoring for Spain

### Every 2 Hours
- Create a cron job for wind generation in Germany every 2 hours
- Monitor cross-border flows France-Germany every 2 hours
- Track imbalance prices in Netherlands every 2 hours

### Every 6 Hours
- Set up 6-hourly monitoring of nuclear generation in France
- Track total generation mix in Spain every 6 hours

### Daily
- Monitor generation outages in Germany once per day
- Track daily capacity changes in Italy
- Set up daily price summary collection for all Nordic zones

### Every 15 Minutes
- Track real-time ACE data for Germany every 15 minutes
- Monitor balancing energy activation every 15 minutes

---

## 🏭 Specific Use Cases

### Energy Trading
- Get day-ahead prices and load forecast for Germany for tomorrow
- Show me price spreads between France and Germany
- Fetch all data needed for cross-border arbitrage analysis

### Grid Operations
- Monitor generation outages and flows for France
- Track transmission capacity and congestion for German borders
- Get real-time balancing data for the Netherlands

### Renewable Integration
- Track solar and wind generation alongside load in Spain
- Monitor renewable forecast errors in Germany
- Get renewable curtailment data for Denmark

### Market Analysis
- Collect historical prices for all major European markets
- Track price convergence between coupled markets
- Monitor auction results for key interconnectors

---

*Tip: For historical requests, the system automatically fetches 20 years of data and merges it into a single file.*
