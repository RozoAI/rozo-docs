---
description: >-
  Merchant API. Accept crypto payments into your preconfigured merchant wallet —
  create payments, poll status, manage API keys, and receive webhooks.
icon: credit-card
---

# Merchant API

Use this API when you are a **merchant accepting payments**. Your receiving wallet address is configured once on your merchant `appId` (via [partners.rozo.ai](https://partners.rozo.ai)) — so payment requests **never include a destination address**. Customers pay from any supported chain, and you receive the token and chain you chose.

## Pages

* [API Quick Start (Merchant)](api-quick-start-merchant.md) — create a payment and poll its status in two calls.
* [Merchant API Keys](merchant-api-keys.md) — Admin vs Orders scope, and using keys from an AI agent.
* [API Doc (POSTMAN)](api-doc-postman.md) — full OpenAPI spec and Postman collection.
* [Webhook](api-for-advanced-used/webhook.md) — get notified on `payment_payin_completed` and `payment_payout_completed`.

## Bridging your own funds instead?

If you want to send funds to an **arbitrary destination address you specify per request**, use the [Bridge & Wallet API](bridge-api.md).
