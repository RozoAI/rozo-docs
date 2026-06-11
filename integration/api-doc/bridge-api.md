---
description: >-
  Bridge & Wallet API. Move funds cross-chain by specifying the destination
  address yourself — bridging, wallet top-up, and smart account payments.
icon: bridge
---

# Bridge & Wallet API

Use this API when **you provide the destination address on every request** — bridging your own funds, topping up a wallet, or paying an arbitrary on-chain address.

Every payment request includes a `destination.receiverAddress`, and ROZO routes the funds cross-chain to it.

## Pages

* [API Quick Start](api-quick-start.md) — bridge 1 USDC from Base to Stellar in one call.
* [Wallet Top-up](api-for-advanced-used/wallet-topup.md) — `anyAmount` deposits: send any amount, the system detects it automatically.
* [Get Fees](api-for-advanced-used/get-fees.md) — preview fees with `dryrun=true` before creating a payment.
* [Stellar Smart Account Payments](api-for-advanced-used/stellar-contract-payments.md) — pay from Soroban contract addresses (C-addresses) to EVM and Solana.

## Webhooks

Bridge and wallet apps get the same [Webhook](api-for-advanced-used/webhook.md) notifications (`payment_payin_completed`, `payment_payout_completed`) as merchants — register your app on [partners.rozo.ai](https://partners.rozo.ai) (you'll get a `wallet_<slug>` appId) and configure your webhook URL there. Without a registered appId, poll the payment status instead.

## Looking to accept payments instead?

If you are a merchant with a **preconfigured receiving wallet** (no destination address needed per request), use the [Merchant API](merchant-api.md).
