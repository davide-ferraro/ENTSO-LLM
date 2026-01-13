#### 9.2.1 Other Market Information

Returns other market information documents (announcements, notifications, events).

| Property | Value |
|----------|-------|
| **Method** | GET |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Response** | ZIP file with XML documents |
| **Max Results** | 200 documents per request |

**Parameters:**

| Parameter | Required | Value | Description |
|-----------|----------|-------|-------------|
| `documentType` | **[M]** | `B47` | Other market information |
| `ControlArea_Domain` | **[M]** | EIC Code | Scheduling Area |
| `periodStart` | **[M]** | `yyyyMMddHHmm` | Start datetime |
| `periodEnd` | **[M]** | `yyyyMMddHHmm` | End datetime |
| `DocStatus` | [O] | Code | A05 = Active; A09 = Cancelled; A13 = Withdrawn |
| `PeriodStartUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (start) - mandatory if period not defined |
| `PeriodEndUpdate` | [O] | `yyyyMMddHHmm` | Filter by update time (end) - mandatory if period not defined |
| `Offset` | [O] | Integer | Pagination [0-4800], returns n+1 to n+200 |
| `mRID` | [O] | String | Query individual versions of a specific event |

**Example Request:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=B47&ControlArea_Domain=10YDE-EON------1&periodStart=202409232200&periodEnd=202409242200'
```

**Example Request with Update Filter:**
```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=B47&ControlArea_Domain=10YDE-EON------1&PeriodStartUpdate=202402221000&PeriodEndUpdate=202402231200'
```

**Response Structure:**

| Element | Description |
|---------|-------------|
| `mRID` | Unique document identifier (Base64 encoded) |
| `revisionNumber` | Version number of the document |
| `type` | `B47` (Other market information) |
| `sender_MarketParticipant.mRID` | EIC code of the publishing TSO |
| `sender_MarketParticipant.marketRole.type` | `A39` (Data provider) |
| `docStatus/value` | Document status (A05, A09, A13) |
| `publication_DateAndOrTime.dateTime` | Publication timestamp |
| `start_DateAndOrTime.dateTime` | Event start time |
| `end_DateAndOrTime.dateTime` | Event end time |
| `reason.code` | Reason code (e.g., A95 = Congestion in real time) |
| `reason.text` | Human-readable description of the event |

**Example Response Data:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<OtherTransparencyMarketInformation_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-n:otmidocument:1:0">
    <mRID>ZWQ5ODdjZjZhYWFkZDA5Yzk0MThkYjUwOGMxNDgxZTk=</mRID>
    <revisionNumber>1</revisionNumber>
    <type>B47</type>
    <sender_MarketParticipant.mRID codingScheme="A01">10XDE-EON-NETZ-C</sender_MarketParticipant.mRID>
    <sender_MarketParticipant.marketRole.type>A39</sender_MarketParticipant.marketRole.type>
    <receiver_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450</receiver_MarketParticipant.mRID>
    <receiver_MarketParticipant.marketRole.type>A39</receiver_MarketParticipant.marketRole.type>
    <createdDateTime>2024-10-08T11:34:58Z</createdDateTime>
    <docStatus>
        <value>A05</value>
    </docStatus>
    <publication_DateAndOrTime.dateTime>2024-09-19T09:11:00Z</publication_DateAndOrTime.dateTime>
    <start_DateAndOrTime.dateTime>2024-09-18T10:00</start_DateAndOrTime.dateTime>
    <end_DateAndOrTime.dateTime>2025-12-15T10:59</end_DateAndOrTime.dateTime>
    <reason.code>A95</reason.code>
    <reason.text>Delay in the completion of the DolWin5 grid connection system until probably 15 December 2025</reason.text>
</OtherTransparencyMarketInformation_MarketDocument>
```

---

### 9.3 Document Types Summary

| Code | Description |
|------|-------------|
| `B47` | Other market information |

### 9.4 Document Status Codes

| Code | Description |
|------|-------------|
| `A05` | Active |
| `A09` | Cancelled |
| `A13` | Withdrawn |

### 9.5 Use Cases

1. **Get all active announcements:**
   - Use `DocStatus=A05` to filter only active events

2. **Track updates since last query:**
   - Use `PeriodStartUpdate` and `PeriodEndUpdate` to get only new/updated information

3. **Get history of a specific event:**
   - Use `mRID` parameter to retrieve all versions of a particular announcement

4. **Monitor infrastructure delays:**
   - Query specific TSO control areas for grid connection and infrastructure updates

---

## Appendix A: Quick Reference

### Example API Call (cURL)

```bash
curl --location 'https://web-api.tp.entsoe.eu/api?securityToken=YOUR_TOKEN&documentType=A65&processType=A16&outBiddingZone_Domain=10YCZ-CEPS-----N&periodStart=202308232200&periodEnd=202308242200'
```

### Common Query Patterns

**Get Actual Load for a Country**:
```
documentType=A65
processType=A16
outBiddingZone_Domain=[EIC_CODE]
periodStart=[START]
periodEnd=[END]
```

**Get Actual Generation by Type**:
```
documentType=A75
processType=A16
in_Domain=[EIC_CODE]
periodStart=[START]
periodEnd=[END]
```

**Get Day-Ahead Prices**:
```
documentType=A44
in_Domain=[EIC_CODE]
out_Domain=[EIC_CODE]
periodStart=[START]
periodEnd=[END]
```
