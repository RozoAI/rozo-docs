# API Quick Start

### Bridge 1 USDC from Base to Stellar

Base chain ID: `8453`

Stellar chain ID: `1500`

App ID (please join our discord)

API Host : https://intentapiv4.rozo.ai/functions/v1

<figure><img src="../../.gitbook/assets/Screenshot 2025-12-02 at 10.38.32 AM.png" alt=""><figcaption></figcaption></figure>

### Request

```
// Curl
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "rozodevDemo",
    "orderId": "order_12345",
    "type": "exactIn",
    "display": {
        "title": "Order #12345",
        "currency": "USD"
    },
    "source": {
        "chainId": "8453",
        "tokenSymbol": "USDC",
        "amount": "1.00"
    },
    "destination": {
        "chainId": "1500",
        "receiverAddress": "GDFLZTLVMLR3OVO4VSODYB7SGVIOI2AS652WODBCGBUQAMXXXXXXXXXX",
        "tokenSymbol": "USDC"
    }
}'
```



### Response

```json
{
  "id": "c3564ae8-74e0-4007-a8f9-91a1d3e3c81d",
  "appId": "rozodevDemo",
  "orderId": "order_12345",
  "status": "payment_unpaid",
  "errorCode": null,
  "type": "exactIn",
  "createdAt": "2025-12-02T02:23:31.743+00:00",
  "updatedAt": "2025-12-02T02:23:31.743+00:00",
  "expiresAt": "2025-12-02T03:23:31.743+00:00",
  "display": {
    "title": "Order #12345",
    "description": null,
    "currency": "USD"
  },
  "source": {
    "chainId": "8453",
    "tokenSymbol": "USDC",
    "tokenAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "amount": "1.00",
    "receiverAddress": "0x5B63758b0954fFc9D803dEC550eCB485C9c15861",
    "receiverMemo": null,
    "fee": "0.01",
    "senderAddress": null,
    "txHash": null,
    "amountReceived": null,
    "confirmedAt": null
  },
  "destination": {
    "chainId": "1500",
    "receiverAddress": "GDFLZTLVMLR3OVO4VSODYB7SGVIOI2AS652WODBCGBUQAMXXXXXXXXXX",
    "receiverMemo": null,
    "tokenSymbol": "USDC",
    "tokenAddress": "USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
    "amount": "0.99",
    "txHash": null,
    "confirmedAt": null
  }
}
```

&#x20;&#x20;
