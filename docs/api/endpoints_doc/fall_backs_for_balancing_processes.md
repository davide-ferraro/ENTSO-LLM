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
