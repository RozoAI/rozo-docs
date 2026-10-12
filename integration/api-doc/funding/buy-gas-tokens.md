---
description: >-
  native_only: pay with a supported stablecoin and receive only the native gas
  token of the destination chain. Gated beta.
---

# Buy Gas Tokens (`native_only`)

{% hint style="warning" %}
Gated beta. Read the [Funding API overview](README.md) first, and check `GET /funding/capabilities` for the chains and limits your app actually has.
{% endhint %}

Your user pays a supported stablecoin (for example USDC or USDT on Base) and receives **only** the native coin of the destination chain: ETH on Ethereum, Arbitrum or Base, POL on Polygon, BNB on BNB Chain, SOL on Solana, XLM on Stellar, HYPE on HyperEVM, when capabilities list them as `supported`.

There is **no stablecoin output**: no USDC is delivered and no USDC trustline is needed on Stellar. After shared fees, the whole source amount buys the native coin.

## 1. Quote

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/quotes \
  -H "X-API-Key: $ROZO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "mode": "native_only",
    "userRef": "user-123",
    "source": { "chainId": "8453", "assetId": "<Base USDC assetId from capabilities>", "amount": "3.00" },
    "outputs": [
      { "id": "native", "kind": "native", "chainId": "42161", "receiverAddress": "<user Arbitrum address>", "allocation": "all_after_fees" }
    ]
  }'
```

* `userRef` is your stable id for the end user (used for limits).
* Optional `outputs[0].minimumAmount` (in the native coin) makes the quote fail instead of delivering less.
* Optional `limits.maxTotalFeesUsd` makes the quote fail if the fees are higher.

The response contains `quoteId`, `planDigest`, `expiresAt`, the source valuation and price, each fee line, and the native leg with `minimumAmount` (coin amount), `budgetUsd`, `principalUsd` and `nativePriceUsd`. Nothing is reserved and there is no deposit address yet.

Common refusals: `limit_exceeded` (the native budget is outside the min/max in capabilities; `details` gives the range), `unsupported_route`, `unsupported_target`, `price_unavailable`, `inventory_unavailable`.

## 2. Create the order

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/orders \
  -H "X-API-Key: $ROZO_API_KEY" -H "Content-Type: application/json" \
  -H "Idempotency-Key: gas-order-123" \
  -d '{ "quoteId": "<quoteId>", "planDigest": "<planDigest>", "orderId": "order-123" }'
```

The order has `status: awaiting_payment` and a one-time `deposit`:

```json
"deposit": {
  "chainId": "8453",
  "assetId": "<Base USDC assetId>",
  "symbol": "USDC",
  "address": "<one-time deposit address>",
  "memo": null,
  "amount": "3",
  "payBefore": "2026-10-12T00:10:00.000Z"
}
```

Show the user exactly this amount, asset, chain and deadline. The address is valid for this order only.

## 3. Track delivery

```bash
curl -s https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/orders/<fundingId> \
  -H "X-API-Key: $ROZO_API_KEY"
```

`status` moves `awaiting_payment`, `source_confirming`, `funds_confirmed` / `executing`, then `completed` once the native leg is `confirmed` with a `txHash`. The leg's `deliveredAmount` is the coin amount sent.

## Stellar specifics

* An **existing** Stellar account receives XLM with a normal payment. It does **not** need a USDC trustline.
* A **new** (unfunded) G-address can be created with the XLM if capabilities list `stellar_account_unfunded` as supported for chain `1500`. The amount must be at least 1 XLM; the quote's `stellar` block shows `totalXlm`, `reserveXlm` (locked as the account's minimum balance) and `spendableXlm`.
* Contract (`C...`) addresses and exchange accounts that require a memo are not supported (`unsupported_target`).

## Solana specifics

A SOL delivery must cover the rent-exempt minimum of a new account; smaller amounts are refused at quote time.
