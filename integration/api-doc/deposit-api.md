# Wallet Deposit API

Generate a unique EVM deposit address for a Stellar address. Anything your user sends to that address (USDC or USDT on a supported EVM chain) is paid out as USDC to the Stellar address.

## Supported Pay In Tokens

| Chain    | USDC | USDT |
| -------- | ---- | ---- |
| Ethereum | Yes  | Yes  |
| Arbitrum | Yes  | Yes  |
| Base     | Yes  | No   |
| BSC      | Yes  | Yes  |
| Polygon  | Yes  | Yes  |

For token addresses and decimals, see [Supported Tokens and Chains](supported-tokens-and-chains.md). For Solana USDC, see [Solana USDC deposits](#solana-usdc-deposits) below.

## API Host

```
https://intentapiv4.rozo.ai/functions/v1
```

## 1. Get an API key

1. Register a **wallet account** at [https://partners.rozo.ai](https://partners.rozo.ai) and verify your email. Your app id looks like `wallet_<your-slug>`.
2. In the dashboard, create an API key.
3. Send the key in the `X-API-Key` header on every create call.

Merchant accounts (`merchant_*`) are not supported by the Deposit API yet.

## 2. Create a deposit address

**Endpoint:** `POST /deposit-api/create`

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/deposit-api/create' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: <your API key>' \
  --data-raw '{
    "stellar_address": "GATR4H...3TQL"
  }'
```

| Parameter         | Type   | Required | Description |
| ----------------- | ------ | -------- | ----------- |
| `stellar_address` | string | Yes      | Stellar address that receives the USDC. G accounts and C smart contract accounts are supported. The account must hold a USDC trustline. |
| `app_id`          | string | No       | Your app id. If you send it, it must equal the app id of your API key exactly. |

### Response

`201 Created` means a new address was generated. `200 OK` means this `stellar_address` already has an address for your app, and the same one is returned. One `stellar_address` + `app_id` pair always maps to the same deposit address, so you can call create every time you show the deposit screen.

```json
{
  "id": "aef5f696-0a80-4324-a8e0-e298796f2b79",
  "stellar_address": "GATR4H...3TQL",
  "evm_address": "0x4019c9D04D509A148a3602ECF397568ea7Dc759e",
  "app_id": "wallet_testwallet001",
  "is_paid": false,
  "first_paid_at": null,
  "metadata": { "forwarder_version": "v1", "...": "..." },
  "created_at": "2026-10-25T13:58:00.000Z"
}
```

Show `evm_address` to your user. It is the same address on every supported EVM chain.

## 3. Fees

| Rule | Fee |
| ---- | --- |
| Default (USDC) | 0.1% of the amount received, minimum $0.01 |
| USDT | 0.2% of the amount received, minimum $0.01 |
| Paid from Ethereum | minimum $0.10 (applies when higher than the percentage fee) |

Amount paid out = amount received minus fee. Example: 0.1 USDC on Base pays out 0.09 USDC (fee $0.01). 100 USDC on Base pays out 99.90 USDC. 100 USDT on BNB Chain pays out 99.80 USDC (fee $0.20).

## 4. Minimum deposit

There is no fixed minimum, but a deposit that is not larger than its fee is not paid out (for example 0.01 USDC on Base, or under $0.10 from Ethereum).

## 5. Check deposit status

**By Stellar address** (latest 5 deposits):

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/deposit-api/deposits?destination_receiver_address=GATR4H...3TQL'
```

**By deposit address id** (paginated, optional `limit`, `offset`, `status`):

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/deposit-api/<id>/deposits?limit=20'
```

Example deposit:

```json
{
  "id": "5e9cf259-0032-4aed-b7c5-8aad19e29311",
  "app_id": "wallet_testwallet001",
  "status": "payment_payout_completed",
  "amount": 0.1,
  "fee": 0.01,
  "amount_out": 0.09,
  "source_tx_hash": "0x427f7e01bf7625f2661ed7ff2a7446adab61d05103ecb5dab94d4094dda5f396",
  "destination_tx_hash": "f74c4b0832046395a4d03e25692ad258ecaf9165ada22e74b57efce9fe0ed763"
}
```

| `status` | Meaning |
| -------- | ------- |
| `payment_payin_completed` | Funds received on the EVM address |
| `payment_payout_started` | USDC payout to Stellar is being sent |
| `payment_payout_completed` | USDC arrived on Stellar, see `destination_tx_hash` |

## 6. Errors

| HTTP | `error.code` | When |
| ---- | ------------ | ---- |
| 400 | `app_id_not_enabled` | No `X-API-Key` header. Register at partners.rozo.ai and send your key. |
| 400 | `invalid_api_key` | The key is invalid, revoked or expired. |
| 403 | `app_type_not_supported` | The key belongs to a merchant account. Only wallet accounts are supported. |
| 403 | `app_id_mismatch` | Body `app_id` is different from the key's app id. |
| 403 | `email_not_verified` | Verify your account email first. |
| 403 | `account_inactive` | Your developer account is disabled. |
| 400 | `Invalid Stellar address format` | `stellar_address` is not a 56 character G or C address. |

## 7. Solana USDC deposits

Solana uses the Payment API instead of a fixed address. Create an `anyAmount` order per deposit. The response gives a Solana address to pay; the amount is priced when the payment arrives.

```bash
curl -X POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
  --header 'Content-Type: application/json' \
  --header 'X-API-Key: <your API key>' \
  --data-raw '{
    "appId": "wallet_<your-slug>",
    "orderId": "deposit-123",
    "type": "anyAmount",
    "display": { "title": "Deposit", "currency": "USD" },
    "source": { "chainId": "900", "tokenSymbol": "USDC" },
    "destination": {
      "chainId": "1500",
      "tokenSymbol": "USDC",
      "receiverAddress": "GATR4H...3TQL"
    }
  }'
```

Send USDC on Solana to `source.receiverAddress` from the response. Track it with `GET /payment-api/payments/<id>`. After payment, a completed order looks like this (trimmed):

```json
{
  "type": "anyAmount",
  "status": "payment_payout_completed",
  "source": { "chainId": "900", "tokenSymbol": "USDC", "receiverAddress": "BYM1JG...fduB", "amountReceived": 0.5, "fee": 0.01 },
  "destination": { "chainId": "1500", "tokenSymbol": "USDC", "amount": 0.49, "txHash": "5f562a...73cf" }
}
```

Fees are the same as above (0.1%, minimum $0.01).
