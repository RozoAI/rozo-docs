---
description: Start a merchant payment integration and choose the right API or browser SDK.
---

# Accept Merchant Payments

Use this path to accept customer payments into a merchant's configured settlement wallet. If you choose a different receiving address for each transfer, start with the [Wallet guide](wallets.md).

## Recommended path: Merchant API

1. Read the [Merchant API overview](../integration/api-doc/merchant-api.md). The receiving wallet is configured on the merchant app, rather than supplied with each order.
2. Register or manage your app at [partners.rozo.ai](https://partners.rozo.ai). Follow [Merchant API Keys](../integration/api-doc/merchant-api-keys.md) for key creation, scopes and server-side use. Public demo examples do not replace your own merchant setup.
3. Follow the [merchant quick start](../integration/api-doc/api-quick-start-merchant.md). It links to a shared Node.js client and provides a request you can run with your own key, starting with a quote.
4. Present the returned payment instructions to the customer. Track the order through the status endpoint documented for the API you use, or integrate [webhooks](../integration/api-doc/api-for-advanced-used/webhook.md).
5. Fulfill only after the corresponding API reports successful settlement. Creating an order or detecting an incoming payment is not enough.

Use the [API and Postman reference](../integration/api-doc/api-doc-postman.md) for detailed requests. Keep status names and authentication from the same API reference; different interfaces may expose different fields.

## Need a payment interface in React?

Start with the [Intent Pay SDK quick start](../integration/rozointentpay/quick-start.md), then check its [API reference](../integration/rozointentpay/api-reference.md) and [examples](../integration/rozointentpay/examples.md). The SDK configures a browser payment flow; review its receiving-address and app configuration for your use case. Do not assume its configuration is identical to the Merchant API.

For an existing in-person merchant app, see [ROZO POS](../products/mobile-app/pos-merchant-app.md).

## Requirements and troubleshooting

- Confirm settlement configuration and supported payment assets before accepting customer funds. See [Supported Tokens and Chains](../integration/api-doc/supported-tokens-and-chains.md) and the selected integration's restrictions.
- Keep server-side API keys out of browser code and public examples. Use the scope appropriate to order creation and reads.
- Use [SDK troubleshooting](../integration/rozointentpay/troubleshooting.md) for UI issues or [Contact us](../contact/contact-us/README.md) for access and settlement questions.

Paying an existing Coinbase-hosted invoice is a separate task: use the [Agent guide](agents.md) or [ROZO Checkout](../products/checkout/README.md).
