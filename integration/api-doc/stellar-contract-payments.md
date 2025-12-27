# Stellar Contract Payments

Stellar Contract Payments enable payments to Soroban smart contract addresses (C-addresses). This is useful for applications that need to receive payments directly into smart contracts for automated processing.

**API Host**: `https://intentapiv4.rozo.ai/functions/v1`

**Supported Routes**: Currently only **Stellar → Base** is supported.

## Overview

When using `stellar_payin_contracts` intent:

1. A unique Soroban contract address (C-address) is generated
2. User sends USDC directly to this contract address (no memo required)
3. System monitors the contract balance via Soroban RPC
4. Payout is triggered once payment is detected

## Payment Intent Types

| Intent | Description |
|--------|-------------|
| `stellar_payin_contracts` | User pays to a Soroban contract address. No memo needed. |

## Create Payment with Contract Intent

### Request

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

### Response

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

## Combining with Any Amount

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

When using `anyAmount` with contract payments, any amount between $0.02 - $3,000 USDC is accepted.

## Register Transaction Hash (Optional)

For faster payment tracking and accurate sender information, you can pre-register the transaction hash and sender address after the user submits their payment:

### Request

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/{paymentId}/payin' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "txHash": "abc123def456...",
    "fromAddress": "GABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGH"
}'
```

### Response

```json
{
  "success": true,
  "message": "Transaction hash registered successfully",
  "payment": {
    "id": "abc123-def456-789",
    "status": "payment_unpaid",
    "source": {
      "txHash": "abc123def456...",
      "senderAddress": "GABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGH"
    }
  }
}
```

## Payment Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Create    │     │    User     │     │   Monitor   │     │   Payout    │
│   Payment   │────▶│   Pays to   │────▶│   Detects   │────▶│  Triggered  │
│             │     │  C-address  │     │   Balance   │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
  C-address is        Optional:           Contract           Funds sent
  generated and      POST /payin         balance is          to user's
  returned           with txHash        checked via         destination
                     & fromAddress      Soroban RPC           address
```

## Supported Tokens

Currently only **USDC** is supported for Stellar contract payments.

| Token | Contract Address |
|-------|------------------|
| USDC | `CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75` |

## Error Handling

| Error Code | Description |
|------------|-------------|
| `paymentNotFound` | Payment ID does not exist |
| `paymentNotUpdatable` | Payment is not in a status that allows updates |
| `invalidRequest` | Missing or invalid request parameters |

## Best Practices

1. **Pre-register transactions**: Use the `/payin` endpoint to register `txHash` and `fromAddress` immediately after the user submits their payment. This ensures accurate tracking.

2. **Poll for status**: After creating a payment, poll `GET /payments/{id}` to check for status updates. Look for `payment_payin_completed` and `payment_payout_completed`.

3. **Handle expiration**: Payments expire after 1 hour. Ensure your UI communicates this to users.
