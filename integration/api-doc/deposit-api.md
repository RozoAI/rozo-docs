# Wallet Deposit API

Generate a unique deposit address to receive funds on the **Stellar network**.


## Supported Pay In Tokens

Users can deposit from any of the following tokens and chains:

| Chain    | USDC | USDT |
| -------- | ---- | ---- |
| Ethereum | Yes  | Yes  |
| Arbitrum | Yes  | Yes  |
| Base     | Yes  | —    |
| BSC      | Yes  | Yes  |
| Polygon  | Yes  | Yes  |

For full token addresses and decimals, see [Supported Tokens and Chains](supported-tokens-and-chains.md).
More chains and tokens coming soon, e.g. USDT on Tron, USDC / USDT on Solana.

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
    "stellar_address": "CB63RSHEF3BLDANXM7V2PLE5UXNWVHC75B7RYMJ24YKWA444ZGWQPGBM",
    "app_id": "rozoTest"
  }'
```

### Parameters

| Parameter         | Type   | Required | Description                                              |
| ----------------- | ------ | -------- | -------------------------------------------------------- |
| `stellar_address` | string | Yes      | Your Stellar address that will receive the deposited funds (G wallet or C wallet Smart contract accounts are supported) |
| `app_id`          | string | Yes      | Your application identifier (join our Discord to get one) |

### Response

```json
{
  "deposit_address": "0x1234567890abcdef1234567890abcdef12345678",
  "status": "created"
}
```

> **Note:** Please contact with ROZO team to get the app_id.
