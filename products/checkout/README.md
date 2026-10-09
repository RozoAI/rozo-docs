---
description: >-
  Pay an OpenRouter top-up or any Coinbase-hosted invoice with the coin you
  already hold. Web, CLI, MCP server and Claude Code skill.
icon: cart-shopping
---

# ROZO Checkout

ROZO Checkout pays a Coinbase-hosted invoice with the coin you already hold. It accepts OpenRouter credit top-ups and other invoices in either link format, `payments.coinbase.com/payment-links/pl_*` or `payments.coinbase.com/payment-sessions/paymentSession_*`. ROZO creates a one-time deposit order for the coin you pick. Once you pay it, ROZO's funder settles the invoice in USDC on Base, which is what the merchant expects.

There is no ROZO account, no API key and no private key involved. You pay the deposit order from your own wallet or straight from an exchange withdrawal.

## Supported coins and chains

| You hold | Chains |
| --- | --- |
| Bitcoin | Lightning |
| USDC or USDT | Solana, Ethereum, BNB Chain, Polygon, Arbitrum |
| USDC | Base, Stellar |
| Native coins | ETH on Ethereum, Base or Arbitrum. BNB on BNB Chain. SOL on Solana |

Not accepted: on-chain Bitcoin, native POL and Tron.

Native coins are available on the web checkout at [checkout.rozo.ai](https://checkout.rozo.ai). The CLI and the MCP server currently quote stablecoins and Lightning; run `supported_coins` (MCP) or check the CLI README for the current list.

Stellar deposits route through a shared address plus a memo. Whatever you send from must let you set the memo shown on the order, or the payment cannot be matched.

## Supported merchants

The merchant directory lives at [checkout.rozo.ai/services](https://checkout.rozo.ai/services), and the directory is the source of truth. A merchant being listed means its Coinbase payment link format is compatible. Invoices that have already been paid through ROZO Checkout include OpenRouter, Venice AI, Porkbun and Alchemy.

## Four ways to use it

### Web

Open [checkout.rozo.ai](https://checkout.rozo.ai), paste the payment link, pick the coin you hold and pay the deposit order shown on the page.

### CLI

```bash
# Review the quote first. Creates nothing.
npx @rozoai/checkout quote <coinbase-link>

# Pay it with a chosen coin, unattended.
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana --yes
```

The default path needs no private key, no environment variable and no configuration. It prints a deposit block (chain, token, exact amount, address and any memo) for you to pay from any wallet, then waits until the invoice settles. Agents and scripts should always pass `--with`; the coin picker only appears on an interactive terminal. Source and full flag list: [RozoAI/rozo-checkout-skill](https://github.com/RozoAI/rozo-checkout-skill).

### MCP server

Remote MCP server (streamable HTTP):

```
https://mcp.rozo.ai/mcp?src=docs
```

The URL only answers MCP `POST` requests, so opening it in a browser shows an error. Add it to an MCP client instead.

It exposes four tools:

| Tool | What it does |
| --- | --- |
| `supported_coins` | Lists the supported chains and tokens. |
| `quote_invoice` | Reads the merchant, invoice amount, what the payer pays and the link expiry. Creates nothing. |
| `create_deposit_order` | Creates a one-time deposit order and returns the deposit address (or a BOLT11 invoice for Lightning), the exact amount, any memo and the expiry. |
| `payment_status` | Reports pay-in, payout progress and whether the Coinbase invoice settled. |

The server never custodies funds. It holds no private keys, signs nothing and sends nothing; the user pays from their own wallet. An order that is never funded expires and costs nothing.

Claude Code:

```bash
claude mcp add --transport http rozo-checkout "https://mcp.rozo.ai/mcp?src=claude-code"
```

Claude Desktop or Claude.ai: Settings, Connectors, Add custom connector, URL `https://mcp.rozo.ai/mcp?src=claude`.

Claude Desktop with a local `claude_desktop_config.json` through the `mcp-remote` bridge:

```json
{
  "mcpServers": {
    "rozo-checkout": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.rozo.ai/mcp?src=claude-desktop"]
    }
  }
}
```

### Claude Code skill

Install the skill in two steps inside Claude Code:

```text
/plugin marketplace add RozoAI/rozo-checkout-skill
/plugin install rozo-checkout@rozo
```

Then ask Claude to pay a Coinbase payment link with the coin you hold. Repository: [RozoAI/rozo-checkout-skill](https://github.com/RozoAI/rozo-checkout-skill).

## Fees and timing

* **The fee is in the quote.** You pay the full invoice amount. The ROZO fee and the bridge cost are added to the deposit amount, which is shown in the order before the deposit address is released. Send exactly that amount; nothing else is charged. Lightning and native coin payments also include a conversion spread built into the coin amount.
* **A quote is short-lived.** The quote returned by `quote` or `quote_invoice` is valid for about 60 seconds. Creating the order takes a fresh quote, so you never pay a stale price.
* **The order has its own deadline.** The deposit order expires at the time returned when it is created, and it can never outlive the Coinbase payment link it pays. Pay before that time.
* **Crypto top-ups are final.** OpenRouter does not refund crypto payments; that is OpenRouter's policy. Check the credit amount before you send.
* **Minimum amount.** OpenRouter's crypto payment links start at $10. See [Why is the minimum $10?](https://checkout.rozo.ai/blog/openrouter-crypto-minimum-10-dollars).

## Paid but the credits have not arrived

Do not pay a second time. Follow [OpenRouter payment troubleshooting](https://checkout.rozo.ai/help/openrouter-payment-troubleshooting), and contact hi@rozo.ai or [Discord](https://discord.com/invite/EfWejgTbuU) with the chain, amount and transaction hash.

## Related

* [Agentic Payments (MPP Router)](../intent-based-payment-transfer/agentic-payments-mpprouter.md): an agent that holds Stellar USDC and pays per API call.
* [Supported Tokens and Chains](../../integration/api-doc/supported-tokens-and-chains.md)
