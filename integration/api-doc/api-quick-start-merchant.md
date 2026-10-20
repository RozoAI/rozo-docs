---
description: Accept a payment with your own merchant app, then verify settlement.
---

# Merchant API Quick Start

Create a customer payment that settles into your merchant's configured wallet. This example uses your own app and API key, not a shared demo merchant.

## Before you start

Complete [Make Your First API Request](first-request.md) and save its `payment.mjs` client. You need Node.js 18+, a verified **Merchant app**, a configured settlement wallet and an Orders key in `ROZO_API_KEY`.

Do not include `destination` in merchant requests. Configure the settlement wallet at [partners.rozo.ai](https://partners.rozo.ai). If the recipient changes for each request, use a [Wallet app](api-quick-start.md) instead.

## 1. Preview a payment

Save this as `payment-request.json` beside `payment.mjs`:

```json
{
  "type": "exactIn",
  "display": { "title": "Example purchase", "currency": "USD" },
  "source": { "chainId": "8453", "tokenSymbol": "USDC", "amount": "10.00" }
}
```

Here the customer pays the specified amount of Base USDC. `exactIn` fixes the input; settlement can differ after fees. Use the amount appropriate to your purchase and check the quote rather than assuming a fixed net amount.

```bash
node payment.mjs quote
```

This uses `POST /payments?dryrun=true`. Check the source amount, expected destination amount and fee information. It does not create a payable order.

## 2. Create the customer order

Set `ROZO_ORDER_ID` in your server environment to your unique purchase reference. If creation has an uncertain outcome, preserve this reference and run `node payment.mjs lookup`; do not repeat create. Then run:

```bash
node payment.mjs create
```

The client calls `POST /payments` and privately saves the response to `.rozo-payment.json`. No wallet payment is sent. The API key identifies your merchant app and its receiving configuration.

Use the returned `paymentLink` as the customer's hosted checkout, or display the returned `source` payment instructions in your own interface. Always use the actual response, including the source network, token, amount and expiry.

## 3. Confirm settlement

After the customer pays, run:

```bash
node payment.mjs status
```

The client calls `GET /payments/{id}` for the saved order. Reconcile the raw status, destination amount and destination transaction against your purchase. A routed payment completes as `payment_payout_completed`; a direct payment can complete as `payment_completed`. The separate `merchantStatus` field can become `payment_completed` before payout is complete, so it is not proof of settlement.

See the [status reference](merchant-api-keys.md#reading-order-status) for intermediate states and recovery. Do not fulfill solely because an order was created or incoming funds were detected. If the result is uncertain, resume the same order instead of asking the customer to pay again.

## Build the checkout

- [Webhooks](api-for-advanced-used/webhook.md): receive and verify payment notifications instead of relying only on polling.
- [Orders and Admin key scopes](merchant-api-keys.md): choose the least access your backend needs.
- [Intent Pay SDK](../rozointentpay/quick-start.md): add a React payment interface.
- [API reference](api-doc-postman.md): request fields and additional operations.

## Merchant info and supported tokens

Create, dry-run and read responses include the merchant and its supported payment methods. Render the coin picker from `supportedTokens`, respecting app-specific and Beta restrictions, rather than assuming every listed product supports every asset. See [Supported Tokens and Chains](supported-tokens-and-chains.md).
