# API Endpoints

Base URL: `https://intentapi.rozo.ai`

## Create Payment

`POST /payment-api`

Creates a new payment request.

**Request Body:** `PaymentRequestData`
**Response:** `PaymentResponseData`

### cURL Example

```bash
curl -X POST https://intentapi.rozo.ai/payment-api \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "appId": "your-app-id",
    "display": {
      "intent": "Premium subscription",
      "paymentValue": "29.99",
      "currency": "USD"
    },
    "destination": {
      "chainId": "8453",
      "amountUnits": "29.99",
      "tokenSymbol": "USDC"
    },
    "externalId": "sub_12345",
    "metadata": {
      "userId": "user_67890"
    }
  }'
```

### JavaScript Fetch

```javascript
const response = await fetch("https://intentapi.rozo.ai/payment-api", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer YOUR_API_KEY",
  },
  body: JSON.stringify({
    appId: "your-app-id",
    display: {
      intent: "Premium subscription",
      paymentValue: "29.99",
      currency: "USD",
    },
    destination: {
      chainId: "8453",
      amountUnits: "29.99",
      tokenSymbol: "USDC",
    },
  }),
});

const payment = await response.json();

// Example response:
/*
{
  "id": "2a41baa0-c2b8-4360-af5a-eda0fef3e914",
  "status": "payment_unpaid",
  "createdAt": "2025-09-21T15:29:29.857+00:00",
  "display": {
    "intent": "Pay",
    "currency": "USDC"
  },
  "source": null,
  "destination": {
    "destinationAddress": "GAA3PV4SN4AEFGYXTHLO7X4ETQEM6PERUJN2NGRGMKEHNJSYYTIFMM5S",
    "txHash": null,
    "chainId": "1500",
    "amountUnits": "0.1",
    "tokenSymbol": "USDC",
    "tokenAddress": "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN"
  },
  "metadata": {
    "receivingAddress": "0x13735745e512befb599ab1bf44021290cab148c9",
    "payinchainid": "137",
    "payintokenaddress": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
    "webhookUrl": "https://example.com/webhook"
  },
  "url": "http://checkout.example.com/pay?id=2a41baa0-c2b8-4360-af5a-eda0fef3e914"
}
*/
```

## Get Payment by ID

`GET /payment-api/id/{paymentId}`

Retrieves payment by Rozo payment ID.

**Parameters:**

- `paymentId` (string): Payment ID

**Response:** `PaymentResponseData`

### cURL Example

```bash
curl -X GET https://intentapi.rozo.ai/payment-api/id/pay_abc123 \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### JavaScript Fetch

```javascript
const response = await fetch(
  "https://intentapi.rozo.ai/payment-api/id/pay_abc123",
  {
    headers: {
      Authorization: "Bearer YOUR_API_KEY",
    },
  }
);

const payment = await response.json();
```

## HTTP Status Codes

| Code | Description                       |
| ---- | --------------------------------- |
| 200  | Success                           |
| 400  | Bad Request - Invalid data        |
| 401  | Unauthorized - Invalid auth       |
| 404  | Not Found - Payment doesn't exist |
| 429  | Too Many Requests - Rate limited  |
| 500  | Internal Server Error             |

## Error Response Format

```typescript
{
  data: null,
  error: Error,
  status: 400
}
```
