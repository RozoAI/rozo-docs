---
description: >-
  Funding API (gated beta). One stablecoin payment buys native gas tokens,
  gas plus a stablecoin, or onboards a new Stellar wallet.
icon: gas-pump
---

# Funding API (gated beta)

{% hint style="warning" %}
**Gated beta, not generally available.** Every endpoint answers `503 funding_disabled` until ROZO enables the product, and each app needs an explicit grant (modes, chains, limits). Always read [capabilities](#discover-what-you-can-do) first: chains, assets, minimums and maximums on these pages are examples, not promises.
{% endhint %}

The Funding API lets your user pay **once, in a supported stablecoin**, and receive:

| Mode | The user receives | Page |
| --- | --- | --- |
| `native_only` | Only the native coin of the destination chain (ETH, SOL, XLM, BNB, POL, HYPE). No stablecoin output. | [Buy Gas Tokens](buy-gas-tokens.md) |
| `native_and_stable` | One native coin output plus one stablecoin output, on the same chain or two supported chains. | [Gas + Stablecoin Funding](gas-plus-stablecoin.md) |
| `stellar_onboarding` | A new or not yet ready Stellar account gets a USDC trustline, USDC and optionally spendable XLM, with one funding signature by the user. | [Stellar Wallet Onboarding](stellar-wallet-onboarding.md) |

**API host**: `https://intentapiv4.rozo.ai/functions/v1/payment-api`
**Contract**: [OpenAPI `openapi-funding-v1.1.0.yaml`](../../../docs/openapi-funding-v1.1.0.yaml) (version `1.1.0`).

## Before you start

1. Register your app on [partners.rozo.ai](https://partners.rozo.ai). You get an app id such as `wallet_<slug>` and a server-side API key.
2. Ask ROZO to enable the Funding API for that app. Registration alone does not grant any funding mode, chain or limit.
3. Call the API **from your backend only**, with `X-API-Key`. Never ship the key to a browser, mobile app or agent. The key identifies your app; it does not authorize spending from the user's wallet. The user always pays the deposit and signs Stellar transactions themselves.

## No API key yet? The public app `rozoNativeGas`

Agents and scripts that have not registered can call the plain gas flow without a key: `GET /funding/capabilities`, `POST /funding/quotes`, `GET /funding/quotes/{quoteId}`, `POST /funding/orders` and `GET /funding/orders/{fundingId}`. Such calls run as the shared public app `rozoNativeGas`:

* only `native_only`, with small limits (see capabilities);
* rate limited per client IP (`429 rate_limited`), and `userRef` is replaced by a per-IP value;
* the public app holds only a few unpaid orders at once; when it is busy, retry later or register your own app;
* keep the `fundingId` private: it is the only handle to a keyless order, and anyone holding it can read that order;
* lookup by `orderId`, Stellar ownership proofs and Stellar signing always need your own API key.

Send a normal `User-Agent` header; some default library user agents are refused at the edge.

## Flow

1. `GET /funding/capabilities`: what your app may fund right now.
2. `POST /funding/quotes`: a read-only, frozen plan with every fee and each output's guaranteed minimum. No deposit address yet, nothing reserved.
3. Show the plan to the user. They approve it.
4. `POST /funding/orders` with `quoteId`, the quote's `planDigest`, your `orderId` and an `Idempotency-Key` header. Inventory and limits are reserved atomically and a **one-time deposit** is returned.
5. The user sends **exactly** `deposit.amount` of `deposit.assetId` on `deposit.chainId` to `deposit.address` before `deposit.payBefore`.
6. Poll `GET /funding/orders/{fundingId}` until `completed` (or `recovery_required`).

## Discover what you can do

```bash
curl -s https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/capabilities \
  -H "X-API-Key: $ROZO_API_KEY"
```

The response lists `modes`, `sourceAssets` (with `assetId`, min and max), `nativeOutputs` (with min/max/step in USD and which receiver kinds are supported), `stableOutputs`, every allowed `routes` combination, `limits`, `fees`, and Stellar signer support. Anything not listed as `supported` is not available; each disabled item carries a `reason`. Cache the response no longer than `validUntil`.

`assetId` values are opaque identifiers taken from capabilities (for example `erc20:<contract>` or `stellar:USDC:<issuer>`). A ticker that looks similar does not imply support: USDT0, bridged USDC and EURC are separate assets.

## Amounts and fees

* Amounts are **decimal strings** in the asset's own unit (`"10.00"`, `"0.0021"`), never JSON numbers.
* The source amount is fixed (`exactIn`). Outputs have a **guaranteed minimum** (`legs[].minimumAmount`) when the deposit is paid in full and on time.
* Every quote balances exactly: `sourceValueUsd = nativeBudgetsUsd + stableDeliveryUsd + sharedFeesUsd + roundingRemainderUsd`. Each fee line says which output it belongs to and whether it is refundable.
* 1 USDT is not assumed to equal 1 USD: the quote shows the source price used.
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
| `action_required` | The user must act (Stellar onboarding signature). |
| `completed` | **Every** output is confirmed on chain. The only success state. |
| `recovery_required` | Something needs ROZO to resolve: a late, short, over or wrong asset payment, or an output that failed. See `recovery`. |
| `expired_unpaid` | No deposit arrived in time. Nothing was charged. |
| `cancelled_unpaid` | Cancelled before any deposit. |

Each output (`legs[]`) has its own `status`: `planned`, `reserved`, `ready`, `submitting`, `unknown`, `confirmed`, `failed_confirmed`, with its `txHash` once delivered. `unknown` means ROZO is reconciling the outcome; it is never re-sent or refunded until the outcome is known. A partially delivered order is never `completed`: `recovery.deliveredLegIds` and `recovery.owedLegIds` say what arrived and what is still owed.

## Payments that do not match

* **Late** (after `payBefore`), **short** or **over** payments: the order moves to `recovery_required`. It is never re-priced at a new rate and never refunded automatically.
* **Wrong asset or wrong chain**: the order is flagged for recovery (`recovery.state = open`) but keeps waiting, so a correct deposit still completes it.
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
| 503 | `funding_disabled`, `price_unavailable` |

Follow `nextAction` (`retry`, `requote`, `verify_ownership`, `change_request`, `poll_order`, `rebuild_signing_request`, `contact_support`). Send `X-Correlation-Id` to have it echoed in errors.

## Webhooks

Funding webhooks (`funding.action_required`, `funding.leg_confirmed`, `funding.completed`, `funding.recovery_required`) are part of the contract but are **not emitted during the gated beta**. Poll the order; polling is always the source of truth.
