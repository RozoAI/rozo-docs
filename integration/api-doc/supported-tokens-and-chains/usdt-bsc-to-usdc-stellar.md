---
hidden: true
---

# USDT on BNB Chain to USDC on Stellar

USDT on BNB Chain (BSC, chain `56`) can be paid in and settled as USDC on Stellar (`1500`). This is a standard route, available to every integration.

| | Value |
| --- | --- |
| Pay in | USDT on BSC, `0x55d398326f99059ff775485246999027b3197955`, **18 decimals** |
| Pay out | USDC on Stellar, `USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN`, 7 decimals |
| Fee on Rozo's rail | **0.2%** of the amount (any order with USDT on either side), minimum per your app tier (public default $0.01). Your partner fee, if any, is added on top |
| Fee on NEAR Intents | flat 0.3%, minimum $0.01 (see [Get Fees](../api-for-advanced-used/get-fees.md)) |
| Example | 100 USDT on BSC pays out 99.80 USDC on Stellar on Rozo's rail (fee $0.20) |
| Limits | Wallet Top-up: $0.02 to $10,000 per payment. Wallet Deposit: no fixed minimum; a deposit not larger than its fee is not paid out |

The Stellar receiving account must hold a USDC trustline. Always read the exact fee from the dry-run or created order.

## Ways to integrate

* **Payment API**: a fixed-amount order, shown below. See [API Quick Start](../api-quick-start.md).
* **Wallet Top-up**: an `anyAmount` order where the payer chooses the amount. See [Wallet Top-up](../api-for-advanced-used/wallet-topup.md).
* **Wallet Deposit API**: a fixed deposit address per user. See [Deposit API](../deposit-api.md). It does not send a memo, so do not use it for an exchange deposit account that needs one.

## Payment API example

Create an `exactOut` order. `destination.amount` is the USDC amount the receiving account gets; the response shows the USDT amount to send on BSC and the deposit address.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "<your appId>",
    "orderId": "<your order reference>",
    "type": "exactOut",
    "display": { "title": "BSC USDT to Stellar USDC", "currency": "USD" },
    "source": { "chainId": "56", "tokenSymbol": "USDT" },
    "destination": {
        "chainId": "1500",
        "tokenSymbol": "USDC",
        "receiverAddress": "<your user Stellar account>",
        "receiverMemo": "<your user memo, omit if none>",
        "amount": "100.00"
    }
}'
```

Add `?dryrun=true` to the URL first to get a quote without creating an order.

## Check the status

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/order/<your appId>/<your order reference>' \
--header 'X-API-Key: <your api key>'
```

Or by payment id: `GET /payment-api/payments/{id}`. Treat the order as settled only at raw `status` `payment_payout_completed`, and reconcile the Stellar transaction. See [Reading order status](../merchant-api-keys.md#reading-order-status).
