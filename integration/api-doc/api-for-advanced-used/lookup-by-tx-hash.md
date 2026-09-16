# Look Up a Payment by Tx Hash

Find an order when all you have is an on-chain transaction hash: the buyer's pay-in transaction, or the payout transaction that landed in the recipient's wallet. Useful for reconciliation and support ("I sent this tx, where is my order?").

**API Host**: `https://intentapiv4.rozo.ai/functions/v1`

**Endpoint:** `GET /payment-api/payments/check`

No API key is required. The response is the same Payment object as `GET /payment-api/payments/{paymentId}`.

## Parameters

Send exactly one of the hash parameters, or the address + memo pair.

| Parameter | Matches | Search window |
| --- | --- | --- |
| `sourceTxHash` | the **pay-in** transaction (from the payer) | last 90 days |
| `destinationTxHash` | the **payout** transaction (to the recipient) | last 90 days |
| `txHash` | either side (legacy; prefer the two above) | last 3 days |
| `receiverAddress` + `receiverMemo` | the deposit address and memo the order was created with | last 7 days |

Sending more than one hash parameter returns `400 invalidRequest`.

## Request

```bash
# by the pay-in transaction
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/check?sourceTxHash=06ada9988b1be34654bcdc9057e837cf35a4b888f02682a3a4730a0bde52d322'

# by the payout transaction
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/check?destinationTxHash=1d9028ab1a4355d46668b13791c8c1ba015d8cef4daf248c0039c2671dd4842b'
```

## Response

```json
{
  "id": "54f7039b-e80e-4a9d-825a-b5d226d3025a",
  "status": "payment_payout_completed",
  "source": {
    "chainId": "1500",
    "tokenSymbol": "USDC",
    "amount": "31.00",
    "txHash": "06ada9988b1be34654bcdc9057e837cf35a4b888f02682a3a4730a0bde52d322"
  },
  "destination": {
    "chainId": "1500",
    "tokenSymbol": "USDC",
    "amount": "30.8925",
    "txHash": "1d9028ab1a4355d46668b13791c8c1ba015d8cef4daf248c0039c2671dd4842b"
  }
}
```

Fields are abbreviated; the full object is documented under `GET /payments/{paymentId}`.

## Not found

```json
{ "error": { "code": "paymentNotFound", "message": "No payment found in the last 90 days" } }
```

Hashes are matched exactly as stored. EVM hashes are `0x`-prefixed; Stellar hashes are 64 hex characters without a prefix.
