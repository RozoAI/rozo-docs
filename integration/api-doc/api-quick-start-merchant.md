# API Quick Start (Merchant)

Accept a USDC payment into your merchant account in two calls: create a payment, then poll for its status.

The examples below use the public demo merchant `pos_rozostudio`. Its receiving configuration belongs to the demo merchant, not to your business. Do not use that app ID to collect your own customer payments. For your own merchant, follow [Merchant API Keys](merchant-api-keys.md) to register and use the authenticated request examples.

API Host: https://intentapiv4.rozo.ai/functions/v1

### 1. Create a payment

`POST /payment-api/payments`

Base chain ID: `8453`

```bash
# Curl
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "pos_rozostudio",
    "orderId": "order-'"$(date +%s)"'",
    "type": "exactIn",
    "display": {
        "title": "Your POS test",
        "currency": "USD"
    },
    "source": {
        "chainId": "8453",
        "tokenSymbol": "USDC",
        "amount": "0.10"
    }
}'
```

The response returns a payment `id` and a `receiverAddress` on the source chain — show the customer this address (or its QR) to pay.

```json
{
  "id": "<payment_id>",
  "appId": "pos_rozostudio",
  "orderId": "order-1700000000",
  "status": "payment_unpaid",
  "type": "exactIn",
  "display": {
    "title": "Your POS test",
    "currency": "USD"
  },
  "source": {
    "chainId": "8453",
    "tokenSymbol": "USDC",
    "tokenAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "amount": "0.10",
    "receiverAddress": "<deposit_address>",
    "fee": "0.00"
  }
}
```

### 2. Check payment status

`GET /payment-api/payments/{id}`

```bash
# Curl
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/<payment_id>'
```

Poll the raw `status`. For a routed payment, wait for `payment_payout_completed`; a direct payment can finish as `payment_completed`. Reconcile the destination amount and transaction against your order before treating it as settled.

| Raw `status` | Meaning |
| --- | --- |
| `payment_unpaid` | Waiting for payment |
| `payment_started` | Payment detected; processing |
| `payment_payin_completed` | Incoming funds confirmed; payout may still be pending |
| `payment_payout_started` | Payout in progress |
| `payment_payout_completed` | Routed payout completed |
| `payment_completed` | Completed direct-payment flow |

The separate `merchantStatus` field can say `payment_completed` before payout is complete. Do not use it as proof of merchant settlement. See [Reading order status](merchant-api-keys.md#reading-order-status) for the distinction and recovery handling.

> Tip: instead of polling, configure a [Webhook](api-for-advanced-used/webhook.md) to get notified when the payment completes.

### Merchant info and supported tokens

Create (including `?dryrun=true`) and get order responses carry the merchant shown to the buyer and what that merchant accepts:

```json
{
  "id": "...",
  "status": "payment_unpaid",
  "merchant": {
    "appId": "merchant_example",
    "name": "Example Store",
    "logoUrl": "https://.../logo.png",
    "description": "...",
    "supportedTokens": {
      "stablecoins": "all",
      "native": [
        { "asset": "ETH@8453", "symbol": "ETH", "chainId": "8453", "chainName": "Base" },
        { "asset": "SOL@900", "symbol": "SOL", "chainId": "900", "chainName": "Solana" }
      ]
    }
  },
  "supportedTokens": { "stablecoins": "all", "native": ["..."] }
}
```

* `supportedTokens.native` lists only the native coins this merchant has enabled (empty when none). Native coins are a beta feature for invited merchants only; stablecoins are always accepted for every merchant. The same object is returned at the top level for orders that have no `merchant` block. Render the checkout coin picker from this field instead of a hardcoded list. See [Supported Tokens and Chains](supported-tokens-and-chains.md#native-coins-beta-invite-only).

