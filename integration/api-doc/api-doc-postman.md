# API Doc (POSTMAN)

## Overview

**Latest version for merchants — Summary**

* **OpenAPI spec:** `docs/openapi.yaml`
* **Version:** `2.0.0` (previously `1.0.0`)
* **Revision date:** `2026-05-11` (recorded in `x-revision-date`)

## Complete Endpoint List

This is everything a merchant needs to look at.

### 1. Payment API (4 endpoints)

All paths are based on the base URL:

```
https://intentapiv4.rozo.ai/functions/v1/payment-api
```

All `POST` requests require the header:

```
X-API-Key: rz_live_xxxxx
```

| #   | Method | Path                                | Purpose                                                                              |
| --- | ------ | ----------------------------------- | ------------------------------------------------------------------------------------ |
| 1   | POST   | `/`                                 | Create an order — returns `id` and `source.receiverAddress` (the deposit address).   |
| 2   | GET    | `/payments/{paymentId}`             | Look up an order by Rozo payment id.                                                 |
| 3   | GET    | `/payments/order/{appId}/{orderId}` | Look up an order by your own `orderId` (idempotent lookup).                          |
| 4   | POST   | `/payments/{paymentId}/payin`       | (Optional) Accelerate confirmation — tell Rozo the buyer's on-chain `txHash`.        |

### 2. Webhooks (2 outbound events)

Rozo will `POST` to the URL you configure at [partners.rozo.ai](https://partners.rozo.ai), signed with HMAC-SHA256.

| Event                       | Triggered when                                                  |
| --------------------------- | --------------------------------------------------------------- |
| `payment_payin_completed`   | The buyer's payment is confirmed on-chain.                      |
| `payment_payout_completed`  | The merchant wallet has received the funds (final success).     |

**Signature headers**

* `X-Rozo-Timestamp`
* `X-Rozo-Signature`

**Signature contents**

```
sha256(timestamp + "." + raw_body, webhook_secret)
```

## Interactive API Documentation

For the full interactive reference (try-it-out, request/response samples, schemas), open the Apidog portal:

{% embed url="https://apidoc.rozo.ai/" %}
ROZO Payment API — Apidog
{% endembed %}

[Open API Doc on Apidog →](https://apidoc.rozo.ai/)
