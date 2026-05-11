# API Doc (POSTMAN)

## Overview

**Latest version for merchants — Summary**

* **OpenAPI spec (v2.0.0):** [`docs/openapi-v2.0.0.yaml`](https://github.com/RozoAI/rozo-docs/blob/main/docs/openapi-v2.0.0.yaml) — hosted in this docs repo
* **Raw download:** [`raw.githubusercontent.com/.../openapi-v2.0.0.yaml`](https://raw.githubusercontent.com/RozoAI/rozo-docs/main/docs/openapi-v2.0.0.yaml)
* **Version:** `2.0.0` (previously `1.0.0`)
* **Revision date:** `2026-05-11` (recorded in `x-revision-date`)
* **This page:** [https://docs.rozo.ai/integration/api-doc/api-doc-postman](https://docs.rozo.ai/integration/api-doc/api-doc-postman)
* **Docs source on GitHub:** [rozoai/rozo-docs](https://github.com/RozoAI/rozo-docs)

## Get Your API Key

Before calling any endpoint, you need an API key from the Rozo merchant portal.

1. Sign in at [**partners.rozo.ai**](https://partners.rozo.ai).
2. Create or open your merchant app — your `appId` will look like `merchant_<slug>` or `wallet_<slug>`.
3. Generate an API key — format: `rz_live_xxxxx`. The key is bound to that `appId`.
4. Configure your **webhook URL** in the portal (used for `payment_payin_completed` and `payment_payout_completed` events).
5. Pass the key on every `POST` request as the `X-API-Key` header:

```
X-API-Key: rz_live_xxxxx
```

> When `X-API-Key` is present, the key's `app_id` is authoritative — a stale `appId` in the request body is silently overridden. This is cross-tenant defense, so you cannot accidentally write into another merchant's namespace.

**Auth errors**

* `400 missing_api_key` — `appId` requires a key but none was provided.
* `400 invalid_api_key` — key is unknown, revoked, expired, or inactive.

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
