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
| `AMOUNT_TOO_SMALL` | Below the route's minimum; the response includes `data.minimumSourceAmount`. |
| `NEGATIVE_ROUTE_ECONOMICS` | The amount is too small to cover the network cost of this route; send a larger amount. |

## Error responses

Errors from this endpoint use `error.code` and `error.message`, plus a `requestId` you can share with support. Route-specific details, when present, are in the top-level `data` object: read `data.errorCode`, not `error.details.errorCode`. Some errors have no `data` object.

The examples below are generated from the API's response-building code using illustrative inputs. They show the full JSON shape, not captured customer responses. Amounts are examples, not fixed route minimums; the placeholder `requestId` is replaced by a generated ID in real responses. These examples are not an exhaustive error catalog.

All five examples return **HTTP 400 Bad Request** with **Content-Type: application/json**.

### Unsupported NEAR route

For example, requesting `provider: "near"` for Base USDC to HyperEVM USDC is rejected by the provider route check.

```json
{
  "error": {
    "code": "invalidRequest",
    "message": "This route is not supported by provider \"near\". Retry with provider \"rozo\" (or omit provider to use auto)."
  },
  "requestId": "00000000-0000-4000-8000-000000000001",
  "data": {
    "errorCode": "ROUTE_NOT_SUPPORTED_BY_PROVIDER",
    "provider": "near",
    "reason": "destination_not_settleable",
    "sourceChainId": "8453",
    "sourceTokenSymbol": "USDC",
    "destinationChainId": "999",
    "destinationTokenSymbol": "USDC",
    "supportedProviders": [
      "rozo"
    ]
  }
}
```

Check the supported routes. If `data.supportedProviders` includes `"rozo"`, retry with `provider: "rozo"` or omit `provider` to use automatic routing. Otherwise, select another supported route. Additional request validation still applies.

### Amount below the route minimum

This example requests 3 source tokens when the provider quote requires at least 5.

```json
{
  "error": {
    "code": "amountTooLow",
    "message": "Amount is below the minimum for this route. Minimum pay-in is 5 (you requested 3)."
  },
  "requestId": "00000000-0000-4000-8000-000000000001",
  "data": {
    "errorCode": "AMOUNT_TOO_SMALL",
    "provider": "near",
    "minimumSourceAmount": 5,
    "requestedSourceAmount": 3
  }
}
```

`data.minimumSourceAmount` and `data.requestedSourceAmount` are numbers in source-token units, not smallest units. Increase the source amount to at least the returned minimum and request a fresh dry-run quote; other route checks may still reject it.

### Amount cannot cover the route cost

The quote cannot cover the requested destination amount after route costs.

```json
{
  "error": {
    "code": "amountTooLow",
    "message": "Amount is too low to cover the network cost of this route (short by 0.024365). Please send a larger amount."
  },
  "requestId": "00000000-0000-4000-8000-000000000001",
  "data": {
    "errorCode": "NEGATIVE_ROUTE_ECONOMICS",
    "provider": "near",
    "deliverable": 19.915635,
    "expectedDeliverable": 19.975562,
    "promised": 19.94,
    "shortfall": 0.024365
  }
}
```

Increase the amount and request a fresh quote. `deliverable`, `expectedDeliverable`, `promised`, and `shortfall` are numbers in destination-token units. `deliverable` is the guaranteed quote floor when available, while `expectedDeliverable` is the expected output. A numeric or null `withdrawFee` may also appear if the provider supplies that field. These values vary with the quote.

### NEAR does not support anyAmount

Setting `provider: "near"` together with `type: "anyAmount"` returns this error.

```json
{
  "error": {
    "code": "invalidRequest",
    "message": "provider \"near\" does not support type \"anyAmount\". Use provider \"rozo\" or \"auto\"."
  },
  "requestId": "00000000-0000-4000-8000-000000000001",
  "data": {
    "errorCode": "PROVIDER_TYPE_NOT_SUPPORTED",
    "provider": "near",
    "type": "anyAmount"
  }
}
```

For `anyAmount`, use `provider: "rozo"` or `"auto"`. To request a NEAR quote, use a supported fixed-amount type (`exactIn` or `exactOut`) and provide its required fields.

### Invalid request body

A malformed JSON body or a body that is not a JSON object returns this error.

```json
{
  "error": {
    "code": "invalidRequest",
    "message": "Body must be valid JSON object"
  },
  "requestId": "00000000-0000-4000-8000-000000000001"
}
```

Send a valid JSON object with `Content-Type: application/json`. This example has no `data` object, so clients must handle that field as optional.

For client-side handling, check the HTTP status first, then `data.errorCode` when available, otherwise `error.code`. Do not match the full `error.message` string: it can contain dynamic amounts or provider guidance. Correct these request errors before retrying the same request.
