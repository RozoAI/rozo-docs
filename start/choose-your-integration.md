---
description: Choose a Rozo integration by task, then follow one recommended guide.
icon: signs-post
---

# Choose Your Integration

Choose the outcome first. You do not need to learn every Rozo product to get started.

| I want to… | Recommended guide | Main distinction |
| --- | --- | --- |
| Accept payments into my merchant's configured settlement wallet | [Merchant guide](merchants.md) | The Merchant API uses a receiving wallet configured on your app |
| Move funds to a wallet address selected for each request | [Wallet guide](wallets.md) | Bridge requests specify the destination; other wallet flows have their own requirements |
| Let an agent pay for something or prepare a wallet | [Agent guide](agents.md) | Paying an API request, paying an invoice and funding a wallet are separate workflows |

## SDK, API, or an existing tool?

- **SDK:** use the [Intent Pay SDK](../integration/rozointentpay/quick-start.md) when you need a React payment interface. Check its supported configuration before choosing it for your flow.
- **API:** use the reference linked from your task guide when you own the interface or run a backend.
- **CLI, MCP or skill:** use the [Agent guide](agents.md) to select the tool for your task. Tool availability differs by product and payment method.
- **Web:** use the [existing product links on the home page](../README.md#which-site-should-i-use) if you want to complete a supported task without building an integration.

## Where do I register, and where is the API?

[partners.rozo.ai](https://partners.rozo.ai) manages apps and merchant API keys. It is separate from this documentation site. App registration does not automatically enable every wallet or Beta feature.

Each guide links to the exact API or tool reference, its access requirements and its completion checks. A public demo app, a merchant API key and a wallet app ID are not interchangeable credentials.

For the full list of documented capabilities and access conditions, see the [capability catalog](capabilities.md).
