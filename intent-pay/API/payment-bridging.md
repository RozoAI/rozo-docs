# Payment Routing Logic

This document explains how payment routing works when users want to pay out to different chains and tokens, particularly USDC on Stellar or Base networks.

## Overview

The payment system supports cross-chain payments where users can:

- **Pay In** from one chain/token (Polygon USDC, Solana USDC, Stellar USDC, BSC USDT)
- **Pay Out** to a different chain/token (Base USDC, Stellar USDC, Solana USDC)

## Key Concept: receivingAddress

When creating a payment, the API returns a `receivingAddress` in the response metadata. This address becomes the **final destination** where funds should be sent, overriding the original destination address.

```javascript
// After creating payment
const response = await fetch("https://intentapi.rozo.ai/payment-api", {
  /* ... */
});
const payment = await response.json();

// Example response structure:
/*
{
  "id": "2a41baa0-c2b8-4360-af5a-eda0fef3e914",
  "status": "payment_unpaid",
  "destination": {
    "destinationAddress": "GAA3PV4SN4AEFGYXTHLO7X4ETQEM6PERUJN2NGRGMKEHNJSYYTIFMM5S",
    "chainId": "1500"
  },
  "metadata": {
    "receivingAddress": "0x13735745e512befb599ab1bf44021290cab148c9",
    "payinchainid": "137",
    "payintokenaddress": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"
  },
  "url": "http://checkout.example.com/pay?id=2a41baa0-c2b8-4360-af5a-eda0fef3e914"
}
*/

// IMPORTANT: Always use receivingAddress as the final destination
const finalDestination = payment.metadata.receivingAddress;
const checkoutUrl = payment.url;

// Check if memo is required (for Stellar and Solana payments)
const memoRequired = payment.metadata.memo !== null;
const memo = payment.metadata.memo;
```

## Supported Payment Routes

### Pay Out to Base USDC

```javascript
const paymentData = {
  appId: "your-app-id",
  display: {
    intent: "Cross-chain payment",
    paymentValue: "100.00",
    currency: "USD",
  },
  destination: {
    destinationAddress: "0x1234...", // Base address
    chainId: "8453", // Base chain ID
    amountUnits: "100000000", // $100 in USDC units (6 decimals)
    tokenSymbol: "USDC",
    tokenAddress: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // Base USDC
  },
  preferredChain: "base",
  preferredToken: "USDC",
};
```

### Pay Out to Stellar USDC

```javascript
const paymentData = {
  appId: "your-app-id",
  display: {
    intent: "Payment to Stellar",
    paymentValue: "100.00",
    currency: "USD",
  },
  destination: {
    destinationAddress: "GCKFBEIYTKP...", // Stellar address
    chainId: "stellar-mainnet", // Stellar chain ID
    amountUnits: "100000000",
    tokenSymbol: "USDC",
    tokenAddress:
      "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN", // Stellar USDC asset
  },
  preferredChain: "stellar",
  preferredToken: "USDC",
};
```

<!-- ### Pay Out to Solana USDC

```javascript
const paymentData = {
  appId: "your-app-id",
  display: {
    intent: "Payment to Solana",
    paymentValue: "100.00",
    currency: "USD",
  },
  destination: {
    destinationAddress: "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM", // Solana address
    chainId: "solana-mainnet", // Solana chain ID
    amountUnits: "100000000",
    tokenSymbol: "USDC",
    tokenAddress: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", // Solana USDC mint
  },
  preferredChain: "solana",
  preferredToken: "USDC",
};
``` -->

## Pay In Options

Users can pay from different chains while paying out to their preferred destination:

### Pay In from Polygon USDC

```javascript
const paymentData = {
  // ... destination stays the same
  preferredChain: "137", // Polygon chain ID
  preferredToken: "USDC",
  preferredTokenAddress: "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359", // Polygon USDC
};
```

### Pay In from Stellar USDC (Memo Required)

When users pay in from Stellar, a memo is **required** for the payment transaction.

```javascript
const paymentData = {
  // ... destination stays the same
  preferredChain: "1500", // Stellar chain ID
  preferredToken: "USDC",
  // No preferredTokenAddress needed for Stellar
};

// After creating the payment, check for memo requirement
const payment = await createPayment(paymentData);

if (payment.metadata.memo) {
  console.log("MEMO REQUIRED for Stellar payment:", payment.metadata.memo);
  // User MUST include this memo when sending Stellar USDC
}
```

### Pay In from Solana USDC (Memo Required)

When users pay in from Solana, a memo is **required** for the payment transaction.

