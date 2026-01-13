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
