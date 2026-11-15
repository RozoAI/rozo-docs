# TRON USDT pay-in, settle in Base USDC (Beta)

{% hint style="info" %}
**Beta.** Any wallet or merchant with a valid Rozo API key can use this route, and anyone can use it without an API key on [intents.rozo.ai/bridge](#in-the-rozo-bridge-app). There is no invite list. Fees, limits and behavior may change while the beta runs. This page makes no settlement time promise.
{% endhint %}

The payer sends USDT on TRON to a payment address issued for one order. Rozo confirms the transfer on chain and pays USDC on Base to the receiving address set on your order.

This route works like [TRON USDT pay-in, settle in Stellar USDC](usdt-tron-to-usdc-stellar.md), with the same fee rules, amount rules, payment flow and status lifecycle. This page describes what is different for a Base destination and repeats the parts you need to integrate.

| Side | Chain | Chain ID | Token | Asset | Decimals |
| --- | --- | --- | --- | --- | --- |
| Pay in | TRON | `728126428` or `tron` | USDT (TRC20) | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | 6 |
| Pay out | Base | `8453` | USDC | `0x833589fcd6edb6e08f4c7c32d4f71b54bda02913` | 6 |

## Who can use it, and what is excluded

* **Who:** any app (wallet or merchant) with a valid `X-API-Key`. Anonymous orders are not accepted. See [Merchant API Keys](../merchant-api-keys.md).
* **Direction:** one way only. USDT on TRON in, USDC on Base out.
* **Not offered on this route:** TRX (the TRON native coin), USDT payouts, TRON as a payout chain, Base to TRON, and a memo on the payout.
* **Merchants with a configured payout chain:** if your merchant account settles to a payout chain set in its settings, this route does not apply to it.
* This route is not a row in the `data` list of `GET /payments/supported`. When it is enabled, it is described in the optional `paymentOptions` list of the same response, with `"route": "tron_usdt_to_base_usdc"`. See [Supported Tokens and Chains](../supported-tokens-and-chains.md#payment-options).

## Before you start

* The receiving address is an EVM address: `0x` followed by 40 hexadecimal characters. A mixed case address must have a valid checksum. The zero address and the USDC token contract itself are refused.
* Use an address that can hold USDC on Base. If it is an exchange deposit address, check that the exchange accepts USDC on Base.
* Do not send `receiverMemo`: Base payouts carry no memo. A request with a memo is refused.
* Keep your API key on your server. Never ship it to a browser or mobile app.

## Amounts, fees and limits

The rules are the same as on the Stellar route. The fee for a given amount is calculated for this route and can differ from a Stellar quote for the same amount; always read it from this route's quote. See [Amounts: gross and net](usdt-tron-to-usdc-stellar.md#amounts-gross-and-net), [Fees](usdt-tron-to-usdc-stellar.md#fees) and [Limits](usdt-tron-to-usdc-stellar.md#limits). In short:

* `exactOut` orders: you enter the net USDC the receiver gets on Base; the payer sends the gross USDT.
* **Rozo service fee:** a dynamic rate with a **0.20% floor**, and a **0.50 USD minimum** per order. The 0.50 USD minimum replaces the percentage fee on small orders; it is not added on top of it.
* **Partner fee:** charged separately if your app has one configured. See [Partner Fee](../api-for-advanced-used/partner-fee.md).
* **Network fee:** the payer pays the TRON network fee (Energy / TRX) from their own wallet. It is not part of the Rozo fee.
* **Minimum:** the rounded gross amount to pay must be at least 1 USDT.
* **Per-order maximum:** there is a per-order maximum, checked on the rounded gross amount (fees included). Read the current value from the quote.
* **Shared daily capacity:** TRON pay-ins have a daily capacity per UTC day that is shared by all apps on the platform and by both TRON routes (Stellar and Base). It resets at 00:00 UTC.
* **Payout capacity:** each order reserves Base USDC for its payout when the payment option is created. If none can be reserved, no payment address is issued.

Read `paymentOption.limits.minGrossUsd`, `paymentOption.limits.maxGrossUsd`, `paymentOption.available` and `availabilityReason` from the quote instead of hardcoding numbers.

## How to integrate

The flow is the same as on the Stellar route: quote (optional, no side effects), then two calls to create the payment option.

### 1. Get a quote (optional)

`POST /payment-api/payments?dryrun=true` with a TRON USDT source and a Base USDC destination. The quote does not create an order, does not reserve capacity, and does not issue an address. `receiverAddress` is optional on a quote; without it the receiver checks do not run.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments?dryrun=true' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "exactOut",
    "provider": "rozo",
    "source": { "chainId": "728126428", "tokenSymbol": "USDT" },
    "destination": {
        "chainId": "8453",
        "tokenSymbol": "USDC",
        "amount": "100.00",
        "receiverAddress": "<your user Base address>"
    }
}'
```

The response has the same shape as the Stellar quote. Check that `paymentOption.route` is `tron_usdt_to_base_usdc`; treat any other answer, or a non-200 response, as "route not available". Read the fee and the amount to pay from `source.amount`, `source.fee` and `paymentOption.fees`.

### 2. Create the order

Create an `exactOut` order that pays USDC on Base (`8453`), with `"provider": "rozo"` set explicitly. `orderId` is your own unique reference. `destination.amount` is the net USDC amount, with at most 6 decimals. Do not send `receiverMemo`.

The order create call does not accept TRON as a source, so set the source to USDC on Base (`8453`). This is a placeholder: the order gets its own Base deposit address as usual. **Never show that address to the payer.** The payer pays only the TRON option from step 3.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "<your appId>",
    "orderId": "<your order reference>",
    "type": "exactOut",
    "provider": "rozo",
    "display": { "title": "TRON USDT to Base USDC", "currency": "USD" },
    "source": { "chainId": "8453", "tokenSymbol": "USDC" },
    "destination": {
        "chainId": "8453",
        "tokenSymbol": "USDC",
        "receiverAddress": "<your user Base address>",
        "amount": "100.00"
    }
}'
```

### 3. Get the TRON payment option

Send the same `orderId` as `merchantOrderId` while the order is still unpaid. Receiver, net amount and partner fee are taken from the order.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/tron-ton-alpha' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "merchantOrderId": "<your order reference>",
    "network": "tron",
    "token": "USDT"
}'
```

The response carries the same payment fields as the Stellar route (`receivingAddress`, `expectedAmount`, `expectedAmountAtomic`, `expiresAt`, `netOutUsdc`, `rozoFeeUsdt`, `partnerFeeUsdt`, `totalFeeUsdt`, `allocationIncrementUsdt`, `reused`), plus:

| Field | Value |
| --- | --- |
| `route` | `tron_usdt_to_base_usdc` |
| `baseRoute` | `true` |
| `fulfilmentMode` | `base_payout` |
| `destination` | `{ "chainId": "8453", "asset": "USDC", "address": "<receiver, lower case>" }` |

Before you show the payment to the payer, check that `route`, `baseRoute`, `fulfilmentMode` and `destination.chainId` have these values, that `destination.address` equals your receiver (compare in lower case), and that `netOutUsdc` equals the net amount you asked for.

Calling the same request again for the same order returns the same option with `"reused": true`. To change the receiver or amount, create a new order.

## Paying, status and webhooks

Paying, the status lifecycle and webhooks are the same as on the Stellar route. See [Paying](usdt-tron-to-usdc-stellar.md#paying) and [Status lifecycle and webhook](usdt-tron-to-usdc-stellar.md#status-lifecycle-and-webhook). On this route the payout transaction is a Base transaction hash.

## Errors and recovery

Quote reasons appear in `paymentOption.availabilityReason` with HTTP 200. Create errors from `/tron-ton-alpha` are returned as `{"error": "<code>"}`, some with a `detail`, with the HTTP status shown. Match on the code, not on message text.

| Situation | What you see | What to do |
| --- | --- | --- |
| Route not available | Quote: a non-200 response, or no `paymentOption.route`; create `403` `base_route_disabled` or `base_route_not_allowed` | Hide the Base option, or offer USDC on Stellar |
| App not eligible | Quote `app_not_eligible`; create `403` `app_not_allowed` | Contact Rozo |
| Amount too small | Quote `below_minimum` | Raise the amount so the rounded gross is at least the minimum |
| Above the per-order maximum | Quote `above_order_max`; create `422` `order_cap_exceeded` | Lower the amount or split into several orders |
| Shared daily capacity used up | Quote `daily_capacity_exhausted`; create `422` `daily_budget_exhausted` | Try again later, or after 00:00 UTC. This is platform-wide, not your quota |
| Base payout capacity used up | Quote `payout_capacity_insufficient`; create `422` `base_capacity_insufficient` | Try a smaller amount, try later, or offer USDC on Stellar. No address was issued |
| Too many open payment options for your app | Quote `app_active_limit`; create `429` `app_active_limit` with `limit` | Wait for open options to be paid or expire, then retry |
| No TRON address free | Create `503` `pool_exhausted` with `"hideOption": true` | Hide the TRON option for now |
| Receiver malformed, zero, bad checksum, or a memo was sent | Quote `recipient_invalid`; create `403` `destination_not_approved` | Fix the address and drop the memo |
| Receiver refused (for example the USDC token contract) | Quote `recipient_not_allowed`; create `403` `destination_not_approved` | Use another receiving address |
| Order is not to USDC on Base | Create `403` `destination_not_approved` | Create a new `exactOut` order to Base USDC |
| Order does not fit this route | Create `409` `base_unsupported_order` | The order must be a Rozo `exactOut` order to Base USDC with at most 6 decimals |
| Order already paid or closed | Create `409` `order_not_open` | Read the order status; do not pay again |
| Same order reference with different values, or `baseServiceUsd` not equal to the net amount | Create `409` `order_conflict` | Use a new order reference, or send `baseServiceUsd` equal to the order's net amount |
| Fee route too costly right now | Quote `fee_refused`; create `409` `no_executable_route` | Retry later |
| Payment window closed before payment | Create `410` `order_expired` | Create a new order. Do not pay the old address |
| A check could not run | Quote `503` `serviceUnavailable`; create `503` (for example `base_capacity_unavailable` or `base_route_unavailable`) | Retry later |
| Paid after the window, underpaid, overpaid, or paid twice | Not paid out automatically | Funds are held and reviewed by Rozo. [Contact us](../../../contact/contact-us/README.md) with the TRON transaction hash |

## In the Rozo Bridge app

{% hint style="info" %}
**Beta.** This route is available on [intents.rozo.ai/bridge](https://intents.rozo.ai/bridge). No integration work, API key or TRON wallet connection is needed.
{% endhint %}

1. Choose **USDT · TRON · Beta** as the source, then **USDC · Base** as the destination. While this route is offered, the destination for this source can be USDC on Stellar or USDC on Base.
2. Enter either the USDT to pay or the USDC to receive; the other amount is calculated. A quote is shown before you enter the receiving address; until then it is an estimate.
3. Enter the Base receiving address. There is no memo for a Base destination.
4. Review the quote, generate the payment and pay the TRON address and exact amount shown, as on the Stellar route.

The page never shows a Base deposit address to pay. Pay only the TRON address and amount it displays.
