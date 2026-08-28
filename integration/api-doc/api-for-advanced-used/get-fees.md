# Get Fees

Use the `dryrun` parameter to preview the fee calculation without creating an actual payment.

**API Host**: `https://intentapiv4.rozo.ai/functions/v1`

**Endpoint:** `POST /payment-api/payments?dryrun=true`

## Request

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments?dryrun=true' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "yourAppId",
    "type": "anyAmount",
    "source": {
        "chainId": "8453",
        "tokenSymbol": "USDC",
        "amount": "100.00"
    },
    "destination": {
        "chainId": "1500",
        "receiverAddress": "GDFLZTLVMLR3OVO4VSODYB7SGVIOI2AS652WODBCGBUQAMXXXXXXXXXX",
        "tokenSymbol": "USDC"
    }
}'
```

## Response

```json
{
  "fee": "0.10",
  "source": {
    "chainId": "8453",
    "tokenSymbol": "USDC",
    "amount": "100.00"
  },
  "destination": {
    "chainId": "1500",
    "tokenSymbol": "USDC",
    "amount": "99.90"
  }
}
```

> **Note**: The `dryrun=true` parameter returns fee details without creating a payment record.

## Which rail charged the fee

Dry-run and create responses also carry a `feeInfo` block that names the routing provider the fee belongs to, so you always know whether a quote is priced on Rozo's own rails or on NEAR Intents:

```json
"provider": "near",
"feeInfo": {
  "feePercentage": "0.3%",
  "minimumFee": "$0.01",
  "provider": "near",
  "feeTier": "near-routing"
}
```

| Provider | Rate |
| --- | --- |
| `rozo` | your app tier (public default 0.1%, minimum $0.01) |
| `near` | flat 0.3% (minimum $0.01); per-destination minimums still apply (e.g. Solana $0.20, Ethereum $0.10, USDT on Tron $1) |

`feePercentage` is the **effective** rate: when a minimum fee applies to a small order it shows the real percentage, not the nominal one.

## Rate card without a dry run

`GET /payment-api/payments/supported` returns the schedule-level rate card for both rails together with the supported chain/token matrix:

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/supported'
```

```json
{
  "fees": {
    "rozo": { "feePercentage": "0.1%", "minimumFee": "$0.01" },
    "near": { "feePercentage": "0.3%", "minimumFee": "$0.01", "feeTier": "near-routing" }
  },
  "data": [ ... ]
}
```

These numbers are indicative. The binding fee for a specific order is always the dry-run `feeInfo`.

## Errors specific to NEAR-routed quotes

| Error code | Meaning |
| --- | --- |
| `ROUTE_NOT_SUPPORTED_BY_PROVIDER` | You asked for `provider: "near"` on a route it cannot serve. |
| `AMOUNT_TOO_SMALL` | Below the route's minimum; the response includes `minimumSourceAmount`. |
| `NEGATIVE_ROUTE_ECONOMICS` | The amount is too small to cover the network cost of this route; send a larger amount. |
