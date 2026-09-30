# API Quick Start (Merchant)

Accept a USDC payment into your merchant account in two calls: create a payment, then poll for its status.

App ID: your merchant `appId`. You can try the examples below with our test merchant `pos_rozostudio`, then join our discord to get your own.

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

Poll this endpoint until `status` becomes `payment_completed`. Common statuses:

| Status | Meaning |
| --- | --- |
| `payment_unpaid` | Waiting for the customer to send funds |
| `payment_started` | Funds detected on chain, confirming |
| `payment_completed` | Settled — fulfill the order |

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

