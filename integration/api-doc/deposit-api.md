# Deposit API

Create a deposit address to receive USDC on Stellar.

## API Host

```
https://intentapiv4.rozo.ai/functions/v1
```

## Create Deposit

**Endpoint:** `POST /deposit-api/create`

### Request

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/deposit-api/create' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "stellar_address": "CB63RSHEF3BLDANXM7V2PLE5UXNWVHC75B7RYMJ24YKWA6SNZGWQPGBM",
    "app_id": "rozoTest"
  }'
```

### Parameters

| Parameter         | Type   | Required | Description                                              |
| ----------------- | ------ | -------- | -------------------------------------------------------- |
| `stellar_address` | string | Yes      | Your Stellar address that will receive the deposited USDC |
| `app_id`          | string | Yes      | Your application identifier (join our Discord to get one) |

### Response

```json
{
  "deposit_address": "GDFLZTLVMLR3OVO4VSODYB7SGVIOI2AS652WODBCGBUQAMXXXXXXXXXX",
  "status": "created"
}
```

> **Note:** The response schema above is illustrative. Refer to the [API Doc (POSTMAN)](https://apidoc.rozo.ai/) for the full response format.
