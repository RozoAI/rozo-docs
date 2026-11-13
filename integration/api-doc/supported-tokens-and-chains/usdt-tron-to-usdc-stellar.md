---
hidden: true
---

# TRON USDT pay-in, settle in Stellar USDC (Beta)

{% hint style="info" %}
**Beta.** Any wallet or merchant with a valid Rozo API key can use this route. There is no invite list. Fees, limits and timing may change while the beta runs. Settlement times will be published after measured runs; until then this page makes no timing promise.
{% endhint %}

The payer sends USDT on TRON to a payment address issued for one order. Rozo confirms the transfer on chain and pays USDC on Stellar to the receiving account and memo set on your order, the same way as on every other route.

| Side | Chain | Chain ID | Token | Asset | Decimals |
| --- | --- | --- | --- | --- | --- |
| Pay in | TRON | `728126428` or `tron` | USDT (TRC20) | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | 6 |
| Pay out | Stellar | `1500` or `stellar` | USDC | `USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN` | 7 |

## Who can use it, and what is excluded

* **Who:** any app (wallet or merchant) with a valid `X-API-Key`. Anonymous orders are not accepted. See [Merchant API Keys](../merchant-api-keys.md).
* **Direction:** one way only. USDT on TRON in, USDC on Stellar out.
* **Not offered on this route:** TRX (the TRON native coin), USDT payouts, TRON as a payout chain, Stellar to TRON, and any destination other than USDC on Stellar.
* This route is not a row in the `data` list of `GET /payments/supported`. When it is enabled, it is described in the optional `paymentOptions` list of the same response. See [Supported Tokens and Chains](../supported-tokens-and-chains.md#payment-options).

## Before you start

* The Stellar receiving account must already exist and hold an authorized **USDC trustline** to the issuer above. Otherwise no payment address is issued (`422` `trustline_missing`, or `"availabilityReason": "recipient_no_trustline"` on a quote). The receiver does not need any other trustline.
* Keep your API key on your server. Never ship it to a browser or mobile app.

## Amounts: gross and net

This route uses `exactOut` orders:

* **Net** (`destination.amount`): the USDC the receiving account gets on Stellar. This is what you enter.
* **Gross** (`source.amount` on a quote, `expectedAmount` on the payment option): the USDT the payer sends on TRON. Gross = net + Rozo service fee + partner fee (if any), plus a tiny unique increment explained below.

All money values are decimal strings. Do your arithmetic in integer base units (6 decimals), never in floating point.

## Fees

* **Rozo service fee:** a dynamic rate with a **0.20% floor**, and a **0.50 USD minimum** per order. The rate can be above the floor when routing costs are higher. The 0.50 USD minimum replaces the percentage fee on small orders; it is not added on top of it.
* **Partner fee:** charged separately if your app has one configured. See [Partner Fee](../api-for-advanced-used/partner-fee.md).
* **Network fee:** the payer pays the TRON network fee (Energy / TRX) from their own wallet. It is not part of the Rozo fee.
* Rozo calculates every fee on the server. Show the values from the quote or payment option; do not compute fees in your client.

The service fee is charged on the gross amount: at the floor rate, fee = net × 0.002 / 0.998, rounded up to the next base unit, and never less than 0.50.

**Worked examples.** These are illustrations at the 0.20% floor with no partner fee. They are not a price commitment. Always read the real quote.

| Net USDC you ask for | Rozo fee | Gross USDT to pay (before the unique increment) | Note |
| --- | --- | --- | --- |
| 0.50 | 0.50 | 1.00 | Smallest payable order: the minimum fee makes up half |
| 100.00 | 0.50 | 100.50 | Minimum fee applies (0.20% would be about 0.20) |
| 1,000.00 | 2.004009 | 1,002.004009 | Percentage fee applies |
| 2,995.00 | 6.002005 | 3,001.002005 | Refused: gross is above the per-order maximum |

The minimum fee applies to every order up to about 249.50 USDC net at the floor rate.

**Unique increment.** To match each TRON transfer to exactly one order, Rozo may add a very small amount to the gross (shown as `allocationIncrementUsdt` on the payment option). The final amount to send is `expectedAmount`, which can be slightly higher than the quote.

## Limits

* **Minimum:** the gross amount to pay must be at least 1 USDT. Because of the 0.50 USD minimum fee, the smallest net payout is 0.50 USDC.
* **Per-order maximum:** currently 3,000 USD, checked on the **gross** amount (fees included). A net amount that is below the maximum but whose gross is above it is refused.
* **Shared daily capacity:** TRON pay-ins have a daily capacity per UTC day that is **shared by all apps on the platform**. It is not a per-user or per-app allowance, and Rozo does not publish it as a guarantee: a new order can be refused because the platform-wide capacity is used up, even if your app has not paid anything that day. It resets at 00:00 UTC.
* **Inventory:** each order reserves Stellar USDC for its payout when the payment option is created. If none can be reserved, no payment address is issued.

The values above can change during the beta. The quote response is authoritative: read `paymentOption.limits.minGrossUsd` and `paymentOption.limits.maxGrossUsd`, and `paymentOption.available` with `availabilityReason`, instead of hardcoding numbers. For higher limits, [contact us](../../../contact/contact-us/README.md).

## Lower network cost for the payer

Rozo tries to use TRON receiving addresses that already hold a small USDT balance. A USDT transfer to such an address usually consumes less Energy than a transfer to an address with zero USDT, so a payer sending directly from a wallet may spend less TRX. The actual network fee is whatever the payer's wallet shows. An exchange sets its own withdrawal fee, which this does not change.

## How to integrate

The flow is: quote (optional, no side effects), then two calls to create the payment option.

{% hint style="warning" %}
**Draft.** The quote and `paymentOptions` fields below follow the API contract for this release and may change before the release is final.
{% endhint %}

### 1. Get a quote (optional)

`POST /payment-api/payments?dryrun=true` with a TRON USDT source. The quote does not create an order, does not reserve inventory or capacity, and does not issue an address. It is accepted only for `"provider": "rozo"`, `"type": "exactOut"`, TRON USDT to Stellar USDC, with a valid API key.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments?dryrun=true' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "exactOut",
    "provider": "rozo",
    "source": { "chainId": "728126428", "tokenSymbol": "USDT" },
    "destination": {
        "chainId": "1500",
        "tokenSymbol": "USDC",
        "amount": "100.00",
        "receiverAddress": "<your user Stellar account>",
        "receiverMemo": "<your user memo, omit if none>"
    }
}'
```

Example response (illustrative values, no partner fee):

```json
{
  "status": "dryrun",
  "id": null,
  "source": { "chainId": "728126428", "tokenSymbol": "USDT", "amount": "100.50", "fee": "0.50" },
  "destination": { "chainId": "1500", "tokenSymbol": "USDC", "amount": "100.00" },
  "feeInfo": { "provider": "rozo" },
  "paymentOption": {
    "route": "tron_usdt_to_stellar_usdc",
    "orderMode": "exactOut",
    "creationMode": "order_option",
    "beta": true,
    "priceLocked": false,
    "amountIsEstimate": true,
    "available": true,
    "availabilityReason": null,
    "limits": { "minGrossUsd": "1.00", "maxGrossUsd": "3000.00" },
    "fees": { "rozoFeeUsd": "0.50", "rozoFeeBps": 20, "minimumFeeApplied": true, "partnerFeeUsd": "0.00" },
    "paymentWindowMinutes": 60
  }
}
```

| Field | Meaning |
| --- | --- |
| `source.amount` | Estimated gross USDT to pay |
| `destination.amount` | Net USDC the receiver gets |
| `paymentOption.priceLocked` | Always `false`: a quote does not lock the fee or reserve anything |
| `paymentOption.amountIsEstimate` | Always `true`: the final `expectedAmount` can be slightly higher (rounding and the unique increment) |
| `paymentOption.available` | Whether a payment option can be created right now |
| `paymentOption.availabilityReason` | Why not, when `available` is `false` (see [Errors and recovery](#errors-and-recovery)) |
| `paymentOption.limits` | Current minimum and maximum gross, in USD |
| `paymentOption.fees` | Rozo fee amount and rate in basis points, whether the 0.50 minimum applied, and the partner fee |
| `paymentOption.paymentWindowMinutes` | How long a created payment option stays payable |

`available: true` is a snapshot. Capacity and inventory are checked again when you create the payment option, and can be gone by then.

### 2. Create the order

Create an `exactOut` order that pays USDC on Stellar (`1500`), with `"provider": "rozo"` set explicitly. `orderId` is your own unique reference. `destination.amount` is the net USDC amount, with at most 6 decimals. Set `receiverAddress` and `receiverMemo` from your own user; omit `receiverMemo` if the account needs no memo.

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
    "display": { "title": "TRON USDT to Stellar USDC", "currency": "USD" },
    "source": { "chainId": "8453", "tokenSymbol": "USDC" },
    "destination": {
        "chainId": "1500",
        "tokenSymbol": "USDC",
        "receiverAddress": "<your user Stellar account>",
        "receiverMemo": "<your user memo, omit if none>",
        "amount": "100.00"
    }
}'
```

