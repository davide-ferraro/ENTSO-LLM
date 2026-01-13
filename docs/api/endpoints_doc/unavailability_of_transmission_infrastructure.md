#### 6.3.4 Unavailability of Transmission Infrastructure (10.1.A&B)

Returns unavailability information for transmission infrastructure (cross-border links).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `A78` | Transmission unavailability |
| `Out_Domain` | **[M]** | EIC Code | Origin Control Area or Bidding Zone (optional if mRID present) |
| `In_Domain` | **[M]** | EIC Code | Destination Control Area or Bidding Zone (optional if mRID present) |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `BusinessType` | [O] | Code | A53 = Planned maintenance; A54 = Forced unavailability |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) |
| `mRID` | [O] | String | Document mRID - retrieves older versions |
| `offset` | [O] | Integer | Pagination offset [0-4800], returns records n+1 to n+200 |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A78&Out_Domain=10YFR-RTE------C&In_Domain=10YBE----------2&periodStart=202312012300&periodEnd=202312022300'
```

**Response Structure:**
- ZIP file with individual outage XML documents
- Each outage includes:
  - `Asset_RegisteredResource`: Transmission asset details (mRID, name, location)
  - `asset_PSRType.psrType`: Asset type (e.g., B21 = transmission line)
  - `Available_Period`: Time periods with available capacity values
  - `docStatus`: Current status (A05=Active, A09=Cancelled)

**Example Response Data:**
```xml
<Unavailability_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-6:outagedocument:3:0">
    <mRID>A47mJe5e9jml9FeSL6jfKg</mRID>
    <revisionNumber>10</revisionNumber>
    <type>A78</type>
    <docStatus>
        <value>A09</value>
    </docStatus>
    <TimeSeries>
        <businessType>A53</businessType>
        <Asset_RegisteredResource>
            <mRID codingScheme="A01">10T-BE-FR-00007U</mRID>
            <name>CHOOZ220 48 MONCE</name>
            <asset_PSRType.psrType>B21</asset_PSRType.psrType>
            <location.name>MONCEAU (B) - CHOOZ (FR) 220.48</location.name>
        </Asset_RegisteredResource>
        <Available_Period>
            <timeInterval>
                <start>2023-07-01T12:30Z</start>
                <end>2023-07-01T13:00Z</end>
            </timeInterval>
            <resolution>PT30M</resolution>
            <Point>
                <position>1</position>
                <quantity>1850</quantity>
            </Point>
        </Available_Period>
    </TimeSeries>
</Unavailability_MarketDocument>
```

---
