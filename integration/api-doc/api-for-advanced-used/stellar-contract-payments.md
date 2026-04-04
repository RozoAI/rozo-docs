# Stellar Contract Payments

Stellar Contract Payments enable payments from Stellar to EVM and Solana chains via Soroban smart contract addresses (C-addresses). Users pay by invoking a contract's `pay()` function with a unique memo, and the system triggers cross-chain payout once payment is detected.

**API Host**: `https://intentapiv4.rozo.ai/functions/v1`

## Supported Routes

| Source Chain | Source Token | Destination Chain | Destination Token |
|-------------|-------------|-------------------|-------------------|
| Stellar (1500) | USDC | Base (8453) | USDC |
| Stellar (1500) | USDC | BNB Chain (56) | USDT |
| Stellar (1500) | USDC | BNB Chain (56) | USDC |
| Stellar (1500) | USDC | Ethereum (1) | USDT |
| Stellar (1500) | USDC | Ethereum (1) | USDC |
| Stellar (1500) | USDC | Arbitrum (42161) | USDC |
| Stellar (1500) | USDC | Polygon (137) | USDC |
| Stellar (1500) | USDC | Solana (501) | USDC |

## Overview

When using `stellar_payin_contracts` intent:

1. A unique Soroban contract address (`receiverAddressContract`) and memo (`receiverMemoContract`) are generated
2. User invokes the contract's `pay()` function with the amount and memo
3. System monitors the contract for the payment
4. Cross-chain payout is triggered once payment is detected

## Payment Intent Types

| Intent | Description |
|--------|-------------|
| `stellar_payin_contracts` | User pays by invoking a Soroban contract's `pay()` function with a unique memo. |

## Create Payment with Contract Intent

### Request

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "yourAppId",
    "intent": "stellar_payin_contracts",
    "type": "exactOut",
    "display": {
        "title": "Order #12345",
        "currency": "USD"
    },
    "source": {
        "senderAddress": "CBHKUT4SOTRYXJBQIOKXSW47CU2PF56OWXCML4XBQZAZLRX6R7TTNE4R",
        "chainId": 1500,
        "tokenSymbol": "USDC"
    },
    "destination": {
        "receiverAddress": "0x5772FBe7a7817ef7F586215CA8b23b8dD22C8897",
        "chainId": 8453,
        "tokenSymbol": "USDC",
        "amount": "1"
    }
}'
```

### Response

```json
{
    "id": "ae718e1b-74d3-485b-bebc-c5208850b400",
    "appId": "yourAppId",
    "orderId": null,
    "status": "payment_unpaid",
    "errorCode": null,
    "type": "exactOut",
    "createdAt": "2026-04-04T14:56:21.279+00:00",
    "updatedAt": "2026-04-04T14:56:21.279+00:00",
    "expiresAt": "2026-04-04T15:56:21.279+00:00",
    "display": {
        "title": "Order #12345",
        "description": null,
        "currency": "USD"
    },
    "source": {
        "chainId": "1500",
        "tokenSymbol": "USDC",
        "tokenAddress": "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
        "amount": "1.01",
        "receiverAddress": "CC4ING2NYT2ZKA5RGSJYPQFLWW4BTSBVADFXNBFMYBJ7GNPZVF4A6FFB",
        "receiverMemo": null,
        "fee": "0.01",
        "senderAddress": null,
        "txHash": null,
        "amountReceived": null,
        "confirmedAt": null,
        "receiverAddressContract": "CAQPKW5AUPEA4C7OERZRUCBWT5RZDSETO4PR5REVRC5MT4CF3PBSKXQC",
        "receiverMemoContract": "memo_1775314581279"
    },
    "destination": {
        "chainId": "8453",
        "receiverAddress": "0x5772FBe7a7817ef7F586215CA8b23b8dD22C8897",
        "receiverMemo": null,
        "tokenSymbol": "USDC",
        "tokenAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "amount": "1.00",
        "txHash": null,
        "confirmedAt": null
    }
}
```

### Key Response Fields

| Field | Description |
|-------|-------------|
| `source.receiverAddressContract` | The Soroban contract address to invoke `pay()` on |
| `source.receiverMemoContract` | The unique memo to pass to the `pay()` function |
| `source.amount` | Total amount to pay (includes fee) |
| `source.fee` | Fee amount deducted from the source payment |
| `destination.amount` | Amount the receiver will get on the destination chain |

## How to Pay

After creating a payment, the user invokes the Soroban contract's `pay()` function:

```
pay(sender, amount, memo)
```

| Parameter | Value | Example |
|-----------|-------|---------|
| Contract | `source.receiverAddressContract` | `CAQPKW5AUPEA4C7OERZRUCBWT5RZDSETO4PR5REVRC5MT4CF3PBSKXQC` |
| `sender` | The user's Stellar address | `CBHK...NE4R` |
| `amount` | `source.amount` in stroops (multiply by 10^7) | `10100000` for 1.01 USDC |
| `memo` | `source.receiverMemoContract` | `memo_1775314581279` |

On-chain, the invocation looks like:

```
invoked contract CAQP…KXQC pay(CBHK…NE4R, 10100000i128, "memo_1775314581279"str)
```

The system detects this contract invocation and triggers the cross-chain payout to the destination address.

## Combining with Any Amount

You can combine Stellar Contract Payments with Any Amount for flexible top-up flows:

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
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
        "chainId": 1500,
        "tokenSymbol": "USDC"
    },
    "destination": {
        "chainId": 8453,
        "receiverAddress": "0x1234567890abcdef1234567890abcdef12345678",
        "tokenSymbol": "USDC"
    }
}'
```

When using `anyAmount` with contract payments, any amount between $0.02 - $10,000 USDC is accepted.

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
│   Create    │     │    User     │     │   System    │     │   Payout    │
│   Payment   │────▶│  Invokes    │────▶│   Detects   │────▶│  Triggered  │
│             │     │   pay()     │     │  Contract   │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
  Contract addr       User calls          Contract            Funds sent
  and memo are       pay(sender,         invocation          cross-chain
  returned           amount, memo)       is detected         to destination
```

## Supported Tokens

Currently only **USDC** is supported as the source token on Stellar for contract payments.

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
