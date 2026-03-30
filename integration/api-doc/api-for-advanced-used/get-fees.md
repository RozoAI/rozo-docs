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
