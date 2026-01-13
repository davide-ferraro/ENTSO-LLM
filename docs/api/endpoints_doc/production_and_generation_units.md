#### 8.2.1 Production and Generation Units

Returns configuration data for commissioned production units in a given bidding zone on a specific date.

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A95` | Configuration document |
| `businessType` | **[M]** | `B11` | Production unit |
| `BiddingZone_Domain` | **[M]** | EIC Code | Bidding Zone or Control Area |
| `Implementation_DateAndOrTime` | **[M]** | `yyyy-MM-dd` | Date (e.g., 2017-01-01) |
| `psrType` | [O] | Code | Filter by production type (B01-B20) |

**PSR Types (Production Source Types):**

| Code | Description |
|------|-------------|
| `B01` | Biomass |
| `B02` | Fossil Brown coal/Lignite |
| `B03` | Fossil Coal-derived gas |
| `B04` | Fossil Gas |
| `B05` | Fossil Hard coal |
| `B06` | Fossil Oil |
| `B07` | Fossil Oil shale |
| `B08` | Fossil Peat |
| `B09` | Geothermal |
| `B10` | Hydro Pumped Storage |
| `B11` | Hydro Run-of-river and poundage |
| `B12` | Hydro Water Reservoir |
| `B13` | Marine |
| `B14` | Nuclear |
| `B15` | Other renewable |
| `B16` | Solar |
| `B17` | Waste |
| `B18` | Wind Offshore |
| `B19` | Wind Onshore |
| `B20` | Other |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A95&businessType=B11&BiddingZone_Domain=10YBE----------2&Implementation_DateAndOrTime=2017-01-01'
```

**Example with PSR Type filter (Fossil Gas only):**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A95&businessType=B11&BiddingZone_Domain=10YBE----------2&Implementation_DateAndOrTime=2017-01-01&psrType=B04'
```

**Response Structure:**

The response contains one `TimeSeries` element per production unit with:

| Element | Description |
|---------|-------------|
| `mRID` | Unique identifier for the TimeSeries |
| `businessType` | `B11` (Production unit) |
| `implementation_DateAndOrTime.date` | Commissioning date |
| `biddingZone_Domain.mRID` | EIC code of the bidding zone |
| `registeredResource.mRID` | EIC code of the production unit |
| `registeredResource.name` | Name of the production unit |
| `registeredResource.location.name` | Location (usually country) |
| `ControlArea_Domain/mRID` | Control area EIC code |
| `Provider_MarketParticipant/mRID` | Market participant EIC code |
| `MktPSRType/psrType` | Production type code (B01-B20) |
| `MktPSRType/production_PowerSystemResources.highVoltageLimit` | Connection voltage in KVT |
| `MktPSRType/nominalIP_PowerSystemResources.nominalP` | Total nominal power in MAW |
| `GeneratingUnit_PowerSystemResources` | Individual generating units (one or more) |

**Generating Unit Details:**

Each `GeneratingUnit_PowerSystemResources` element contains:

| Element | Description |
|---------|-------------|
| `mRID` | EIC code of the generating unit |
| `name` | Name of the generating unit |
| `nominalP` | Nominal power in MAW |
| `generatingUnit_PSRType.psrType` | Production type |
| `generatingUnit_Location.name` | Location |

**Example Response Data:**
```xml
<Configuration_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:configurationdocument:3:0">
    <mRID>e52e35a2c0844e8ca98cd46999f0e39d</mRID>
    <type>A95</type>
    <process.processType>A39</process.processType>
    <TimeSeries>
        <mRID>b362105694c34556</mRID>
        <businessType>B11</businessType>
        <implementation_DateAndOrTime.date>2014-10-01</implementation_DateAndOrTime.date>
        <biddingZone_Domain.mRID codingScheme="A01">10YBE----------2</biddingZone_Domain.mRID>
        <registeredResource.mRID codingScheme="A01">22WSAINT-000221B</registeredResource.mRID>
        <registeredResource.name>SAINT-GHISLAIN STEG</registeredResource.name>
        <registeredResource.location.name>Belgium</registeredResource.location.name>
        <ControlArea_Domain>
            <mRID codingScheme="A01">10YBE----------2</mRID>
        </ControlArea_Domain>
        <Provider_MarketParticipant>
            <mRID codingScheme="A01">10X1001A1001A094</mRID>
        </Provider_MarketParticipant>
        <MktPSRType>
            <psrType>B04</psrType>
            <production_PowerSystemResources.highVoltageLimit unit="KVT">150</production_PowerSystemResources.highVoltageLimit>
            <nominalIP_PowerSystemResources.nominalP unit="MAW">350</nominalIP_PowerSystemResources.nominalP>
            <GeneratingUnit_PowerSystemResources>
                <mRID codingScheme="A01">22WSAINT-150221B</mRID>
                <name>SAINT-GHISLAIN STEG</name>
                <nominalP unit="MAW">350</nominalP>
                <generatingUnit_PSRType.psrType>B04</generatingUnit_PSRType.psrType>
                <generatingUnit_Location.name>Belgium</generatingUnit_Location.name>
            </GeneratingUnit_PowerSystemResources>
        </MktPSRType>
    </TimeSeries>
    <!-- Additional TimeSeries for other production units -->
