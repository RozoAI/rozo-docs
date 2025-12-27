# API Advanced

This page covers advanced payment features including Stellar Contract Payments and Wallet Top-up (Any Amount) payments.

**API Host**: `https://intentapiv4.rozo.ai/functions/v1`

**Supported Routes**: Currently only **Base ↔ Stellar** is supported for these advanced features.

---

## Wallet Top-up (Any Amount)

The `anyAmount` payment type allows users to send any amount without specifying it upfront. The system automatically detects the received amount and calculates the output dynamically.

This is ideal for:
- Wallet top-up flows
- Donation payments
- Flexible payment amounts

### Supported Amount Range

| Limit | Value |
|-------|-------|
| Minimum | $0.02 USDC |
| Maximum | $3,000 USDC |

Amounts outside this range will be rejected with `amountTooLow` or `amountTooHigh` error codes. For custom limits, please contact us.

### Create Any Amount Payment

#### Request

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "yourAppId",
    "type": "anyAmount",
    "display": {
        "title": "Wallet Top-up",
        "currency": "USD"
    },
    "source": {
        "chainId": "8453",
        "tokenSymbol": "USDC"
    },
    "destination": {
        "chainId": "1500",
        "receiverAddress": "GDFLZTLVMLR3OVO4VSODYB7SGVIOI2AS652WODBCGBUQAMXXXXXXXXXX",
        "tokenSymbol": "USDC"
    }
}'
```

> **Note**: For `anyAmount` type, do NOT include `source.amount` or `destination.amount`. The amounts are determined after payment is received.

#### Response

```json
{
  "id": "abc123-def456-789",
  "appId": "yourAppId",
  "status": "payment_unpaid",
  "type": "anyAmount",
  "source": {
    "chainId": "8453",
    "tokenSymbol": "USDC",
    "amount": "0",
    "receiverAddress": "0x5B63758b0954fFc9D803dEC550eCB485C9c15861",
    "receiverMemo": null
  },
  "destination": {
    "chainId": "1500",
    "receiverAddress": "GDFLZTLVMLR3OVO4VSODYB7SGVIOI2AS652WODBCGBUQAMXXXXXXXXXX",
    "tokenSymbol": "USDC",
    "amount": "0"
  }
}
```

### After Payment Received

Once the user sends USDC to the `source.receiverAddress`, the system:

1. Detects the payment amount on-chain
2. Validates the amount is within the allowed range ($0.02 - $3,000)
3. Calculates the fee based on your app tier
4. Updates the payment with actual amounts
5. Triggers the payout to the destination

The payment record is updated:

```json
{
  "id": "abc123-def456-789",
  "status": "payment_payin_completed",
  "type": "anyAmount",
  "source": {
    "amount": "100.00",
    "amountReceived": "100.00",
    "fee": "0.10"
  },
  "destination": {
    "amount": "99.90"
  }
}
```

### Stellar → Base Example

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "yourAppId",
    "type": "anyAmount",
    "display": {
        "title": "Wallet Top-up",
        "currency": "USD"
    },
    "source": {
        "chainId": "1500",
        "tokenSymbol": "USDC"
    },
    "destination": {
        "chainId": "8453",
        "receiverAddress": "0x1234567890abcdef1234567890abcdef12345678",
        "tokenSymbol": "USDC"
    }
}'
```

### Error Codes

| Error Code | Description |
|------------|-------------|
| `amountTooLow` | Received amount is below $0.02 USDC |
| `amountTooHigh` | Received amount exceeds $3,000 USDC |
| `insufficientLiquidity` | Destination chain lacks liquidity for the payout |

---

## Stellar Contract Payments

Stellar Contract Payments enable payments to Soroban smart contract addresses (C-addresses). This is useful for applications that need to receive payments directly into smart contracts.

### Overview

When using `stellar_payin_contracts` intent:

1. A unique Soroban contract address (C-address) is generated
2. User sends USDC directly to this contract address (no memo required)
3. System monitors the contract balance via Soroban RPC
4. Payout is triggered once payment is detected

### Create Payment with Contract Intent

#### Request

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "yourAppId",
    "orderId": "order_12345",
    "type": "exactIn",
    "intent": "stellar_payin_contracts",
    "display": {
        "title": "Order #12345",
        "currency": "USD"
    },
    "source": {
        "chainId": "1500",
        "tokenSymbol": "USDC",
        "amount": "10.00"
    },
    "destination": {
        "chainId": "8453",
        "receiverAddress": "0x1234567890abcdef1234567890abcdef12345678",
        "tokenSymbol": "USDC"
    }
}'
```

#### Response

```json
{
  "id": "abc123-def456-789",
  "appId": "yourAppId",
  "orderId": "order_12345",
  "status": "payment_unpaid",
  "type": "exactIn",
  "intent": "stellar_payin_contracts",
  "source": {
    "chainId": "1500",
    "tokenSymbol": "USDC",
    "amount": "10.00",
    "receiverAddress": "CCWOKELYHFN4TRD6XK4PLRVFPXEMQ4WYPA4K5XFUAXSBYKDGKWXD3H7K",
    "receiverMemo": null
  },
  "destination": {
    "chainId": "8453",
    "receiverAddress": "0x1234567890abcdef1234567890abcdef12345678",
    "tokenSymbol": "USDC",
    "amount": "9.99"
  }
}
```

> **Note**: The `source.receiverAddress` is a Soroban contract address (starts with `C`, 56 characters). No memo is needed.

### Combining with Any Amount

You can combine Stellar Contract Payments with Any Amount for flexible top-up flows:

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "yourAppId",
    "type": "anyAmount",
    "intent": "stellar_payin_contracts",
    "display": {
        "title": "Flexible Top-up",
        "currency": "USD"
    },
    "source": {
        "chainId": "1500",
        "tokenSymbol": "USDC"
    },
    "destination": {
        "chainId": "8453",
        "receiverAddress": "0x1234567890abcdef1234567890abcdef12345678",
        "tokenSymbol": "USDC"
    }
}'
```

### Register Transaction Hash (Optional)

For faster payment tracking, pre-register the transaction hash after the user submits payment:

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/{paymentId}/payin' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "txHash": "abc123def456...",
    "fromAddress": "GABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGH"
}'
```

---

## Payment Flow Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Create    │     │    User     │     │   Monitor   │     │   Payout    │
│   Payment   │────▶│   Sends     │────▶│   Detects   │────▶│  Triggered  │
│             │     │   USDC      │     │   Amount    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
  Deposit address      For anyAmount:      Validates         Funds sent
  is generated         any amount          amount range       to user's
  and returned         [$0.02-$3000]       and liquidity      destination
```

---

## Best Practices

1. **Use Pusher for real-time updates**: Subscribe to payment status changes instead of polling.

2. **Handle bounced payments**: If amount is outside range or liquidity is insufficient, payment will be marked as `payment_bounced` with appropriate error code.

3. **Pre-register for contracts**: When using Stellar contract payments, call `/payin` endpoint with txHash for faster detection.

4. **Check payment status**: Poll `GET /payments/{id}` or use Pusher to monitor status transitions.
