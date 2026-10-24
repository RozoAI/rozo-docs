---
description: Quote a Base USDC to Stellar transfer, create an order, and verify settlement.
---

# Wallet API Quick Start

This example transfers USDC from Base to a classic Stellar account. Use a **Wallet app** when you choose the recipient for each transfer. For a merchant's configured receiving wallet, use the [Merchant quick start](api-quick-start-merchant.md).

## Before you start

Complete [Make Your First API Request](first-request.md) and save its `payment.mjs` client. You need Node.js 18+, a verified app and its Orders API key in `ROZO_API_KEY`.

Quoting does not move funds. To complete a mainnet transfer, the payer needs Base USDC and the gas required by their wallet. The receiving Stellar account must be ready to receive USDC. For an account that is not ready, use [Stellar onboarding](funding/stellar-wallet-onboarding.md). For C-address wallets, use the [smart-account guide](api-for-advanced-used/stellar-contract-payments.md).

## 1. Preview the transfer

Set `ROZO_RECEIVER_ADDRESS` in your local or server environment to the intended Stellar G-address obtained from the recipient. The client uses the same destination for the quote and the created order.

Save this as `payment-request.json` beside `payment.mjs`:

```json
{
  "type": "exactIn",
  "display": { "title": "Wallet transfer", "currency": "USD" },
  "source": { "chainId": "8453", "tokenSymbol": "USDC", "amount": "10.00" },
  "destination": { "chainId": "1500", "tokenSymbol": "USDC" }
}
```

`8453` is Base and `1500` is Stellar. The amount is an example, not a minimum or a fee promise. Change it to the amount the user intends to pay.

```bash
node payment.mjs quote
```

The client calls `POST /payments?dryrun=true`. Expect a dry-run response with source amount, destination amount and fee information. No payment order or usable deposit address is created. A quote does not lock a future price; review the created order before paying.

## 2. Create an order

Set these in your local or server environment:

| Variable | Value |
| --- | --- |
| `ROZO_ORDER_ID` | Your unique order reference; preserve it for lookup if creation is uncertain |
| `ROZO_RECEIVER_ADDRESS` | The intended Stellar G-address, obtained from the recipient |

After the user approves the amount and destination:

```bash
node payment.mjs create
```

The client calls `POST /payments` and saves the response to `.rozo-payment.json`. It does not send funds. The response supplies `id`, `status`, `source` payment instructions and the `destination`. Check the actual destination, amount, fees and expiry before presenting those instructions in your application.

## 3. Pay and check the result

Have the payer's wallet send the returned `source.amount`, on the returned source network and token, to the returned `source.receiverAddress`. Use the newly created order's instructions, not an address from an example or a previous order.

```bash
node payment.mjs status
```

This calls `GET /payments/{id}` for the saved order. For this routed transfer, wait for raw `status = payment_payout_completed`, then reconcile the destination amount and transaction. `payment_payin_completed` means incoming funds are confirmed, not that the recipient has received the payout.

Preserve the order reference if the result is unclear. Resume status checks instead of creating or paying another order. See [status and reconciliation](merchant-api-keys.md#reading-order-status) and [webhooks](api-for-advanced-used/webhook.md).

## Next steps

- [Fee previews and errors](api-for-advanced-used/get-fees.md): handle rejected quotes and read fees from the response.
- [Supported chains and tokens](supported-tokens-and-chains.md): discover available routes; individual apps can have narrower support.
- [Wallet top-up](api-for-advanced-used/wallet-topup.md): variable-amount deposits.
- The Base Sepolia to Stellar testnet route is currently unavailable.

## Routing provider (optional)

Routing is automatic by default. The optional `provider` field accepts `auto`, `rozo` or `near`. Check the live supported matrix and quote result before selecting a provider; unsupported combinations return an error. Deposit addresses for NEAR-routed orders are single-use and expire.
