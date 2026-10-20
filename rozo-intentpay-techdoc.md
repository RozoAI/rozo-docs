# Payment Integration Lifecycle

This guide explains what an application needs to do before, during and after a Rozo payment. Choose the API or tool for your task first; each product defines its own request fields, authentication and final result.

## Choose a payment flow

| Outcome | Start here |
| --- | --- |
| Accept customer payments into configured merchant settlement | [Merchant guide](start/merchants.md) |
| Transfer across chains or fund a wallet | [Wallet guide](start/wallets.md) |
| Pay an existing invoice or call a paid API | [Agent guide](start/agents.md) |

The [capability catalog](start/capabilities.md) lists documented interfaces and access restrictions. A supported chain in one product does not imply support in every product.

## 1. Prepare the request

Confirm the recipient, network, asset and amount with the user. If the destination requires a memo, verify that the chosen flow supports the required memo type. For an invoice, preserve the provider's payment reference and use the supported invoice URL format.

Obtain the app ID or scoped API key required by the selected integration. Store server-side credentials on your backend. Keep wallet signing with the user or their authorized signer; do not send wallet secrets to an API or MCP endpoint.

## 2. Preview the payment

Use the selected flow's fee preview or quote operation before creating a payment where available. Show the required input, expected outputs, fees and expiry to the user. The returned quote or order is authoritative for that request; do not build a fee or route calculation from examples in the documentation.

- Intent payments: [fee preview](integration/api-doc/api-for-advanced-used/get-fees.md).
- Wallet preparation: [Funding quotes and capabilities](integration/api-doc/funding/README.md).
- Existing invoices: [Checkout](products/checkout/README.md).
- Paid API calls: the [MPP payment challenge](products/intent-based-payment-transfer/agentic-payments-mpprouter.md).

## 3. Create and authorize

Create the order using the interface's documented request and idempotency rules. Save the order reference privately so the application can resume after a restart. An order creation response does not mean that any funds have arrived.

Show the returned payment instructions. Check the source network, asset, exact amount or amount policy, destination and payment deadline before asking the user to authorize a transfer. Use the returned order details, never a deposit address from an earlier example.

Some flows require a separate receiving-wallet signature. Follow the [Stellar onboarding signing checks](integration/api-doc/funding/stellar-wallet-onboarding.md) when that flow requests one. A payment authorization does not authorize unrelated wallet operations.

## 4. Track the requested outcome

| Integration | Completion reference |
| --- | --- |
| Merchant payment | [Raw payment status and settlement reconciliation](integration/api-doc/merchant-api-keys.md#reading-order-status) |
| Wallet Funding | [Funding order status](integration/api-doc/funding/README.md#order-status); every output must be confirmed |
| Coinbase-hosted invoice | [Checkout invoice settlement](products/checkout/bulk-and-agents.md); a completed funding leg alone is insufficient |
| Paid API call | [MPP request and payment receipt](products/intent-based-payment-transfer/agentic-payments-mpprouter.md) |
| Smart-account exchange deposit or withdrawal | [Beta receipt and order checks](integration/api-doc/api-for-advanced-used/stellar-exchange-deposits-withdrawals.md) |

Use the corresponding endpoint or webhook to track progress. Do not treat a convenience display field as proof that the receiving wallet has been paid. Compare the final amount, asset, recipient and transaction or receipt with the original request.

Provider delivery is a separate outcome when relevant. For example, payment of an invoice does not by itself prove that a third party has updated an account balance, and on-chain delivery to an exchange does not prove exchange-account credit.

## 5. Handle interruptions and failures

After a timeout, read the existing order before creating or paying another one. Where the API supports idempotency, retry with the same key and request as documented. Never infer that a payment failed solely because the client lost its connection.

Expired orders, unsupported assets, wrong amounts and partial delivery have product-specific handling. Follow the relevant recovery instructions; do not assume automatic refunds or send another payment to fix an unclear result.

For intent payment notifications, follow [Webhook](integration/api-doc/api-for-advanced-used/webhook.md), verify signatures and process events idempotently. Funding currently requires order polling. Keep sensitive order references and credentials out of public logs.

## Test and review

Start with the [Base Sepolia to Stellar testnet guide](testnet/README.md) when it covers your intended route. Check success, expiry, duplicate requests and interrupted status polling before accepting customer payments. Features outside that test route have their own environment and access requirements.

For public contract source and published reviews, see [Contracts & Audits](contact/contracts-and-audits.md). For integration questions or an unresolved payment, [contact Rozo](contact/contact-us/README.md) with the relevant order reference and transaction evidence.
