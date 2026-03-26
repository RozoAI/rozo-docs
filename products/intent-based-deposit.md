---
description: >-
  ROZO Intent Based Deposit. Generate a unique Stellar deposit address for your
  app to receive USDC with one API call.
icon: arrow-down-to-bracket
---

# Intent Based Deposit

Accept USDC deposits into your application by generating a unique Stellar deposit address per session or user.

## Why this product

* **One API call** to create a deposit address — no wallet infrastructure needed.
* **Stellar-native** settlement for fast, low-cost transactions.
* **Simple integration** — just pass your Stellar address and app ID.

## How it works

1. Call the Deposit API with your Stellar address and app ID.
2. Share the returned deposit address with your user.
3. Once the user sends USDC to that address, funds are forwarded to your Stellar account.

## Web UI

{% embed url="https://rozo.ai/deposit" %}

## Related docs

* [Deposit API Reference](../integration/api-doc/deposit-api.md)
* [ROZO Intent Pay API](../integration/api-doc/)
* [Intent Based Bridge](intent-based-bridge.md)
* [Intent Based Payment & Transfer](intent-based-payment-transfer.md)
