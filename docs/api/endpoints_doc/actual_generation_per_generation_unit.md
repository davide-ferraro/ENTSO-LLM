#### 4.4.4 Actual Generation per Generation Unit (16.1.A)

Returns actual generation data for individual generation units (power plants).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Request Limits:**
- Maximum time interval: 1 day
- Minimum time interval: 1 Market Time Unit (MTU)

**Important Notes:**
- `inBiddingZone_Domain` = **Generation** values
- `outBiddingZone_Domain` = **Consumption** values

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A73` | Actual generation |
| `processType` | **[M]** | `A16` | Realised |
| `in_Domain` | **[M]** | EIC Code | Control Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `PsrType` | [O] | Code | Production type filter |
| `RegisteredResource` | [O] | EIC Code | Specific generation unit EIC |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A73&processType=A16&in_Domain=10YBE----------2&periodStart=202308152200&periodEnd=202308162200'
```

**Response Structure:**
- Resolution: `PT60M` (hourly)
- `businessType`: `A01` (Production)
- `objectAggregation`: `A06` (Resource object)
- Each TimeSeries includes:
  - `registeredResource.mRID` - Unit EIC code
  - `MktPSRType/PowerSystemResources/name` - Plant name (e.g., "DOEL 1")
  - `MktPSRType/psrType` - Production type

**Example Response Data:**
```xml
<TimeSeries>
    <businessType>A01</businessType>
    <registeredResource.mRID codingScheme="A01">22WDOELX1000076X</registeredResource.mRID>
    <MktPSRType>
        <psrType>B14</psrType>  <!-- Nuclear -->
        <PowerSystemResources>
            <mRID codingScheme="A01">22WDOELX1150076X</mRID>
            <name>DOEL 1</name>
        </PowerSystemResources>
    </MktPSRType>
    <Period>
        <resolution>PT60M</resolution>
        <Point>
            <position>1</position>
            <quantity>439</quantity>
        </Point>
    </Period>
</TimeSeries>
```

---
