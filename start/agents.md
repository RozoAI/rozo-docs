---
description: Select the Rozo tool for paid API calls, invoices or Stellar wallet funding.
---

# Let an Agent Pay

Start with the task. Rozo has separate workflows for paid API requests, existing invoices and wallet funding. They do not share one universal payment command.

| Task | Recommended entry point | What you need |
| --- | --- | --- |
| Call a paid HTTP API | [MPP Router](../products/intent-based-payment-transfer/agentic-payments-mpprouter.md) | Stellar USDC and an authorized compatible wallet signer |
| Pay an OpenRouter top-up or another Coinbase-hosted invoice | [ROZO Checkout](../products/checkout/README.md) | A supported invoice link and a supported funding method |
| Prepare and fund a Stellar wallet | [Stellar onboarding](../integration/api-doc/funding/stellar-wallet-onboarding.md) | A supported source payment and a supported receiving account/signer |

## Pay for an API request

1. Follow the [MPP Router getting-started instructions](../products/intent-based-payment-transfer/agentic-payments-mpprouter.md#getting-started) to obtain the wallet tools or integrate the documented SDK.
2. Discover services using the live catalog linked in the [MPP guide](../products/intent-based-payment-transfer/agentic-payments-mpprouter.md). Read availability and verification information before selecting an endpoint.
3. Follow its challenge, authorization and retry flow. Check the requested amount against the user's authorized spending scope before signing.
4. Check the API result and payment receipt. A submitted signature alone does not mean the requested API call succeeded.

MPP Router is mainnet-only. If the wallet needs funds first, choose a compatible route in the [Wallet guide](wallets.md).

## Pay an existing invoice

Use the [Checkout CLI, MCP or skill instructions](../products/checkout/README.md). Start with a quote, show the amount and payment method, then create an order within the user's authorization. The user's wallet supplies the payment; the Checkout MCP does not hold their private key or sign for them.

Track both the deposit and the invoice result using Checkout's status instructions. Coinbase payment links and payment sessions are supported URL families. Availability differs between web, CLI and MCP; in particular, do not treat web-only Beta methods as MCP capabilities. See [Bulk Purchases and Agents](../products/checkout/bulk-and-agents.md) for bulk workflows and [x402 Payer](../products/checkout/x402-payer.md) for that separate payment protocol.

## Prepare a Stellar wallet

Use the MCP or API flow in [Open a Stellar Wallet](../integration/api-doc/funding/stellar-wallet-onboarding.md). That page names the tools, signing requirements and recovery steps. The MCP does not supply a wallet signer. The [Funding reference](../integration/api-doc/funding/README.md) defines live capability discovery and the final order state.

## Give an agent the right instructions

Provide the task-specific reference above together with the user's intended destination, authorized amount and available signing method. Have the agent discover supported capabilities, explain the proposed payment, preserve the order reference privately and resume status checks after interruption. Do not create another payment merely because a tool timed out.

For an app integration beyond these workflows, use the [capability catalog](capabilities.md). For access questions, [contact Rozo](../contact/contact-us/README.md).
