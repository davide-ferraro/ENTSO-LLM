#### 3.4.1 Actual Total Load (6.1.A) - GET Method

Returns realized/actual total electricity load for a bidding zone.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one MTU (Market Time Unit) period

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A65` | System total load |
| `processType` | **[M]** | `A16` | Realised |
| `outBiddingZone_Domain` | **[M]** | EIC Code | Control Area, Bidding Zone, or Country |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A16&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202303030000&periodEnd=202303060000'
```

**Response Structure:**
```xml
<GL_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0">
    <mRID>...</mRID>
    <type>A65</type>
    <process.processType>A16</process.processType>
    <TimeSeries>
        <businessType>A04</businessType>
        <outBiddingZone_Domain.mRID>10YCZ-CEPS-----N</outBiddingZone_Domain.mRID>
        <quantity_Measure_Unit.name>MAW</quantity_Measure_Unit.name>
        <Period>
            <resolution>PT60M</resolution>
            <Point>
                <position>1</position>
                <quantity>7146</quantity>
            </Point>
            ...
        </Period>
    </TimeSeries>
</GL_MarketDocument>
```

- Resolution: `PT60M` (hourly) or `PT15M`/`PT30M` depending on country
- `businessType`: `A04` (Base load)
- `objectAggregation`: `A01` (Area)

---
