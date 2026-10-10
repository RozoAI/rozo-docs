---
description: >-
  Buy OpenRouter credits in bulk, or let an AI agent top up on behalf of users.
  Three self-serve ways in: the CLI, the MCP server and the public HTTP API. No
  account and no API key.
icon: robot
---

# Bulk Purchases and Agents

This page is for anyone who pays more than the occasional invoice through [ROZO Checkout](README.md):

* **Resellers** who buy OpenRouter credits for their own customers.
* **Teams** that top up several OpenRouter accounts on a schedule.
* **AI agents** that top up OpenRouter, or pay another Coinbase-hosted invoice, on behalf of a user.

Paying x402 APIs instead of Coinbase invoices? See [x402 Payer](x402-payer.md).

Everything here is self-serve. There is no account to create, no API key to request and no private key to share. Each OpenRouter top-up is its own Coinbase payment link, so a batch is a loop over links: one order per link, one payment per order.

## Three ways in

All three use the same public backend and the same safety rules. Pick the one your tooling speaks.

### 1. CLI (`@rozoai/checkout` on npm)

Install once so each run skips the `npx` download:

```bash
npm i -g @rozoai/checkout
```

Then, per link, non-interactively:

```bash
rozo-checkout pay <coinbase-link> --with usdt-solana --yes --json --no-watch
rozo-checkout status <rozoPaymentId> --json
rozo-checkout receipt <rozoPaymentId> --json
```

Or without installing: `npx @rozoai/checkout pay <coinbase-link> --with usdt-solana --yes --json --no-watch`.

* `--with` is required for scripts and agents; there is no default coin. Accepted values: `usdt-solana`, `usdc-solana`, `usdt-bnb`, `usdc-bnb`, `usdt-ethereum`, `usdc-ethereum`, `usdt-polygon`, `usdc-polygon`, `usdc-base`, `usdc-stellar`, `btc-lightning`.
* `--yes` is required when stdin is not a terminal. `--json` prints exactly one JSON object on stdout.
* `--no-watch` returns as soon as the deposit details exist. Without it, `pay --json` waits for settlement before printing anything.
* A successful `pay --no-watch` means the order and its deposit details exist. **No money has moved yet.** The payer then sends the exact amount in `order.deposit`.
* Exit codes: `0` ok, `1` refused or failed (read `error.code`), `2` usage error (nothing was created), `3` the watch window ended before a final state (money may be in flight; do not pay again).

