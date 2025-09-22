# Rozo Payment API

Backend-focused API documentation for creating, managing, and tracking payments through the Intent Pay system.

**Base URL:** `https://intentapi.rozo.ai`

## Documentation Structure

- [API Endpoints](./endpoints.md) - REST API reference with cURL and fetch examples
- [Payment Bridging](./payment-bridging.md) - Cross-chain payment logic and receiving addresses
- [Data Types](./types.md) - Interface definitions and data structures

## Quick Start

### cURL Example

```bash
curl -X POST https://intentapi.rozo.ai/payment-api \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "appId": "your-app-id",
    "display": {
      "intent": "Purchase item",
      "paymentValue": "1",
      "currency": "USD"
    },
    "destination": {
      "chainId": "8453",
      "amountUnits": "1",
      "tokenSymbol": "USDC"
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
      intent: "Purchase item",
      paymentValue: "1",
      currency: "USD",
    },
    destination: {
      chainId: "8453",
      amountUnits: "1",
      tokenSymbol: "USDC",
    },
  }),
});

const payment = await response.json();
```

## Authentication

Include API credentials in request headers as configured in your application:

```bash
Authorization: Bearer YOUR_API_KEY
```

## Support

For questions about the Rozo Payment API, contact the development team or refer to the main documentation.
