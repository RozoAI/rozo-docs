---
description: >-
  Pay a Coinbase-hosted invoice with Bitcoin sent on the Bitcoin network, not
  Lightning. One-time address per order, 1 to 3 confirmations, invoices from
  $10. Beta.
icon: bitcoin-sign
---

# On-chain Bitcoin (Beta)

ROZO Checkout accepts BTC sent on the Bitcoin network (chain id `9000`), in Beta. It is a separate rail from BTC over Lightning (chain id `lightning`): an on-chain order gives you a Bitcoin address, a Lightning order gives you a BOLT11 invoice, and one can never pay the other.

| | Bitcoin Lightning | Bitcoin (on-chain, Beta) |
| --- | --- | --- |
| You pay | A BOLT11 invoice from a Lightning wallet | A one-time `bc1q` address from any Bitcoin wallet or exchange |
| Chain id | `lightning` | `9000` |
| Settles after | Seconds | 1 to 3 confirmations, usually 10 to 60 minutes |
| Minimum invoice | OpenRouter's own minimum | $10 |

## On the web

Open [checkout.rozo.ai](https://checkout.rozo.ai), paste the payment link and pick **Bitcoin (on-chain)** in the network row (not Bitcoin Lightning). The page shows the exact BTC amount, the address, a QR code and the price timer. A short guide is at [checkout.rozo.ai/btc-onchain](https://checkout.rozo.ai/btc-onchain).

## With the API

The same three public calls as the rest of the checkout API (see [checkout.rozo.ai/llms.txt](https://checkout.rozo.ai/llms.txt)), with one difference: **both `quote-invoice` and `create-invoice` must carry `?beta=btc`**. Without it, chain `9000` is never offered.

1. Quote: `POST https://apiserver.mpprouter.dev/v1/services/rozo-agent-api/quote-invoice?beta=btc` with `{"url": "<payment link>"}`. On-chain BTC is available for that invoice only when `supportedSources` lists `"9000": ["BTC"]`.
2. Create: `POST https://apiserver.mpprouter.dev/v1/services/rozo-agent-api/create-invoice?beta=btc` with the payment link, the `quoteReceipt` from step 1 and `source: {"chainId": "9000", "tokenSymbol": "BTC"}`. Check that the returned `source` is chain `9000` BTC: an unexpired order on the same link is reused as it is. For a chain `9000` order, use `raw.source.amount` for the exact BTC amount and `raw.source.receiverAddress` for the one-time address. Save the top-level `rozoPaymentId` for status checks and use `quoteExpiresAt` for the price-lock deadline.
3. Status: poll `GET https://apiserver.mpprouter.dev/v1/services/rozo-agent-api/invoice-status?rozo_payment_id=<rozoPaymentId>`. `rozoPayment.source.btc` reports progress: `payinState` (`awaiting`, `seen`, `eligible`, `underpaid`, `late_review`, `manual_review`, `reorged`, `expired`), `confirmations`, `requiredConfirmations` (1 to 3, by amount), `requiredSat` and `receivedSat`. For a real merchant invoice, `routerState.status: "paid"` confirms settlement. Once `payinState` is anything other than `awaiting`, do not pay again.

The CLI and the MCP server do not create on-chain BTC orders yet; the MCP server's `supported_coins` lists it under `webOnlyRoutes`.

## Rules

* Send exactly `raw.source.amount` BTC to `raw.source.receiverAddress` on the Bitcoin network, once, before the top-level `quoteExpiresAt` deadline. Your wallet's network fee goes on top.
* The address belongs to that order only. Never reuse it, and never copy it from wallet history: look-alike addresses send tiny payments to trick you.
* A Lightning wallet cannot pay this address, and a Lightning invoice is never an on-chain order.
* If the payment is not seen before the price timer ends, the order closes. If you sent less than asked, or the payment arrived after the order closed, do not send more: contact hi@rozo.ai with the payment link and your transaction ID.

## Fees

The BTC amount includes the 1% service fee and a 1% exchange rate margin. The network fee for sending your BTC goes to the miners, not to ROZO.

## Availability

On-chain Bitcoin is in Beta, for invoices from $10. Availability can change per invoice; when `quote-invoice` does not list it, pay with Bitcoin Lightning or another coin.
