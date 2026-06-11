---
description: >-
  ROZO Intent Pay API. One intent API, two integration paths — Bridge & Wallet
  (you specify the destination address) and Merchant (preconfigured wallet).
---

# ROZO Intent Pay API

One intent API, two integration paths. Pick the one that matches how you receive funds:

| | [Bridge & Wallet API](bridge-api.md) | [Merchant API](merchant-api.md) |
| --- | --- | --- |
| **Who it's for** | Wallets, bridges, apps moving funds | Merchants accepting payments |
| **Destination address** | You pass `destination.receiverAddress` on every request | Preconfigured on your merchant `appId` — never sent per request |
| **Auth** | App ID | `X-API-Key` from [partners.rozo.ai](https://partners.rozo.ai) |
| **Start here** | [API Quick Start](api-quick-start.md) | [API Quick Start (Merchant)](api-quick-start-merchant.md) |

Shared references:

* [ROZO Intents Tech Design](rozo-intents-tech-design.md) — how the intent flow works under the hood.
* [Supported Tokens and Chains](supported-tokens-and-chains.md) — chain IDs, tokens, and routes.
