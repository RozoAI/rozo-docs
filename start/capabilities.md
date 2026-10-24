---
description: A task-oriented directory of documented Rozo capabilities and their access requirements.
---

# Capability Catalog

This catalog links to the documentation for each capability. It is a discovery map, not a guarantee that every route, account type or tool supports every feature. The linked reference and its live discovery response, where available, define the current scope.

## Merchant payments

| Capability | Interface and reference | Access or boundary |
| --- | --- | --- |
| Accept payments into configured merchant settlement | [Merchant API](../integration/api-doc/merchant-api.md) | Merchant app and API key; use the appropriate key scope |
| Add a React payment interface | [Intent Pay SDK](../integration/rozointentpay/README.md) | Configure the SDK for the intended payment flow |
| Use the existing in-person merchant app | [ROZO POS](../products/mobile-app/pos-merchant-app.md) | Follow merchant setup instructions |

## Wallet funding and transfers

| Capability | Interface and reference | Access or boundary |
| --- | --- | --- |
| Cross-chain transfer to a per-request destination | [Bridge & Wallet API](../integration/api-doc/bridge-api.md) | App ID and supported route |
| Receive variable-amount wallet top-ups | [Wallet Top-up](../integration/api-doc/api-for-advanced-used/wallet-topup.md) | Follow the documented amount policy |
| Create a deposit address for a Stellar recipient | [Wallet Deposit API](../integration/api-doc/deposit-api.md) | App ID; supported source assets and recipient types |
| Prepare a Stellar account and deliver USDC with optional XLM | [Stellar onboarding](../integration/api-doc/funding/stellar-wallet-onboarding.md), API/web/MCP | Keyless public mode with limits; supported accounts and signers only |
| Buy native gas | [Buy Gas Tokens](../integration/api-doc/funding/buy-gas-tokens.md) | Availability from Funding capabilities |
| Deliver gas and a stablecoin together | [Gas + Stablecoin Funding](../integration/api-doc/funding/gas-plus-stablecoin.md) | On request, enabled app and server-side API key |
| Pay from a Stellar smart account to supported chains | [Stellar Smart Account Payments](../integration/api-doc/api-for-advanced-used/stellar-contract-payments.md) | App integration and compatible contract payment |
| Forward classic Stellar deposits into a C account | [Exchange Deposits and Withdrawals (Beta)](../integration/api-doc/api-for-advanced-used/stellar-exchange-deposits-withdrawals.md) | Beta, enabled per app, USDC only |
| Withdraw from a C account to an exchange G address with a memo | [Exchange Deposits and Withdrawals (Beta)](../integration/api-doc/api-for-advanced-used/stellar-exchange-deposits-withdrawals.md) | Beta, enabled per app, USDC and text memo only |
| Use native USDC bridging | [CCTP Bridge](../products/cctp-bridge/README.md) | Separate route and setup; see its supported networks |
| Access EURC onramp and bridge flows | [EURC Onramp and Bridge](../products/intent-based-bridge/eurc-onramp/README.md) | Follow that product's eligibility and route requirements |

## Agent payments

| Capability | Interface and reference | Access or boundary |
| --- | --- | --- |
| Pay per paid API request | [MPP Router](../products/intent-based-payment-transfer/agentic-payments-mpprouter.md), wallet plugin/SDK | Stellar USDC, compatible signer, mainnet only; check catalog verification |
| Settle an existing Coinbase-hosted invoice | [Checkout](../products/checkout/README.md), web/CLI/MCP/skill | Supported invoice and payment method; web-only methods are identified there |
| Batch supported purchases | [Bulk Purchases and Agents](../products/checkout/bulk-and-agents.md) | Follow the documented batch and payment limits |
| Pay an x402 endpoint | [x402 Payer](../products/checkout/x402-payer.md) | Separate protocol flow and supported settlement requirements |

## Integration operations

- [Supported Tokens and Chains](../integration/api-doc/supported-tokens-and-chains.md): shared chain and asset reference; individual products can have narrower support.
- [Fee preview](../integration/api-doc/api-for-advanced-used/get-fees.md): preview an intent payment; Funding uses its own quote flow.
- [Webhooks](../integration/api-doc/api-for-advanced-used/webhook.md): intent payment notifications. Funding currently requires polling.
- [Look up by transaction hash](../integration/api-doc/api-for-advanced-used/lookup-by-tx-hash.md): locate a payment using its transaction.
- [Testnet](../testnet/README.md): the documented Base Sepolia to Stellar test flow, not a test environment for every product.

For an ordered walkthrough, choose the [Merchant](merchants.md), [Wallet](wallets.md) or [Agent](agents.md) guide.