### 3. Get the TRON payment option

Send the same `orderId` as `merchantOrderId`. `baseServiceUsd` must equal the net USDC amount of the order (`destination.amount`), not the gross. `existingAppFeeUsd` is not needed: Rozo calculates the fee on the server.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/tron-ton-alpha' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "merchantOrderId": "<your order reference>",
    "baseServiceUsd": 100,
    "network": "tron",
    "token": "USDT"
}'
```

Example response (illustrative values, no partner fee; some fields omitted):

```json
{
  "orderId": "<your order reference>",
  "reused": false,
  "chainId": "728126428",
  "network": "tron",
  "tokenSymbol": "USDT",
  "tokenIdentity": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
  "tokenDecimals": 6,
  "receivingAddress": "T...",
  "expectedAmount": "100.500013",
  "expectedAmountAtomic": "100500013",
  "grossUsd": "100.500013",
  "expiresAt": "2026-01-01T01:00:00Z",
  "poolAddress": true,
  "inventoryBeta": true,
  "netOutUsdc": "100.000000",
  "rozoFeeUsdt": "0.500000",
  "partnerFeeUsdt": "0.000000",
  "totalFeeUsdt": "0.500000",
  "allocationIncrementUsdt": "0.000013",
  "destination": {
    "chainId": "1500",
    "asset": "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
    "address": "<your user Stellar account>",
    "memoType": "text",
    "memo": "<your user memo>"
  }
}
```

| Field | Meaning |
| --- | --- |
| `receivingAddress` | TRON address issued for this order. Show it to the payer |
| `expectedAmount` | Exact USDT amount to send, fees and increment included |
| `expectedAmountAtomic` | The same amount in base units (6 decimals) |
| `expiresAt` | End of the payment window |
| `netOutUsdc` | Net USDC paid out on Stellar |
| `rozoFeeUsdt`, `partnerFeeUsdt`, `totalFeeUsdt` | Fee breakdown |
| `allocationIncrementUsdt` | The unique increment added to identify this payment |
| `reused` | `true` when the same request was sent again for this order |

Calling the same request again for the same order returns the same option with `"reused": true`. It does not issue a new address, amount or fee. Sending the same `merchantOrderId` with different values returns `409` `order_conflict`. To change the receiver, memo or amount, create a new order.

## Paying

* Send **exactly** `expectedAmount` of USDT (TRC20) on TRON to `receivingAddress` before `expiresAt`. When paying from an exchange, add the exchange's withdrawal fee on top so that the exact amount arrives.
* Show the address and the amount as two separate values the payer can copy. If you render a QR code, encode the address only, unless you have verified that the payer's wallet reads an amount from the code.
* Use the address from this order's response only. Do not copy an address from wallet history.
* The payment window is the time to pay, not a delivery time.

## Status lifecycle and webhook

```text
payment_unpaid → payment_payin_completed → payment_payout_started → payment_payout_completed
```

* A wallet showing the transfer as sent does not mean the order is paid. Rozo waits for the TRON confirmations its current policy requires before it marks the pay-in complete.
* After the transfer is confirmed, the order moves to `payment_payin_completed` and the USDC payout to Stellar starts.
* Treat the order as settled only at raw `status` `payment_payout_completed`, and reconcile the Stellar transaction and net amount.
* Webhooks: `payment_payin_completed` and `payment_payout_completed` are sent as for every other order. See [Webhook](../api-for-advanced-used/webhook.md).

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/order/<your appId>/<your order reference>' \
--header 'X-API-Key: <your api key>'
```

