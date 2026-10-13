---
description: >-
  Funding API. One stablecoin payment opens a Stellar wallet (account, USDC
  trustline, USDC and XLM with one signature) or buys XLM gas. No API key.
icon: gas-pump
---

# Funding API

The Funding API lets your user pay **once**, in USDC or USDT on Base, Ethereum, Arbitrum or Polygon, and receive:

| Mode | The user receives | Page |
| --- | --- | --- |
| `stellar_onboarding` | USDC on Stellar. A new address, or one without a USDC trustline, also gets its account, the trustline and optional XLM, in one transaction it signs once. 1 to 1,000 USD per order. | [Open a Stellar Wallet](stellar-wallet-onboarding.md) |
| `native_only` | Only XLM on Stellar, no stablecoin. 1 to 10 USD of XLM per order. | [Buy Gas Tokens](buy-gas-tokens.md) |
| `native_and_stable` | One native coin output plus one stablecoin output. On request, for apps with an API key. | [Gas + Stablecoin Funding](gas-plus-stablecoin.md) |

**API host**: `https://intentapiv4.rozo.ai/functions/v1/payment-api`
**Contract**: [OpenAPI `openapi-funding-v1.2.0.yaml`](../../../docs/openapi-funding-v1.2.0.yaml) (version `1.2.0`).

