---
description: >-
  Pay any x402 API that asks for USDC on Base from a ROZO balance you top up
  once with the coin you already hold. Three CLI commands or two HTTP calls.
icon: bolt
---

# x402 Payer

An x402 endpoint answers `402 Payment Required` and asks for USDC. ROZO pays the ones that want USDC on Base. You top up a ROZO balance once with the coin you have, and every later x402 call is paid from that balance in seconds.

Each payment is one-off, not a subscription. Every paid call gets its own 402 from the seller and its own signature from ROZO, so the seller never holds a standing authorization to charge you again.

The human-readable guide is at [checkout.rozo.ai/x402](https://checkout.rozo.ai/x402). The agent reference is in [checkout.rozo.ai/llms.txt](https://checkout.rozo.ai/llms.txt).

## Three commands

If your agent can run a shell command, this is the whole integration.

```bash
# 1. Fund the balance once. Prints a one-time deposit address; pay it from your own wallet.
npx @rozoai/checkout x402 topup 20 --with usdt-solana
# 2. Call a paid endpoint. Reads the 402, ROZO signs, the request is sent again with the payment.
npx @rozoai/checkout x402 pay https://api.example.com/v1/search --method POST --body '{"q":"..."}'
# 3. See what is left.
npx @rozoai/checkout x402 balance
```

What happens on `x402 pay`:

1. Your machine sends the request straight to the endpoint. ROZO never sees the request body, your headers or the API keys you use for that service.
2. On a 402 the CLI reads the payment requirements, keeps only USDC on Base, and refuses anything above `--max-usd` (default `1.00`).
3. It asks ROZO to sign one payment with a fresh `idempotencyKey`. A retry reuses the same key, so a timeout can never charge you twice.
4. It sends the original request again with the `PAYMENT-SIGNATURE` header and prints the response.

The full option list for `x402 pay` (`--method`, `--body`, `--header`, `--max-usd`) is in [llms.txt](https://checkout.rozo.ai/llms.txt) and the [rozo-checkout-skill](https://github.com/RozoAI/rozo-checkout-skill) README.

## Raw HTTP: two calls

No shell? Use the same API directly. Send your agent key as `Authorization: Bearer ak_...`.

```bash
# Top up: returns a one-time deposit address for the coin you chose.
curl -s -X POST https://apiserver.mpprouter.dev/v1/x402/topup \
  -H 'authorization: Bearer ak_...' -H 'content-type: application/json' \
  -d '{"amount":"20","token":"USDT","chain":"900"}'
# Sign: pass the one requirement you picked from the 402 "accepts" list.
# Returns the value for the PAYMENT-SIGNATURE header. Replay your request with it.
curl -s -X POST https://apiserver.mpprouter.dev/v1/x402/sign \
  -H 'authorization: Bearer ak_...' -H 'content-type: application/json' \
  -d '{"accepts":[{"scheme":"exact","network":"eip155:8453","amount":"10000","asset":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913","payTo":"0x...","maxTimeoutSeconds":60}],"budget":"0.05","idempotencyKey":"<uuid>"}'
```

`POST /v1/x402/keys` creates the agent key (shown once). `GET /v1/x402/balance` returns the balance. Reuse the same `idempotencyKey` on every retry of one payment.

## Coverage

Two legs, listed apart on purpose: what you send ROZO, and what the seller receives.

**Top up leg (you to ROZO)**

| Coin | Chains |
| --- | --- |
| USDT | Solana, BNB Chain, Ethereum, Polygon |
| USDC | Solana, BNB Chain, Ethereum, Polygon, Base, Stellar |
| BTC | Lightning |
| ETH (native coin, beta) | Ethereum, Base, Arbitrum |
| BNB (native coin, beta) | BNB Chain |
| SOL (native coin, beta) | Solana |

**Payment leg (ROZO to the x402 seller)**

| Network | Asset | x402 scheme |
| --- | --- | --- |
| Base (`eip155:8453`) | USDC | `exact` |
| Solana | Coming later | An endpoint that only accepts USDC on Solana is refused before anything is charged. |

Native coins and USDT only fund the balance. Sellers are always paid in USDC on Base, because x402 `exact` payments are token transfers.

## Limits and keys

* **Per payment:** at most $5 by default, adjustable per key.
* **Per day:** at most $100 per key by default, adjustable per key.
* **payTo allowlist:** you can also restrict a key to a list of `payTo` addresses.
* **Minimum top up:** $5.
* **Fees:** the top up carries a 1% fee. Each x402 payment from the balance costs only what the seller asks; ROZO adds no fee to it.
* **Agent key:** the first top up creates a key that starts with `ak_`. It is shown once, and the CLI stores it in `~/.rozo-checkout/x402-key` with owner only permissions. ROZO keeps only a hash of it.
* **The key owns the balance.** Do not paste it into prompts, logs or tickets. If you lose it, create a new one and contact us to move the balance.
* **Withdrawals:** not self serve yet. Email [hi@rozo.ai](mailto:hi@rozo.ai) with your masked key (for example `ak_...a1b2`) and the amount.

## Error codes

| Code | Meaning | What to do |
| --- | --- | --- |
| `X402_UNSUPPORTED` | The endpoint does not accept USDC on Base, for example it only accepts Solana. Nothing is charged. | Tell the user the endpoint is not covered yet. Do not try to bridge per call. |
| `X402_RETRY`, `X402_PAYER_MODE_CHANGED` or `X402_LEDGER_UNAVAILABLE` (503) | A temporary condition on the ROZO side. | Retry with the same `idempotencyKey`. |
| Any other 503 from `/v1/x402` | The x402 payer is not enabled for this key. Nothing was charged. | Stop and tell the user. |

Never generate a new `idempotencyKey` when retrying one payment. A new key on retry can charge twice.

## FAQ

**Why do I have to top up first?**
An x402 payment requirement is valid for one to five minutes, while moving funds across chains takes longer. Paying from a balance that is already in place is the only way to answer inside that window. You top up rarely and in larger amounts; you pay often and in small ones.

**Where is my money?**
In your ROZO x402 balance. The funds sit in ROZO wallets, the one on Base signs the payments for your key, and the total of all balances is reconciled against those wallets every hour. ROZO never holds your own wallet keys.

**How do I get my balance back?**
Withdrawals are not self serve yet. Email [hi@rozo.ai](mailto:hi@rozo.ai) with your masked key (for example `ak_...a1b2`) and the amount, and we send it back on the chain you choose.

**Does ROZO see my request?**
No. The paid request goes from your machine to the endpoint. ROZO only sees the payment requirement it is asked to sign: who gets paid, how much, on which network.

**Which networks can the seller be paid on?**
USDC on Base (`eip155:8453`), x402 scheme `exact`. The Solana payment leg is coming later. If an endpoint only accepts Solana, the CLI stops with `X402_UNSUPPORTED` and nothing is charged.

Need an endpoint or payment network we do not cover yet? Email [hi@rozo.ai](mailto:hi@rozo.ai) with the endpoint you want to pay and the coin you hold.