Or by payment id: `GET /payment-api/payments/{id}`. See [Reading order status](../merchant-api-keys.md#reading-order-status).

## Errors and recovery

| Situation | What you see | What to do |
| --- | --- | --- |
| Route switched off | Quote `"availabilityReason": "disabled"`; create `403` `alpha_disabled` | Hide the TRON option and offer another method |
| Amount too small | Quote `"availabilityReason": "below_minimum"` | Raise the amount so the gross is at least the minimum |
| Above the per-order maximum | Quote `"availabilityReason": "above_order_max"`; create `422` `order_cap_exceeded` | Lower the amount or split into several orders |
| Shared daily capacity used up | Quote `"availabilityReason": "daily_capacity_exhausted"`; create `422` `daily_budget_exhausted` | Try again later, or after 00:00 UTC, or offer another method. This is platform-wide, not your quota |
| No Stellar USDC inventory | Quote `"availabilityReason": "inventory_insufficient"`; create `422` `inventory_unavailable` | Try again later or offer another method. No address was issued |
| No TRON address free | Create `503` `pool_exhausted` with `"hideOption": true` | Hide the TRON option for now |
| Receiver has no USDC trustline, or does not exist | Quote `"availabilityReason": "recipient_no_trustline"` or `"recipient_invalid"`; create `422` `trustline_missing` | Ask the user to add the USDC trustline, then request again |
| Stellar check could not run | Create `503` `stellar_check_unavailable` | Retry later |
| Fee route too costly right now | Quote `"availabilityReason": "fee_refused"`; create `409` `no_executable_route` | Retry later |
| Same order reference, different values | Create `409` `order_conflict` | Use a new order reference |
| Order already paid or closed | Create `409` `order_not_open` | Read the order status; do not pay again |
| Order does not fit this route | Create `409` `beta_unsupported_order` | The order must be a Rozo `exactOut` order to Stellar USDC, at most 6 decimals, with `baseServiceUsd` equal to its net amount |
| Payment window closed before payment | Create `410` `order_expired`; order `payment_expired` | Create a new order. Do not pay the old address |
| Paid after the window, underpaid, or overpaid | Not paid out automatically | Funds are held and reviewed by Rozo. [Contact us](../../../contact/contact-us/README.md) with the TRON transaction hash |
| Paid twice, or paid the Base placeholder too | The second payment is held as a duplicate | [Contact us](../../../contact/contact-us/README.md) with both transaction hashes |
| Missing or invalid API key | `401` `unauthorized` | Check the key |

Quote reasons appear in `paymentOption.availabilityReason` with HTTP 200. Create errors are returned as `{"error": "<code>"}` with the HTTP status shown. Match on the code, not on message text.

## In the Rozo Bridge app

When this Beta is enabled in the app, [intents.rozo.ai/bridge](https://intents.rozo.ai/bridge) offers it without any integration work:

1. Choose **USDT · TRON · Beta** as the source. The destination is set to **USDC · Stellar** and cannot be changed for this source.
2. Enter the USDC amount to receive, the Stellar receiving account and an optional memo. The app checks the USDC trustline.
3. Review the quote: USDT to pay, net USDC, Rozo fee, partner fee and limits. Nothing is reserved yet.
4. Generate the payment: the app shows the TRON address as a QR code, with separate buttons to copy the address and the exact amount, and a countdown.
5. Pay from any TRON wallet or exchange. The page shows waiting for payment, confirming, paying out, and completed with the Stellar transaction. Refreshing the page resumes the same order.

No TRON wallet connection is needed.