Always read [capabilities](#discover-what-you-can-do) first: chains, assets, minimums and maximums on these pages are examples, the live values are in capabilities.

## No API key needed: the public app `rozoNativeGas`

Every call below works **without** a key. Keyless calls run as the shared public app `rozoNativeGas`:

* modes `stellar_onboarding` and `native_only`;
* 1 to 1,000 USD per order, 2,000 USD per client IP per day, 10,000 USD per day for all keyless traffic together;
* rate limited per client IP (`429 rate_limited`), and `userRef` is replaced by a per-IP value;
* the public app holds only a few unpaid orders at once; when it is busy, retry later or register your own app;
* keep the `fundingId` private: it is the only handle to a keyless order, and anyone holding it can read that order;
* lookup by `orderId` and Stellar ownership proofs need your own API key.

Send a normal `User-Agent` header; some default library user agents are refused at the edge.

## Your own app (optional)

Register on [partners.rozo.ai](https://partners.rozo.ai) for an app id and a server-side API key if you need your own limits, lookup by `orderId`, or `native_and_stable`. Ask ROZO to enable the Funding API for that app; registration alone grants no mode, chain or limit. Call with `X-API-Key` **from your backend only**, never from a browser, mobile app or agent. The key identifies your app; it does not authorize spending from the user's wallet.

## Flow

1. `GET /funding/capabilities`: what your app may fund right now.
2. `POST /funding/quotes`: a read-only, frozen plan with every fee and each output's guaranteed minimum. No deposit address yet, nothing reserved.
3. Show the plan to the user. They approve it.
4. `POST /funding/orders` with `quoteId`, the quote's `planDigest`, your `orderId` and an `Idempotency-Key` header. Inventory and limits are reserved atomically and a **one-time deposit** is returned.
5. The user sends one payment to `deposit.address` before `deposit.payBefore` (the quote's expiry, 10 minutes after quoting). Follow `deposit.amountPolicy`: `exact` requires the quoted amount; Stellar onboarding with `any_amount` uses the accepted range described below.
6. Poll `GET /funding/orders/{fundingId}` until `completed` (or `recovery_required`). For `stellar_onboarding`, sign once when the order asks for it.

## Discover what you can do

```bash
curl -s https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/capabilities \
  -H "User-Agent: my-app/1.0"
```

The response lists `modes`, `sourceAssets` (with `assetId`, min and max), `nativeOutputs` (with min/max/step in USD and which receiver kinds are supported), `stableOutputs`, every allowed `routes` combination, `limits`, `fees`, Stellar signer support and `gasOptions` (the fixed XLM tiers of `stellar_onboarding`). Anything not listed as `supported` is not available; each disabled item carries a `reason`. Cache the response no longer than `validUntil`.

`assetId` values are opaque identifiers taken from capabilities (for example `erc20:<contract>` or `stellar:USDC:<issuer>`). A ticker that looks similar does not imply support: USDT0, bridged USDC and EURC are separate assets.

## Amounts and fees

* Amounts are **decimal strings** in the asset's own unit (`"10.00"`, `"0.0021"`), never JSON numbers.
* Read `source.amountPolicy` on the quote and `deposit.amountPolicy` on the order. `exact` (also the fallback when the field is absent) requires the quoted amount. Outputs have a **guaranteed minimum** (`legs[].minimumAmount`) when that deposit is paid in full and on time.
* For Stellar onboarding with `any_amount`, `deposit.amount` is the suggested amount. A single on-time payment at or above `minAcceptedAmount` is priced on the amount received, using frozen prices and fees. The XLM tier stays the same; the remaining USDC is recalculated. Only up to `maxPricedAmount` and the remaining daily allowance is priced; excess is held for manual handling, with no automatic refund. If the remaining allowance cannot cover a deliverable amount, the whole payment requires recovery. Below the minimum, a wrong chain or asset, a late payment or a second payment requires recovery. Read the refreshed order's `legs`, `fees`, `totals` and `repricing` before signing. This XLM-tier behavior does not apply to other Funding modes.
* Every quote balances exactly: `sourceValueUsd = nativeBudgetsUsd + stableDeliveryUsd + sharedFeesUsd + roundingRemainderUsd`. Each fee line says which output it belongs to and whether it is refundable.
* Quote with the chain's USDC `assetId`. At payment, USDC or USDT on any enabled source chain is accepted 1:1 against the quoted amount; the one-time deposit address is the same on every enabled chain.
* Fees charged by the user's own wallet or exchange for the deposit transfer are outside this API: `externalSourceFee` is always `unknown`. The API cannot pay the gas of the user's first deposit transfer.
* `settlement.type = internal_settlement` describes where the deposit settles inside ROZO. It is not a stablecoin output to the user.

## Idempotency and retries

* `POST /funding/orders` requires `Idempotency-Key` (8 to 128 characters of `[A-Za-z0-9_.:-]`). Retrying with the same key and body returns the same order (`200`); the same key with a different body returns `409 idempotency_conflict`.
* A quote can create at most one order (`409 quote_consumed`), and only with its own `planDigest` (`409 plan_mismatch`).
* `orderId` is your reference and must be unique per app. Look an order up by it with `GET /funding/orders?orderId=<orderId>`.

## Order status

| `status` | Meaning |
| --- | --- |
| `awaiting_payment` | Waiting for the deposit. |
| `source_confirming` | Deposit seen, waiting for confirmations. |
| `funds_confirmed` / `executing` | Deposit final; outputs are being delivered. |
| `action_required` | The user must act (Stellar onboarding signature, see [Open a Stellar Wallet](stellar-wallet-onboarding.md#how-to-sign-and-claim)). |
| `completed` | **Every** output is confirmed on chain. The only success state. |
| `recovery_required` | Something needs ROZO to resolve: a late, short, over or wrong asset payment, or an output that failed. See `recovery`. |
| `expired_unpaid` | No deposit arrived in time. Nothing was charged. |
| `cancelled_unpaid` | Cancelled before any deposit. |

Each output (`legs[]`) has its own `status`: `planned`, `reserved`, `ready`, `submitting`, `unknown`, `confirmed`, `failed_confirmed`, with its `txHash` once delivered. `unknown` means ROZO is reconciling the outcome; it is never re-sent or refunded until the outcome is known. A partially delivered order is never `completed`: `recovery.deliveredLegIds` and `recovery.owedLegIds` say what arrived and what is still owed.

## Payments that do not match

* **Over** payments complete the order; the extra is not refunded automatically.
* **Late** (after `payBefore`) or **short** payments: the order moves to `recovery_required`. It is never re-priced at a new rate and never refunded automatically.
* **Wrong asset or wrong chain** (anything other than USDC or USDT on an enabled source chain, for example BSC): the order is flagged for recovery (`recovery.state = open`) but keeps waiting, so a correct deposit still completes it.
* Never send to a deposit address after its order has expired. Request a new quote.

## Errors

Every error has the same shape:

```json
{
  "code": "quote_expired",
  "message": "the quote expired; request a new quote",
  "retryable": false,
  "nextAction": "requote",
  "correlationId": "5d0f8c1e-..."
}
```

| HTTP | `code` |
| --- | --- |
| 400 | `invalid_request` |
| 401 | `unauthorized` |
| 403 | `app_not_enabled` |
| 404 | `not_found` |
| 409 | `idempotency_conflict`, `quote_consumed`, `plan_mismatch`, `inventory_unavailable`, `state_changed`, `channel_busy`, `recovery_required` |
| 410 | `quote_expired`, `challenge_expired`, `template_expired` |
| 422 | `unsupported_mode`, `unsupported_route`, `unsupported_asset`, `unsupported_target`, `limit_exceeded`, `fees_exceed_limit`, `ownership_required`, `ownership_invalid`, `signer_unsupported`, `stellar_account_not_ready`, `signature_invalid` |
| 500 | `internal_error` (retry with the same `Idempotency-Key`) |
| 429 | `rate_limited` |
| 503 | `funding_disabled`, `price_unavailable` |

Follow `nextAction` (`retry`, `requote`, `verify_ownership`, `change_request`, `poll_order`, `rebuild_signing_request`, `contact_support`). Send `X-Correlation-Id` to have it echoed in errors.

## Webhooks

Funding webhooks (`funding.action_required`, `funding.leg_confirmed`, `funding.completed`, `funding.recovery_required`) are part of the contract but are **not emitted yet**. Poll the order; polling is always the source of truth.
