# Wallet Top-up (Any Amount)

The API is for wallet topup. If the wallet is on Base or Stellar, users can top up with USDC on other chains. For example, deposit from Ethereum, Solana, Base to your Stellar wallets.



The `anyAmount` payment type allows users to send any amount without specifying it upfront. The system automatically detects the received amount and calculates the output dynamically.

**API Host**: `https://intentapiv4.rozo.ai/functions/v1`

**Supported Routes**: Currently only **Base ↔ Stellar** is supported.

## Use Cases

* Wallet top-up flows
* Donation payments
* Flexible payment amounts

## Supported Amount Range

| Limit   | Value       |
| ------- | ----------- |
| Minimum | $0.02 USDC  |
| Maximum | $3,000 USDC |

Amounts outside this range will be rejected with `amountTooLow` or `amountTooHigh` error codes. For custom limits, please contact us.

## Create Any Amount Payment

### Base → Stellar Example

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

### Response

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

## After Payment Received

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

## Payment Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Create    │     │    User     │     │   Monitor   │     │   Payout    │
│   Payment   │────▶│   Sends     │────▶│   Detects   │────▶│  Triggered  │
│             │     │   USDC      │     │   Amount    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
  Deposit address      Any amount          Validates         Funds sent
  is generated         [$0.02-$3000]       amount range       to user's
  and returned         is accepted         and liquidity      destination
```

## Error Codes

| Error Code              | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `amountTooLow`          | Received amount is below $0.02 USDC              |
| `amountTooHigh`         | Received amount exceeds $3,000 USDC              |
| `insufficientLiquidity` | Destination chain lacks liquidity for the payout |

## Best Practices

1. **Use Pusher for real-time updates**: Subscribe to payment status changes instead of polling.
2. **Handle bounced payments**: If amount is outside range or liquidity is insufficient, payment will be marked as `payment_bounced` with appropriate error code.
3. **Check payment status**: Poll `GET /payments/{id}` or use Pusher to monitor status transitions.
