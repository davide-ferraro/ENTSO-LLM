#### 5.3.3 Commercial Schedules (12.1.F)

Returns finalized commercial schedules for cross-border energy exchanges.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A09` | Finalised schedule |
| `out_Domain` | **[M]** | EIC Code | Origin Control Area, Bidding Zone, or Country |
| `in_Domain` | **[M]** | EIC Code | Destination Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `contract_MarketAgreement.Type` | [O] | Code | A01 = Day Ahead Commercial Schedules; A05 = Total Commercial Schedules |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A09&out_Domain=10YBE----------2&in_Domain=10YFR-RTE------C&periodStart=202410312300&periodEnd=202411012300'
```

**Response Structure:**
- Resolution: `PT15M` (15-minute intervals)
- `businessType`: `A06` (Commercial exchange)
- Returns separate TimeSeries for Day-Ahead (`A01`) and Total (`A05`) schedules
- `curveType`: `A03` (Variable-sized blocks)

**Example Response Data:**
```xml
<TimeSeries>
    <mRID>1</mRID>
    <businessType>A06</businessType>
    <in_Domain.mRID codingScheme="A01">10YFR-RTE------C</in_Domain.mRID>
    <out_Domain.mRID codingScheme="A01">10YBE----------2</out_Domain.mRID>
    <contract_MarketAgreement.type>A01</contract_MarketAgreement.type>
    <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
    <curveType>A03</curveType>
    <Period>
        <resolution>PT15M</resolution>
        <Point>
            <position>1</position>
            <quantity>0</quantity>
        </Point>
    </Period>
</TimeSeries>
```

---
