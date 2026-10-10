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

x402 balance top ups accept USDC and USDT only. A top up request for any other coin is answered with `X402_TOPUP_SOURCE_UNSUPPORTED` and no deposit address. Holding a native coin or sats? Use them to top up OpenRouter with [ROZO Checkout](https://checkout.rozo.ai).

**Payment leg (ROZO to the x402 seller)**

| Network | Asset | x402 scheme |
| --- | --- | --- |
| Base (`eip155:8453`) | USDC | `exact` |
| Solana | Coming later | An endpoint that only accepts USDC on Solana is refused before anything is charged. |

Sellers are always paid in USDC on Base, because x402 `exact` payments are token transfers; from a balance funded with USDT, ROZO pays the seller in USDC.

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

### CLI codes

The CLI raises these on its own, before or after talking to ROZO.

| Code | Meaning | What to do |
| --- | --- | --- |
| `X402_UNSUPPORTED` | The endpoint does not accept USDC on Base, for example it only accepts Solana. Nothing is charged. | Tell the user the endpoint is not covered yet. Do not try to bridge per call. |
| `X402_OVER_BUDGET` | Every payable option is above `--max-usd`. Nothing is charged. | Ask the user before raising `--max-usd`. |
| `X402_PAYER_DISABLED` | The CLI's name for any server 503 except the three retryable ones. The server code is in `error.details.serverCode`. | Stop and tell the user. |

On `/sign` the CLI retries 429, 500, 502, 504 and the 503 codes `X402_RETRY`, `X402_PAYER_MODE_CHANGED` and `X402_LEDGER_UNAVAILABLE` itself, with the same `idempotencyKey`.

### Server codes

What `https://apiserver.mpprouter.dev/v1/x402/*` returns. Every error body looks like `{"ok":false,"code":"X402_...","error":{"code":"X402_...","message":"..."}}`, sometimes with extra top level fields such as `limitUsd` or `balanceUsd`.

The balance is debited only by the ledger commit inside `/sign`, after signing; every error raised before that commit charges nothing. If `/sign` answers `X402_LEDGER_UNAVAILABLE` or `X402_INTERNAL` the commit may have landed: retry with the same `idempotencyKey`, and a payment that did land comes back as the stored signature (`"replay": true`), never as a second charge. On `/topup` no deposit address is shown on any error, so only pay an address from a 200 response.

| Endpoint | HTTP | Code | Meaning | Charged? | What to do |
| --- | --- | --- | --- | --- | --- |
| `/balance`, `/topup`, `/sign` | 401 | `X402_KEY_INVALID` | Agent key missing, malformed or unknown. | No | Send `Authorization: Bearer ak_...`. Do not mint a new key to get around it: the balance belongs to the old key. |
| `/balance`, `/topup`, `/sign` | 403 | `X402_KEY_SUSPENDED` | The key is not active. | No | Stop. Email hi@rozo.ai. |
| any | 503 | `X402_PAYER_DISABLED` | The payer is switched off. | No | Stop and tell the user. |
| any | 503 | `X402_PAYER_NOT_CONFIGURED` | The payer is not set up on this deployment. | No | Stop. |
| any | 503 | `X402_LEDGER_UNAVAILABLE` | The balance ledger is unreachable. | No. On `/sign` the outcome can be unknown, see below the table. | Retry shortly with the same `idempotencyKey`. |
| any | 500 | `X402_INTERNAL` | Unexpected server error. | No. On `/sign` the outcome can be unknown, see below the table. | Retry with the same `idempotencyKey` a few times, then stop and report it. |
| any | 405 | `METHOD_NOT_ALLOWED` | Wrong HTTP method. | No | `keys`, `topup` and `sign` are POST; `balance` is GET. |
| `/keys` | 429 | `X402_KEY_RATE_LIMITED` | Too many keys created from this IP this hour. | No | Reuse the key you have, or retry later. |
| `/keys` | 503 | `X402_RETRY` | Key collision. | No | Retry. |
| `/topup` | 400 | `X402_INVALID_REQUEST` | Body is not JSON, or `amount` is not a USD amount with at most 2 decimals. | No | Fix the request. |
| `/topup` | 400 | `X402_TOPUP_AMOUNT_OUT_OF_RANGE` | A top up must be between $5 and $500. | No | Pick an amount in range. |
| `/topup` | 400 | `X402_TOPUP_SOURCE_REQUIRED` | `chain` and `token` are missing. The response lists accepted chains. | No | Say which coin you pay with. |
| `/topup` | 400 | `X402_UNSUPPORTED_CHAIN` | Unknown chain. | No | Use a CAIP-2 id or a name such as `solana`, `base`, `ethereum`, `bsc`, `polygon`, `arbitrum`, `stellar`. |
| `/topup` | 400 | `X402_TOPUP_SOURCE_UNSUPPORTED` | That coin is not accepted for top ups. May carry a `supported` list. | No | Use USDC or USDT. |
| `/topup` | 502 | `INTENTS_API_FAILED` | The top up order could not be created. | No, no address was shown | Retry later. |
| `/topup` | 503 | `X402_TOPUP_MISCONFIGURED`, `X402_TOPUP_NOT_REGISTERED` | The order was not usable, so the deposit address was withheld. | No, no address was shown | Retry later; email hi@rozo.ai if it repeats. |
| `/topup` | 503 | `X402_PAYER_SHADOW`, `X402_TOPUP_NOT_CONFIGURED`, `X402_SIGNER_NOT_CONFIGURED` | Top ups are closed right now. | No | Stop. |
| `/sign` | 400 | `X402_INVALID_REQUEST` | Body is not JSON, or `budget` is not a positive USD amount. | No | Fix the request. |
| `/sign` | 400 | `X402_IDEMPOTENCY_KEY_REQUIRED` | `idempotencyKey` missing or invalid: 8 to 128 chars of `[A-Za-z0-9_.:-]`. | No | Send one key per 402 challenge. |
| `/sign` | 400 | `X402_UNSUPPORTED_VERSION` | Only `x402Version` 2 is accepted. | No | Send the v2 requirement. |
| `/sign` | 400 | `X402_UNSUPPORTED_NETWORK`, `X402_UNSUPPORTED_SCHEME`, `X402_UNSUPPORTED_ASSET`, `X402_INVALID_REQUIREMENT`, `X402_SIGN_UNSUPPORTED` | The `accepts` entry is malformed or asks for something not covered (only `exact` USDC is signed). | No | Do not retry the same entry. Tell the user. |
| `/sign` | 402 | `X402_BUDGET_EXCEEDED` | The challenge asks more than your `budget`. | No | Stop and ask the user. |
| `/sign` | 402 | `X402_PER_TX_LIMIT_EXCEEDED` | Above this key's single-payment limit (`limitUsd`). | No | Stop and ask the user. |
| `/sign` | 402 | `X402_INSUFFICIENT_BALANCE` | Balance too low (`balanceUsd`). | No | Top up, wait for the credit, then pay again. |
| `/sign` | 403 | `X402_PAYTO_NOT_ALLOWED` | `payTo` is not on this key's allowlist. | No | Stop. |
| `/sign` | 403 | `X402_PAYTO_BLOCKED` | This `payTo` is blocked. | No | Stop. Do not retry. |
| `/sign` | 409 | `X402_IDEMPOTENCY_CONFLICT` | This `idempotencyKey` was already used for a different requirement. | No new charge | Use a new key only for a new 402 challenge. |
| `/sign` | 410 | `X402_CREDENTIAL_REFUNDED` | The stored signature expired unused and its amount went back to the balance. | Refunded | Fetch a new 402 and sign it with a new key. |
| `/sign` | 429 | `X402_DAILY_LIMIT_EXCEEDED` | This key's daily limit would be exceeded (`limitUsd`, `spentTodayUsd`). | No | Wait for the daily window to reset, or ask hi@rozo.ai for a higher limit. |
| `/sign` | 429 | `X402_GLOBAL_DAILY_CAP_REACHED`, `X402_SIGNER_DAILY_CAP_REACHED` | A platform-wide daily cap was reached. | No | Retry after 00:00 UTC. |
| `/sign` | 429 | `X402_SIGNER_CAP_REACHED` | The signing service refused this amount. | No | Try a smaller payment or later. |
| `/sign` | 503 | `X402_RETRY`, `X402_PAYER_MODE_CHANGED` | Transient. | No | Retry with the same `idempotencyKey`. |
| `/sign` | 503 | `X402_PAYER_SHADOW` | The payer is not live for this key. A fresh request is checked and recorded but not signed. With `"replay": true` it refers to an earlier payment under this `idempotencyKey`. | No for a fresh request. A replay may refer to an earlier charged payment. | Stop. On a replay check `/balance` and never pay again with a new key. |
| `/sign` | 503 | `X402_SIGNER_NOT_CONFIGURED`, `X402_SIGNER_DISABLED` | Signing for this network is off right now. | No | Stop. |

A 200 with `"replay": true` is the stored signature for an `idempotencyKey` that was already paid. It is not a second charge.

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
