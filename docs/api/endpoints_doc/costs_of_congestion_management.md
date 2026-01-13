#### 5.3.6 Costs of Congestion Management (13.1.C)

Returns monthly aggregated costs associated with congestion management activities.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response Document** | `TransmissionNetwork_MarketDocument` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A92` | Congestion costs |
| `out_Domain` | **[M]** | EIC Code | Control Area |
| `in_Domain` | **[M]** | EIC Code | Control Area (same as out_Domain) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A92&out_Domain=10YBE----------2&in_Domain=10YBE----------2&periodStart=202112312300&periodEnd=202212312300'
```

**Response Structure:**
- Resolution: `P1M` (monthly)
- `currency_Unit.name`: `EUR`
- Returns `congestionCost_Price.amount` instead of quantity
- Multiple TimeSeries with different `businessType` values:
  - `A46` = System Operator re-dispatching costs
  - `B03` = Redispatching costs
  - `B04` = Countertrading costs

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>A46</businessType>
    <in_Domain.mRID codingScheme="A01">10YBE----------2</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YBE----------2</out_Domain.mRID>
    <currency_Unit.name>EUR</currency_Unit.name>
    <curveType>A01</curveType>
    <Period>
        <timeInterval>
            <start>2021-12-31T23:00Z</start>
            <end>2022-01-31T23:00Z</end>
        </timeInterval>
        <resolution>P1M</resolution>
        <Point>
            <position>1</position>
            <congestionCost_Price.amount>0.00</congestionCost_Price.amount>
        </Point>
    </Period>
</TimeSeries>
```

---
