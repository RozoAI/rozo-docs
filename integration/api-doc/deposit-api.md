# Wallet Deposit API

Generate a unique deposit address to receive funds on the **Stellar network**.

## Supported Network

| Chain ID | Chain Name |
| -------- | ---------- |
| `1500`   | Stellar    |

## Supported Pay In Tokens

Users can deposit from any of the following tokens and chains:

| Chain    | USDC | USDT |
| -------- | ---- | ---- |
| Ethereum | Yes  | Yes  |
| Arbitrum | Yes  | Yes  |
| Base     | Yes  | —    |
| BSC      | Yes  | Yes  |
| Polygon  | Yes  | Yes  |
| Solana   | Yes  | Yes  |
| Stellar  | Yes  | —    |

## Supported Deposit Tokens

Funds are deposited to your Stellar address in the following tokens:

| Token | Supported |
| ----- | --------- |
| USDC  | Yes       |
| USDT  | Yes       |

For full token addresses and decimals, see [Supported Tokens and Chains](supported-tokens-and-chains.md).

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
| `stellar_address` | string | Yes      | Your Stellar address that will receive the deposited funds |
| `app_id`          | string | Yes      | Your application identifier (join our Discord to get one) |

### Response

```json
{
  "deposit_address": "GDFLZTLVMLR3OVO4VSODYB7SGVIOI2AS652WODBCGBUQAMXXXXXXXXXX",
  "status": "created"
}
```

> **Note:** The response schema above is illustrative. Refer to the [API Doc (POSTMAN)](https://apidoc.rozo.ai/) for the full response format.
