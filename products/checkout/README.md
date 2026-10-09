---
description: >-
  Pay an OpenRouter top-up or any Coinbase-hosted invoice with the coin you
  already hold. Use it from the web, the CLI, an MCP server or a Claude Code
  skill.
icon: cart-shopping
---

# ROZO Checkout

ROZO Checkout pays a Coinbase-hosted invoice with the coin you already hold. It accepts OpenRouter credit top-ups and other `payments.coinbase.com/payment-links/pl_*` and `payments.coinbase.com/payment-sessions/paymentSession_*` links. ROZO creates a one-time deposit order for the coin you pick; once your payment arrives, ROZO's funder settles the invoice to the merchant in USDC on Base.

There is no account to create and no private key to share. You pay from your own wallet or straight from an exchange withdrawal.

## Supported coins and chains

| Type | What you can pay with |
| --- | --- |
| Bitcoin | BTC over Lightning |
| Stablecoins | USDC or USDT on Solana, Ethereum, BNB Chain, Polygon or Arbitrum; USDC on Base or Stellar |
| Native coins | ETH on Ethereum, Base or Arbitrum; BNB on BNB Chain; SOL on Solana |

On-chain Bitcoin, native POL and Tron are not accepted. Native coins are available on [checkout.rozo.ai](https://checkout.rozo.ai); the CLI, MCP server and skill take the stablecoins and Lightning.

## Supported merchants

The merchant directory lives at [checkout.rozo.ai/services](https://checkout.rozo.ai/services); the directory there is the source of truth. A merchant listed there uses a compatible Coinbase link format. Payments have been completed so far for **OpenRouter, Venice.ai, Porkbun and Alchemy**. Any other `payments.coinbase.com` link is quoted the same way.

## Four ways to use it

### Web

Open [checkout.rozo.ai](https://checkout.rozo.ai), paste the payment link, pick a coin and send the exact amount shown.

### CLI

```bash
npx @rozoai/checkout quote <coinbase-link>
npx @rozoai/checkout pay <coinbase-link> --with usdt-solana --yes
```

`quote` is read-only. `pay` prints a deposit address (or a Lightning invoice) and waits until the invoice settles. No private key, no environment variable, no configuration. Agents and scripts should always pass `--with`; there is no default coin. Source: [RozoAI/rozo-checkout-skill](https://github.com/RozoAI/rozo-checkout-skill).

### MCP server

Remote MCP over streamable HTTP:

```
https://mcp.rozo.ai/mcp?src=docs
```

It exposes four tools: `supported_coins`, `quote_invoice`, `create_deposit_order` and `payment_status`. The server holds no private keys, signs nothing and never custodies funds; the user pays from their own wallet. An order that is never funded expires and costs nothing.

Claude Code:

```bash
claude mcp add --transport http rozo-checkout "https://mcp.rozo.ai/mcp?src=claude-code"
```

Claude Desktop or Claude.ai: Settings, Connectors, Add custom connector, URL `https://mcp.rozo.ai/mcp?src=claude`. For a local `claude_desktop_config.json`, use the `mcp-remote` bridge:

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

The endpoint only answers MCP `POST` requests, so opening it in a browser shows `405`. That is expected.

### Claude Code skill

```text
/plugin marketplace add RozoAI/rozo-checkout-skill
/plugin install rozo-checkout@rozo
```

The skill wraps the same CLI, so it pays from your own wallet without a key.

## Fees and timing

* **Fee.** ROZO's service fee is included in the quote, shown before you pay. You pay the full invoice amount plus the fee, as the exact deposit amount in your order. The network fee for sending your coin goes to the blockchain, not to ROZO. Lightning and native coin payments also include a conversion spread built into the coin amount.
* **Quote validity.** A quote (`quoteReceipt`) is valid for about 60 seconds. Creating the order takes a fresh quote.
* **Order deadline.** Each deposit order has its own expiry, returned when the order is created (`expiresAt`). It is also bounded by the expiry of the Coinbase link itself. Pay before the earlier of the two.
* **Refunds.** Crypto top-ups to OpenRouter are never refundable. That is OpenRouter's policy. Check the credit amount before you pay.
* **Minimum.** OpenRouter sets its own minimum top-up; see [Pay OpenRouter with crypto](https://checkout.rozo.ai/blog/pay-openrouter-with-crypto).

## Paid but credits did not arrive

Do not pay again. Follow [OpenRouter payment troubleshooting](https://checkout.rozo.ai/help/openrouter-payment-troubleshooting), or email hi@rozo.ai with your payment link and transaction hash.