```javascript
const paymentData = {
  // ... destination stays the same
  preferredChain: "900", // Solana chain ID
  preferredToken: "USDC",
  preferredTokenAddress: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", // Solana USDC
};

// After creating the payment, check for memo requirement
const payment = await createPayment(paymentData);

if (payment.metadata.memo) {
  console.log("MEMO REQUIRED for Solana payment:", payment.metadata.memo);
  // User MUST include this memo when sending Solana USDC
}
```

### Pay In from BSC USDT

```javascript
const paymentData = {
  // ... destination stays the same
  preferredChain: "56", // BSC chain ID
  preferredToken: "USDT",
  preferredTokenAddress: "0x55d398326f99059fF775485246999027B3197955", // BSC USDT
};
```

## Complete Example: Cross-Chain Payment

```javascript
async function createCrossChainPayment() {
  // User wants to pay out to Stellar USDC, but pay in from Polygon
  const paymentRequest = {
    appId: "my-app",
    display: {
      intent: "Cross-chain payment to Stellar",
      paymentValue: "250.00",
      currency: "USD",
    },
    // Pay OUT to Stellar
    destination: {
      destinationAddress:
        "GCKFBEIYTKP7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
      chainId: "stellar-mainnet",
      amountUnits: "250000000", // $250 USDC
      tokenSymbol: "USDC",
      tokenAddress:
        "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
    },
    // Pay IN from Polygon
    preferredChain: "137",
    preferredToken: "USDC",
    preferredTokenAddress: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    externalId: "payment_123",
    metadata: {
      userId: "user_456",
      description: "Cross-chain USDC transfer",
    },
  };

  try {
    const response = await fetch("https://intentapi.rozo.ai/payment-api", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer YOUR_API_KEY",
      },
      body: JSON.stringify(paymentRequest),
    });

    const payment = await response.json();

    // IMPORTANT: Always use receivingAddress from response
    const finalDestination = payment.metadata.receivingAddress;
    const checkoutUrl = payment.url;

    console.log(
      "Original destination:",
      paymentRequest.destination.destinationAddress
    );
    console.log("Final receiving address:", finalDestination);
    console.log("Payment ID:", payment.id);
    console.log("Checkout URL:", checkoutUrl);

    return {
      paymentId: payment.id,
      finalDestination,
      checkoutUrl,
      status: payment.status,
      payInChain: payment.metadata.payinchainid,
      payInToken: payment.metadata.payintokenaddress,
      memo: payment.metadata.memo, // Required for Stellar/Solana
      memoRequired: payment.metadata.memo !== null,
    };
  } catch (error) {
    console.error("Payment creation failed:", error);
    throw error;
  }
}
```

## Chain and Token Reference

### Supported Chains

| Chain   | Chain ID         | Description         |
| ------- | ---------------- | ------------------- |
| Base    | `8453`           | Base mainnet        |
| Polygon | `137`            | Polygon mainnet     |
| BSC     | `56`             | Binance Smart Chain |
| Stellar | `1500`           | Stellar network     |
| Solana  | `solana-mainnet` | Solana network      |

### Token Addresses

#### USDC Addresses

- **Base**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **Polygon**: `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`
- **Stellar**: `USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN`
- **Solana**: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

#### USDT Addresses

- **BSC**: `0x55d398326f99059fF775485246999027B3197955`

## Error Handling

```javascript
async function createPaymentWithErrorHandling(paymentData) {
  try {
    const payment = await createRozoPayment(paymentData);

    if (!payment.data?.id) {
      throw new Error(payment.error?.message || "Payment creation failed");
    }

    // Extract receiving address if provided
    const receivingAddress = payment.data.metadata?.receivingAddress;

    return {
      success: true,
      paymentId: payment.data.id,
      receivingAddress:
        receivingAddress || paymentData.destination.destinationAddress,
      originalDestination: paymentData.destination.destinationAddress,
    };
  } catch (error) {
    console.error("Payment creation error:", error);
    return {
      success: false,
      error: error.message,
    };
  }
}
```

## Best Practices

1. **Always check for receivingAddress** in the API response
2. **Check for memo requirements** - required for Stellar and Solana payments
3. **Store both original and final destinations** for tracking
4. **Use external IDs** to correlate payments with your system
5. **Include comprehensive metadata** for better tracking
6. **Handle cross-chain delays** - payments may take time to process
7. **Validate chain IDs and token addresses** before sending
8. **Monitor payment status** using the GET endpoint

## Payment Status Flow

1. **payment_unpaid** - Payment created, awaiting user payment
2. **payment_progress** - Cross-chain bridge in progress
3. **payment_completed** - Funds delivered to final destination
4. **payment_expired** - Payment expired
