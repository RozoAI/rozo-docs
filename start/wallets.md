---
description: Choose a wallet funding or transfer flow, with explicit Stellar account compatibility.
---

# Fund and Connect Wallets

Choose the direction and account type before choosing an API. A classic Stellar account starts with `G`; a Soroban contract account starts with `C`. A passkey describes how a wallet authorizes actions, and does not by itself establish compatibility with every flow below.

## Choose your wallet flow

| Task | Start here | Access and scope |
| --- | --- | --- |
| Transfer across chains to an address chosen for this request | [Bridge & Wallet API](../integration/api-doc/bridge-api.md) | Wallet app and Orders API key; check route and destination requirements |
| Prepare a Stellar account and receive USDC, with optional XLM | [Open a Stellar Wallet](../integration/api-doc/funding/stellar-wallet-onboarding.md) | Public keyless Funding flow, subject to live capabilities and signer support; do not assume C-address or passkey support |
| Buy native gas | [Buy Gas Tokens](../integration/api-doc/funding/buy-gas-tokens.md) | Check Funding capabilities for available outputs and limits |
| Give an app a deposit address for a Stellar recipient | [Wallet Deposit API](../integration/api-doc/deposit-api.md) | Requires an app ID; check supported source assets and G/C recipient rules |
| Pay out from a Stellar contract wallet to another supported chain | [Stellar Smart Account Payments](../integration/api-doc/api-for-advanced-used/stellar-contract-payments.md) | Registered app and a compatible contract-wallet payment flow |
| Receive classic Stellar deposits into a smart account, or withdraw to an exchange with a memo | [Exchange Deposits and Withdrawals (Beta)](../integration/api-doc/api-for-advanced-used/stellar-exchange-deposits-withdrawals.md) | Enabled per app; USDC and text-memo restrictions apply |

For gas plus a stablecoin, see [Gas + Stablecoin Funding](../integration/api-doc/funding/gas-plus-stablecoin.md). This is an on-request app capability, not part of the default public flow. [CCTP Bridge](../products/cctp-bridge/README.md) describes the separate native-USDC route.

## Start a cross-chain integration

1. Read [Bridge & Wallet API](../integration/api-doc/bridge-api.md), including app registration and webhook access. Consult [Supported Tokens and Chains](../integration/api-doc/supported-tokens-and-chains.md) and the selected flow's narrower restrictions.
2. Use the [testnet guide](../testnet/README.md) for its documented Base Sepolia to Stellar test route. Testnet coverage does not imply that Funding, MPP or every mainnet route is available there.
3. Follow the [Bridge API quick start](../integration/api-doc/api-quick-start.md) and [fee preview](../integration/api-doc/api-for-advanced-used/get-fees.md). Resolve app access before creating a live payment.
4. Have the user approve and pay according to the returned order instructions. Track settlement using that flow's status reference or [webhooks](../integration/api-doc/api-for-advanced-used/webhook.md).

## Start a Stellar onboarding integration

Follow [Open a Stellar Wallet](../integration/api-doc/funding/stellar-wallet-onboarding.md) for API, web and MCP entry points. Read capabilities, request a quote, create the order, obtain any required user signature, and follow the order to completion. The [Funding reference](../integration/api-doc/funding/README.md) defines completion, recovery and idempotency; Funding webhooks are not emitted yet, so poll.

## Compatibility and completion

A transfer to a classic account, onboarding a new account, and delivering to a smart account are different capabilities. Confirm the exact account and signer requirements instead of assuming that any Stellar wallet is supported.

For exchange withdrawals, copy the address and required memo from the exchange's deposit instructions. The Beta only supports the memo type documented on its page. On-chain delivery to an exchange is not proof that the exchange has credited the user's exchange balance.

Do not retry a payment by sending funds again when the result is unclear. Use the selected flow's recovery instructions and [contact support](../contact/contact-us/README.md).
