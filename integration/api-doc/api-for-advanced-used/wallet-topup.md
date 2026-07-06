# Wallet Top-up

## Wallet Top-up v1 (Any Amount) to Stellar

The `anyAmount` payment type allows users to send any amount without specifying it upfront. The system automatically detects the received amount and calculates the output dynamically.

**API Host**: `https://intentapiv4.rozo.ai/functions/v1`

**Supported Routes**: `Ethereum`, `Arbitrum`, `Base`, `BSC`, and `Polygon` source routes to `Stellar` are supported.

**Supported Source Tokens**: `USDC` and `USDT`

## Wallet Top-up v2 (Fixed address, Any amount)

For multi-chain deposit support (Ethereum, Arbitrum, Base, BSC, Polygon) with a fixed deposit address, see the [Wallet Deposit API](https://github.com/RozoAI/rozo-docs/blob/main/integration/api-doc/deposit-api.md).

## Use Cases

* Wallet top-up flows
* Donation payments
* Flexible payment amounts

## Supported Amount Range

| Limit   | Value        |
| ------- | ------------ |
| Minimum | $0.02 USDC   |
| Maximum | $10,000 USDC |

Amounts outside this range will be rejected with `amountTooLow` or `amountTooHigh` error codes. For custom limits, please contact us.

## Create Any Amount Payment

### Base USDC → Stellar Example

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

### Arbitrum USDT → Stellar Example

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
        "chainId": "42161",
        "tokenSymbol": "USDT"
    },
    "destination": {
        "chainId": "1500",
        "receiverAddress": "GDFLZTLVMLR3OVO4VSODYB7SGVIOI2AS652WODBCGBUQAMXXXXXXXXXX",
        "tokenSymbol": "USDC"
    }
}'
```

## Supported Source Chains

* `1` Ethereum
* `42161` Arbitrum
* `8453` Base
* `56` BSC
* `137` Polygon

## Supported Source Tokens

* `USDC`
* `USDT`

## Destination Chain

* `1500` or `stellar`

## Request Notes

* `source.chainId` must be one of the supported EVM source chains above.
* `source.tokenSymbol` can be `USDC` or `USDT`.
* `destination.chainId` must be `1500` or `stellar`.
* `destination.receiverAddress` must be a valid Stellar address.
* Current examples use Stellar `USDC` as the destination token.

For the broader token and chain matrix, see [Supported Tokens and Chains](../supported-tokens-and-chains.md).

## After Payment Received

Once the user sends the selected source token to the `source.receiverAddress`, the system:

1. Detects the payment amount on-chain
2. Validates the amount is within the allowed range ($0.02 - $10,000)
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
│             │     │ USDC/USDT   │     │   Amount    │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
  Deposit address      Any amount          Validates         Funds sent
  is generated         [$0.02-$10000]       amount range       to user's
  and returned         is accepted         and liquidity      destination
```

## Error Codes

| Error Code              | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `amountTooLow`          | Received amount is below $0.02 USDC              |
| `amountTooHigh`         | Received amount exceeds $10,000 USDC             |
| `insufficientLiquidity` | Destination chain lacks liquidity for the payout |

## Best Practices

1. **Use Pusher for real-time updates**: Subscribe to payment status changes instead of polling.
2. **Handle bounced payments**: If amount is outside range or liquidity is insufficient, payment will be marked as `payment_bounced` with appropriate error code.
3. **Check payment status**: Poll `GET /payments/{id}` or use Pusher to monitor status transitions.
