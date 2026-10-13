---
description: >-
  native_only: pay USDC or USDT on Base, Ethereum, Arbitrum or Polygon and
  receive only XLM on Stellar. No API key.
---

# Buy Gas Tokens (`native_only`)

{% hint style="info" %}
No API key needed. Read the [Funding API overview](README.md) for statuses and errors, and `GET /funding/capabilities` for the live chains and limits. Need USDC on Stellar too, or a new Stellar wallet? Use [Open a Stellar Wallet](stellar-wallet-onboarding.md) instead: one order delivers USDC, the trustline and XLM.
{% endhint %}

Your user pays USDC or USDT on Base, Ethereum, Arbitrum or Polygon and receives **only** XLM on Stellar. Other native coins (ETH, POL, BNB, SOL, HYPE) are listed in capabilities and are not enabled today.

There is **no stablecoin output**: no USDC is delivered and no USDC trustline is needed. After fees, the whole source amount buys XLM.

| Item | Value |
| --- | --- |
| XLM per order | 1 to 10 USD worth |
| Fee | 5 % spread on the XLM price (`fees.nativeSpreadBps` = 500 in capabilities) |
| Pay with | USDC or USDT on Base, Ethereum, Arbitrum or Polygon, accepted 1:1. Quote with the chain's USDC `assetId` (see [the chain table](stellar-wallet-onboarding.md#supported-chains-and-tokens)) |
| Daily limits | Shared with the other keyless modes: 2,000 USD per client IP, 10,000 USD for all keyless traffic |

The quote is authoritative: read `fees`, `totals` and the leg's `minimumAmount` from it.

## 1. Quote

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/quotes \
  -H "Content-Type: application/json" -H "User-Agent: my-app/1.0" \
  -d '{
    "mode": "native_only",
    "source": { "chainId": "8453", "assetId": "erc20:0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", "amount": "3.00" },
    "outputs": [
      { "id": "native", "kind": "native", "chainId": "1500", "receiverAddress": "<Stellar G-address>", "allocation": "all_after_fees" }
    ]
  }'
```

* With your own API key, also send `X-API-Key` and a `userRef` (your stable id for the end user, used for limits). Keyless calls get a per-IP `userRef`.
* Optional `outputs[0].minimumAmount` (in XLM) makes the quote fail instead of delivering less.
* Optional `limits.maxTotalFeesUsd` makes the quote fail if the fees are higher.

The response contains `quoteId`, `planDigest`, `expiresAt` (10 minutes), the source valuation and price, each fee line, and the native leg with `minimumAmount` (XLM), `budgetUsd`, `principalUsd` and `nativePriceUsd`. Nothing is reserved and there is no deposit address yet.

Common refusals: `limit_exceeded` (the XLM budget is outside 1 to 10 USD; `details` gives the range), `unsupported_route`, `unsupported_target`, `price_unavailable`, `inventory_unavailable`.

## 2. Create the order

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/orders \
  -H "Content-Type: application/json" -H "User-Agent: my-app/1.0" \
  -H "Idempotency-Key: gas-order-123" \
  -d '{ "quoteId": "<quoteId>", "planDigest": "<planDigest>", "orderId": "order-123" }'
```

The order has `status: awaiting_payment` and a one-time `deposit`:

```json
"deposit": {
  "chainId": "8453",
  "assetId": "erc20:0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
  "symbol": "USDC",
  "address": "<one-time deposit address>",
  "memo": null,
  "amount": "3",
  "payBefore": "2026-10-12T00:10:00.000Z"
}
```

Show the user exactly this amount and deadline. The address is valid for this order only and is the same on all four chains; USDC or USDT on any of them is accepted.

## 3. Track delivery

```bash
curl -s https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/orders/<fundingId> \
  -H "User-Agent: my-app/1.0"
```

`status` moves `awaiting_payment`, `source_confirming`, `funds_confirmed` / `executing`, then `completed` once the native leg is `confirmed` with a `txHash`. The leg's `deliveredAmount` is the XLM sent. Keep the `fundingId` private: without an API key it is the only handle to the order.

## Stellar specifics

* An **existing** Stellar account receives XLM with a normal payment. It does **not** need a USDC trustline.
* A **new** (unfunded) G-address is created with the XLM. The amount must be at least 1 XLM; the quote's `stellar` block shows `totalXlm`, `reserveXlm` (locked as the account's minimum balance) and `spendableXlm`.
* Contract (`C...`) addresses and exchange accounts that require a memo are not supported (`unsupported_target`).
