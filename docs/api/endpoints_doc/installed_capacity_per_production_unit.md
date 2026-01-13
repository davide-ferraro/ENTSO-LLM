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