A complete batch script with a per-link log is in the CLI README: [Paying many invoices (batch / resellers)](https://github.com/RozoAI/rozo-checkout-skill#paying-many-invoices-batch--resellers).

### 2. MCP server

Remote MCP over streamable HTTP:

```
https://mcp.rozo.ai/mcp
```

It exposes four tools: `supported_coins`, `quote_invoice`, `create_deposit_order` and `payment_status`. The flow is `quote_invoice`, then `create_deposit_order`, then the user sends from their own wallet, then `payment_status`. The server holds no private keys and never custodies funds. Setup for Claude Code, Claude Desktop and Claude.ai is on the [ROZO Checkout](README.md#mcp-server) page.

### 3. Raw HTTP

Four public calls, no API key. Base URLs:

* Router: `https://apiserver.mpprouter.dev/v1/services/rozo-agent-api`
* Payment record: `https://intentapiv4.rozo.ai/functions/v1/payment-api`

**Step 1. Quote (read-only).**

```bash
curl -X POST https://apiserver.mpprouter.dev/v1/services/rozo-agent-api/quote-invoice \
  -H 'content-type: application/json' \
  -d '{"url":"https://payments.coinbase.com/payment-links/pl_XXXX"}'
```

Returns the merchant, the invoice amount, the price breakdown (`original`, `serviceFee`, `callerPays`) and a signed `quoteReceipt`. The receipt is valid for about 60 seconds.

**Step 2. Create (or reuse) the order.**

```bash
curl -X POST https://apiserver.mpprouter.dev/v1/services/rozo-agent-api/create-invoice \
  -H 'content-type: application/json' \
  -d '{"url":"https://payments.coinbase.com/payment-links/pl_XXXX",
       "source":{"chainId":"900","tokenSymbol":"USDT"},
       "quoteReceipt":"<from step 1>",
       "client":"my-agent/1.0"}'
```

Returns `rozoPaymentId`, `reused`, `source`, `expiresAt` and a hosted `paymentLink`. `client` is an optional free-text label for our reporting; it is never used for authentication or pricing. An optional `email` lets us reach you if an order needs attention.

Source chain ids: `"1"` Ethereum, `"56"` BNB Chain, `"137"` Polygon, `"42161"` Arbitrum, `"8453"` Base, `"900"` Solana, `"1500"` Stellar, `"lightning"` Bitcoin Lightning.

**Step 3. Read the deposit instructions.**

```bash
curl https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/<rozoPaymentId>
```

Before sending anything, confirm all of these in the same run. If any check fails, do not pay; poll status instead:

* `status` is `payment_unpaid`, and `source.txHash`, `source.confirmedAt` and `source.amountReceived` (null or `"0"`) show no pay-in yet.
* The returned order's `source` matches the chain and token you asked for (a reused order keeps its own rail).
* The order is still payable: `invoice-status` (step 4) does not show the link as paid or expired.
* There is time left: now is earlier than the order `expiresAt` and the payment link's own expiry, minus a margin (10 minutes for EVM chains and Stellar, 5 for Solana; only pay a Lightning invoice with at least 10 minutes of validity left).

Then pay exactly `source.amount` to `source.receiverAddress`, once. On Stellar also send `source.receiverMemo` as a text memo (`MEMO_TEXT`, even when it looks numeric). For Lightning, pay the BOLT11 in `source.lnInvoice`; the amount is in satoshis when `source.amountUnit` is `sats`.

**Step 4. Poll until settled.** See [Receipts and status](#receipts-and-status).

The full agent-oriented reference for these calls, including every safety check, is at [checkout.rozo.ai/llms.txt](https://checkout.rozo.ai/llms.txt).

## Supported pay-in rails

| Type | What you can pay with | CLI and MCP | Raw HTTP and web |
| --- | --- | --- | --- |
| Stablecoins | USDC or USDT on Solana, Ethereum, BNB Chain or Polygon; USDC on Base or Stellar | Yes | Yes |
| Stablecoins | USDC or USDT on Arbitrum | No | Yes |
| Bitcoin | BTC over Lightning | Yes | Yes |
| Native coins | ETH on Ethereum, Base or Arbitrum; BNB on BNB Chain; SOL on Solana; POL on Polygon (Beta) | No | Yes, when `quote-invoice` lists the coin in `supportedSources` and the invoice is within the native limit below |

USDT is not accepted on Base or Stellar. On-chain Bitcoin and Tron are not accepted. Lightning and native coin orders include a conversion spread in the coin amount, and a native coin price is locked only until the quote expires. Native coin orders are limited to $2,000 per invoice, fee included; above that, `create-invoice` answers `UNSUPPORTED_SOURCE`, so pay large invoices with a stablecoin.

## Fees

ROZO charges a **1% service fee** on top of the merchant invoice amount, rounded up to the next cent. It applies to every invoice paid through ROZO Checkout, whichever merchant the link belongs to. The quote returns `original`, `serviceFee` and `callerPays` before anything is created, so an agent always knows the total before a user pays. The network fee for sending your coin goes to the blockchain, not to ROZO.

OpenRouter's own crypto fee is already inside the Coinbase link amount. Crypto top-ups to OpenRouter are never refundable; that is OpenRouter's policy.

## Rate limits <a href="#rate-limits" id="rate-limits"></a>

Order creation (`create-invoice`) is rate limited per IP address. Quotes and status reads are cheap, but do not poll faster than you need to.

* Per-IP limits apply to every caller.
* A history of paid orders raises the limit for that caller.
* Need more headroom than that? Email [hi@rozo.ai](mailto:hi@rozo.ai) and ask about an API key.

Every `create-invoice` call counts toward the limit, including a retry that returns the same order. The current numbers are published in the API reference. When you hit the limit, `create-invoice` answers HTTP `429` with code `RATE_LIMITED`. Wait, then resume with the links that are not yet `settled`. Retrying an order you already created is safe (see below); hammering the endpoint is not.

## Idempotency and error codes

**Creating is idempotent per link. Paying is not.**

* `create-invoice` is keyed by the Coinbase link. While that link's order is unpaid and unexpired, calling it again returns the same order with `reused: true`, not a second one.
* Once the order has moved past unpaid (a pay-in was seen, or it is bridging or paying the merchant), creating again answers `409 ORDER_ALREADY_ACTIVE`. Do not pay again; poll status.
* Only after an order expired with nothing received does create on the same link make a new order.
* Use the same source coin on every attempt for a link. If an open order already exists on another rail, the response echoes the order's real `source`, and `sourceMismatch: true` plus a `warnings` entry when it could not switch. Always compare the returned `source` with what you asked for, and abort on a mismatch. (The web checkout shows this case as `WRONG_SOURCE_RAIL`.)

Codes an agent should handle. Errors are JSON; read the code from `error.code`, or from a top-level `code` where `error` is a plain string.

| Code | HTTP | Meaning | What to do |
| --- | --- | --- | --- |
| `LINK_NOT_PAYABLE` | 422 | The upstream provider refused to quote this link. | Do not retry the same link. Ask the user for a new payment link. |
| `LINK_NOT_FOUND` | 404 | No such payment link, or it is mistyped. | Check the URL; ask for a new link. |
| `LINK_USED_OR_EXPIRED` | 409 / 410 | The Coinbase link is already paid or has expired. | Check the merchant balance; get a new link if it was not credited. |
| `ORDER_ALREADY_ACTIVE` | 409 | An order for this link is funded or in flight. | Never pay again. Poll status. |
| `PAYMENT_EXPIRED` | 409 | An earlier order for this link expired. | `retryable: true`: wait a few minutes and retry the same create. `confirmed: true`: get a new link. |
| `UNSUPPORTED_SOURCE` | 400 | The chain and token pair is not accepted. | Pick a pair from the `supported` list in the response. |
| `QUOTE_RECEIPT_INVALID_OR_EXPIRED` | 409 | The `quoteReceipt` is older than about 60 seconds or was altered. | Quote again, then create. |
| `RATE_LIMITED` | 429 | Per-IP creation limit reached. | Back off; see [Rate limits](#rate-limits). |

## Receipts and status <a href="#receipts-and-status" id="receipts-and-status"></a>

Always track orders by `rozoPaymentId`. A link-only lookup cannot see the pay-in.

**CLI.** `rozo-checkout status <rozoPaymentId> --json` returns `state`, plus the simpler `paymentOutcome` and `nextAction`. `nextAction.canSend` is the only field that permits paying. `rozo-checkout receipt <rozoPaymentId> --json` gives a yes or no: exit `0` only when Coinbase itself reports the invoice paid, `3` while the payment is in flight or unknown, `1` if the order expired unpaid or needs a human.

**Raw HTTP.** Poll both:

```bash
curl "https://apiserver.mpprouter.dev/v1/services/rozo-agent-api/invoice-status?rozo_payment_id=<rozoPaymentId>"
curl https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/<rozoPaymentId>
```

The Coinbase link is settled only when `invoice-status` reports `coinbase.settled: true` and `routerState.status` is `paid`. An intents status of `payment_completed` on its own is the bridge leg, not final settlement.

What the outcomes mean:

| `paymentOutcome` | Terminal? | Meaning | What to do |
| --- | --- | --- | --- |
| `awaiting_payment` | No | Order is open and unfunded. | Pay once, only if `nextAction.canSend` is true. |
| `processing` | No | Money is moving: pay-in detected, bridging or paying the merchant. | Wait and poll. Never pay again. |
| `settled` | Yes | The merchant invoice is paid, proved by Coinbase. | Done. Skip this link. |
| `expired_unfunded` | Yes | Nothing arrived and the order is dead. | Check your own wallet first. If nothing was sent, run `pay` (or create) again on the same link for a new order. Never fund the old deposit address. |
| `needs_attention` | Yes, until a human acts | Underpaid, stuck after payment, or otherwise not clean. | Do not pay again. Contact support with `linkId`, `rozoPaymentId` and every transaction hash. |
| `unknown` | No | The backend could not be read. This is not proof that nothing was paid. | Retry the status read, never the payment. |

ROZO cannot see the OpenRouter balance, so credit delivery is always reported as `unknown`. Check the OpenRouter account to confirm the credits.

## Support

Email [hi@rozo.ai](mailto:hi@rozo.ai) with the payment link, `rozoPaymentId` and transaction hash, or reach us on [Discord](https://discord.com/invite/EfWejgTbuU) or [X](https://x.com/ROZOai).
