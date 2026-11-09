---
hidden: true
---

# USDT on TRON to USDC on Stellar (beta)

{% hint style="info" %}
**Open beta.** Any app with a Rozo API key can use this route. Fees and limits may change while the beta runs.
{% endhint %}

The payer sends USDT on TRON to a payment address issued for one order. Rozo confirms the transfer on chain and pays USDC on Stellar to the receiving account and memo set on your order, the same way as on every other route.

| Side | Chain | Chain ID | Token | Asset | Decimals |
| --- | --- | --- | --- | --- | --- |
| Pay in | TRON | `728126428` or `tron` | USDT (TRC20) | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | 6 |
| Pay out | Stellar | `1500` or `stellar` | USDC | `USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN` | 7 |

This route is not listed in `GET /payments/supported`. TRON is not a pay-out chain, and Stellar to TRON is not offered.

## Before you start

* You need an `X-API-Key` for your app. See [Merchant API Keys](../merchant-api-keys.md).
* The Stellar receiving account must already exist and hold an authorized USDC trustline to the issuer above. Otherwise the payment option is refused with `422` `trustline_missing` and no payment address is issued.

## Fees and limits

* Fee: a Rozo service fee at a dynamic rate with a 0.20% floor and a $0.50 minimum, plus your partner fee if configured (see [Partner Fee](../api-for-advanced-used/partner-fee.md)). Rozo calculates the fee on the server. The response shows the exact amount to send.
* Very small orders are mostly fee because of the $0.50 minimum. An order whose total to pay is below 1 USDT is not offered.
* Maximum: **3,000 USD** per order. An order above it returns `422` `order_cap_exceeded`.
* Daily limit: **10,000 USD** per UTC day on TRON, shared across all apps. Once it is used up, new orders return `422` `daily_budget_exhausted` until the next UTC day.
* Fees and limits may change during the beta. For higher limits, [contact us](../../../contact/contact-us/README.md).
* Each order reserves USDC on Stellar for the payout when the payment option is created. If Rozo cannot reserve it, the API returns `422` `inventory_unavailable` and no payment address is issued. Try again later or offer another payment method.

## How to integrate

The flow has two calls. First create the order on the Payment API. Then ask for the TRON payment option for that order.

### 1. Create the order

Create an `exactOut` order that pays USDC on Stellar (`1500`), with `"provider": "rozo"` set explicitly. `orderId` is your own unique reference. `destination.amount` is the USDC amount the receiving account gets (the net amount), with at most 6 decimals. Set `receiverAddress` and `receiverMemo` from your own user, as you do for any other Stellar payout; omit `receiverMemo` if the account needs no memo.

The Payment API does not accept TRON as a source, so set the source to USDC on Base (`8453`). The order gets its own Base deposit address as usual. **Do not show that address to the payer**: the payer pays only the TRON option from step 2.

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

### 2. Get the TRON payment option

Send the same `orderId` as `merchantOrderId`. `baseServiceUsd` must equal the net USDC amount of the order (`destination.amount`), not the amount including fees. `existingAppFeeUsd` is not needed: Rozo calculates the fee on the server.

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

Example response (values are illustrative, for an app with no partner fee):

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
  "expectedAmount": "100.50",
  "expectedAmountAtomic": "100500000",
  "grossUsd": "100.50",
  "expiresAt": "2026-01-01T01:00:00Z",
  "poolAddress": true,
  "notice": "Alpha: the payment is verified on chain and the top-up is delivered automatically. Each order has its own address. Do not copy an address from your wallet history."
}
```

| Field | Meaning |
| --- | --- |
| `receivingAddress` | TRON address issued for this order. Show it to the payer |
| `expectedAmount` | Exact USDT amount to send, fees included |
| `expectedAmountAtomic` | The same amount in base units (6 decimals) |
| `grossUsd` | USD value of `expectedAmount` |
| `expiresAt` | End of the 60-minute payment window |
| `reused` | `true` when the same request was sent again for this order |
| `tokenIdentity`, `tokenDecimals` | The TRC20 USDT contract and its decimals |

Calling the same request again for the same order returns the same option with `"reused": true`; it does not issue a new address or amount. Sending the same `merchantOrderId` with different values returns `409` `order_conflict`.

## Settlement conditions

* Send **exactly** `expectedAmount` of USDT on TRON to `receivingAddress` before `expiresAt`. The payment window is 60 minutes. When paying from an exchange, add the exchange's withdrawal fee on top so that the exact amount arrives.
* Use the address from this order's response only. Do not copy an address from wallet history.
* After the transfer is confirmed on chain, the order moves to `payment_payin_completed` and the USDC payout to Stellar starts.
* If the payer pays the order's Base deposit address instead, the order settles as a normal Base to Stellar order and any TRON payment is held as a duplicate for review.
* A transfer outside a small tolerance of `expectedAmount`, a transfer after the window has closed, or a second payment for an order that is already paid is not paid out automatically. The funds are held and reviewed by Rozo. [Contact us](../../../contact/contact-us/README.md) with the TRON transaction hash.
* After expiry the same request returns `410` `order_expired`. Create a new order.

## Check the status

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/order/<your appId>/<your order reference>' \
--header 'X-API-Key: <your api key>'
```

Or by payment id: `GET /payment-api/payments/{id}`. Treat the order as settled only at raw `status` `payment_payout_completed`, and reconcile the Stellar transaction. See [Reading order status](../merchant-api-keys.md#reading-order-status).

## Errors

| HTTP | `error` | Meaning |
| --- | --- | --- |
| `400` | `bad_request`, `unsupported_asset` | Missing fields, or a network or token other than TRON USDT |
| `401` | `unauthorized` | Missing, unknown or expired API key |
| `403` | `alpha_disabled` | The route is switched off |
| `403` | `app_not_allowed` | Your app cannot use this route |
| `403` | `destination_not_approved` | The order does not pay out USDC on Stellar. The destination must be USDC on Stellar |
| `409` | `order_conflict` | Same order reference sent with different values |
| `409` | `order_not_open` | The order is already paid or closed |
| `409` | `beta_unsupported_order` | The order does not exist, is not a Rozo `exactOut` order to Stellar USDC, has more than 6 decimals, carries a native coin, `USDT0` or exchange quote lock, or its amount does not match `baseServiceUsd` |
| `409` | `pilot_partner_fee_invalid`, `pilot_partner_fee_mismatch` | The partner fee is not in USDC or USDT, or does not match the configured rate on the net amount |
| `410` | `order_expired` | The payment window closed |
| `422` | `order_cap_exceeded` | Above the 3,000 USD per-order maximum |
| `422` | `inventory_unavailable` | No USDC can be reserved on Stellar now |
| `422` | `trustline_missing` | The receiving account does not exist or has no authorized USDC trustline |
| `422` | `daily_budget_exhausted` | The 10,000 USD TRON limit for the UTC day, shared across all apps, is used up |
| `503` | `pool_exhausted` (with `"hideOption": true`) | No TRON payment address is free right now. Hide the TRON option and offer another method |
| `503` | `stellar_check_unavailable` | The Stellar account check could not run. Try again later |
