#### 3.4.2 Actual Total Load (6.1.A) - POST Method

Alternative method using XML request body instead of query parameters.

| Property | Value |
|----------|-------|
| **Method** | POST |
| **Endpoint** | `https://web-api.tp.entsoe.eu/api` |
| **Content-Type** | `application/xml` |

**Request Limits:**
- One year range limit applies
- Minimum time interval in response is one MTU period

**Headers:**

| Header | Value |
|--------|-------|
| `Content-Type` | `application/xml` |
| `SECURITY_TOKEN` | Your API token |

**Request Body Structure:**
```xml
<StatusRequest_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-5:statusrequestdocument:4:0">
    <mRID>SampleCallToRestfulApi</mRID>
    <type>A59</type>
    <sender_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450</sender_MarketParticipant.mRID>
    <sender_MarketParticipant.marketRole.type>A07</sender_MarketParticipant.marketRole.type>
    <receiver_MarketParticipant.mRID codingScheme="A01">10X1001A1001A450</receiver_MarketParticipant.mRID>
    <receiver_MarketParticipant.marketRole.type>A32</receiver_MarketParticipant.marketRole.type>
    <createdDateTime>2016-01-10T13:00:00Z</createdDateTime>
    <AttributeInstanceComponent>
        <attribute>DocumentType</attribute>
        <attributeValue>A65</attributeValue>
    </AttributeInstanceComponent>
    <AttributeInstanceComponent>
        <attribute>ProcessType</attribute>
        <attributeValue>A16</attributeValue>
    </AttributeInstanceComponent>
    <AttributeInstanceComponent>
        <attribute>OutBiddingZone_Domain</attribute>
        <attributeValue>10YCZ-CEPS-----N</attributeValue>
    </AttributeInstanceComponent>
    <AttributeInstanceComponent>
        <attribute>TimeInterval</attribute>
        <attributeValue>2016-01-01T00:00Z/2016-01-02T00:00Z</attributeValue>
    </AttributeInstanceComponent>
</StatusRequest_MarketDocument>
```

**Note:** The POST method is an alternative for programmatic access when query string length is a concern.

---