</Configuration_MarketDocument>
```

**Example: Multi-Unit Production Facility (Pumped Storage):**
```xml
<TimeSeries>
    <mRID>d70176d8ff70447c</mRID>
    <businessType>B11</businessType>
    <registeredResource.mRID codingScheme="A01">22WCOOXII000070C</registeredResource.mRID>
    <registeredResource.name>COO II T</registeredResource.name>
    <MktPSRType>
        <psrType>B10</psrType>
        <nominalIP_PowerSystemResources.nominalP unit="MAW">690</nominalIP_PowerSystemResources.nominalP>
        <!-- Multiple generating units within the same production unit -->
        <GeneratingUnit_PowerSystemResources>
            <mRID codingScheme="A01">22WCOOX5X000061A</mRID>
            <name>COO 5 T</name>
            <nominalP unit="MAW">230</nominalP>
        </GeneratingUnit_PowerSystemResources>
        <GeneratingUnit_PowerSystemResources>
            <mRID codingScheme="A01">22WCOOX6X000064W</mRID>
            <name>COO 6 T</name>
            <nominalP unit="MAW">230</nominalP>
        </GeneratingUnit_PowerSystemResources>
        <GeneratingUnit_PowerSystemResources>
            <mRID codingScheme="A01">22WCOOX4X0000588</mRID>
            <name>COO 4 T</name>
            <nominalP unit="MAW">230</nominalP>
        </GeneratingUnit_PowerSystemResources>
    </MktPSRType>
</TimeSeries>
```

---

### 8.3 Document Types Summary

| Code | Description |
|------|-------------|
| `A95` | Configuration document |

### 8.4 Business Types in Master Data

| Code | Description |
|------|-------------|
| `B11` | Production unit |

### 8.5 Use Cases

1. **Get all production units in a bidding zone:**
   - Query without `psrType` to retrieve all commissioned units

2. **Get specific technology type:**
   - Add `psrType` parameter to filter (e.g., `psrType=B14` for nuclear)

3. **Historical analysis:**
   - Change `Implementation_DateAndOrTime` to see which units were commissioned at different dates

4. **Cross-reference with generation data:**
   - Use `registeredResource.mRID` from master data to filter actual generation queries

---

## Chapter 9: OMI (Other Market Information)

The OMI (Other Market Information) domain provides access to general market announcements and transparency information that doesn't fit into other specific categories. This includes announcements about infrastructure delays, market events, and other relevant information published by TSOs.

### 9.1 Overview

| Aspect | Details |
|--------|---------|
| **Authorization** | API Key (inherited from collection) |
| **Response Format** | XML (`OtherTransparencyMarketInformation_MarketDocument`) |
| **Namespace** | `urn:iec62325.351:tc57wg16:451-n:otmidocument:1:0` |
| **Response Type** | ZIP file containing XML documents |

### 9.2 Endpoints

---
