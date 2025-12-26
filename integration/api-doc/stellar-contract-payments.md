# Stellar Contract Payments

Stellar Contract Payments enable payments to Soroban smart contract addresses (C-addresses). This is useful for applications that need to receive payments directly into smart contracts for automated processing.

## Overview

When using `stellar_payin_contracts` intent, the system:

1. Generates a unique Soroban contract address (C-address) as the payment destination
2. Monitors the contract for incoming USDC payments using Soroban RPC
3. Automatically triggers the payout once payment is detected

## Payment Intent Types

| Intent | Description |
| --- | --- |
| `stellar_payin_contracts` | User pays to a Soroban contract address. Contract balance is monitored for payin confirmation. |

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

Note: The `source.receiverAddress` is a Soroban contract address (starts with `C`, 56 characters).

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
| --- | --- |
| USDC | `CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75` |

## Technical Details

### Contract Address Generation

Contract addresses are deterministically generated using:

- **Factory Contract**: `CCMGFBBY44JOY6LMM2HTADT5MZ77W75PMAT2QS7GQ4KVNC2RSEBTIAEJ`
- **Salt**: Full timestamp stored as `source_receiver_memo` in the payment record
- **Algorithm**: SHA256(salt) → XDR Preimage → SHA256 → StrKey.encodeContract()

### Balance Monitoring

- Payments are monitored using the Soroban Batch Balance Checker contract
- Balance checks occur every minute via cron job
- Once balance is detected, the payout is automatically initiated

### Batch Balance Checker Contract

```
CB7M7UEOJYS74KIGDBMWENTBBEYIIJUFBB3YYWAKMKWMPGN4HOJBHW24
```

## Error Handling

| Error Code | Description |
| --- | --- |
| `paymentNotFound` | Payment ID does not exist |
| `paymentNotUpdatable` | Payment is not in a status that allows updates |
| `invalidRequest` | Missing or invalid request parameters |

## Best Practices

1. **Pre-register transactions**: Use the `/payin` endpoint to register `txHash` and `fromAddress` immediately after the user submits their payment. This ensures accurate tracking.

2. **Poll for status**: After creating a payment, poll `GET /payments/{id}` to check for status updates. Look for `payment_payin_completed` and `payment_payout_completed`.

3. **Handle expiration**: Payments expire after 1 hour. Ensure your UI communicates this to users.
