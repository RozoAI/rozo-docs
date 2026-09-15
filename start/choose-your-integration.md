---
description: >-
  Choose your ROZO integration. One table to pick between the SDK, the Bridge &
  Wallet API, the Merchant API, MPP Router and CCTP Bridge.
icon: signs-post
---

# Choose Your Integration

Every ROZO product runs on the same intent rails. Pick the entry point that matches what you are building, then follow its quick start.

| You are building… | Use | Start here |
| --- | --- | --- |
| A web app that accepts payments from any chain, with a drop-in React component | **Intent Pay SDK** | [Quick Start Guide](../integration/rozointentpay/quick-start.md) |
| A wallet, bridge or app that moves funds to an address you control per request | **Bridge & Wallet API** | [API Quick Start](../integration/api-doc/api-quick-start.md) |
| A merchant checkout that settles into a preconfigured wallet, with webhooks | **Merchant API** | [API Quick Start (Merchant)](../integration/api-doc/api-quick-start-merchant.md) |
| An AI agent that pays per API call over HTTP 402, no API keys | **Agentic Payments (MPP Router)** | [MPP Router](../products/intent-based-payment-transfer/agentic-payments-mpprouter.md) |
| Native USDC moves between Stellar and Base, Ethereum or Solana, self-custody | **CCTP Bridge** | [CCTP Bridge](../products/cctp-bridge/README.md) |
| A unique deposit address per user so your app can receive USDC | **Wallet Deposit for Apps** | [Wallet Deposit for Apps](../products/intent-based-bridge/intent-based-deposit.md) |

## SDK or API?

* **SDK** when you ship a browser UI and want the payment flow rendered for you.
* **API** when you own the UI, run a backend, or integrate from a non-JavaScript stack.

Both talk to the same intent API, so you can start with the SDK and add API calls later without re-integrating.

## Before you start

* Check [Supported Tokens and Chains](../integration/api-doc/supported-tokens-and-chains.md) for chain IDs and routes.
* Try the flow end to end on [testnet](../testnet/README.md) before going live.
* Questions: [Contact us](../contact/contact-us/README.md) or the [FAQs](../contact/faqs.md).
