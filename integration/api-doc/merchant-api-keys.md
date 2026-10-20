# API Keys and Payment Status

Use an API key to create and read payments from your own backend. The key identifies your app; it does not authorize spending from a customer's wallet.

## Scopes at a glance

| Scope | Access | Recommended use |
| --- | --- | --- |
| **Orders** | Create payments and read order status | Payment integration on your backend |
| **Admin** | Orders access plus merchant statistics | Your private reporting backend, only if needed |

Start with an Orders key. Keep all API keys on your backend or trusted server-side tool. Do not embed them in browser JavaScript, distributable apps, shared prompts or source control. If an agent uses a tool backed by the key, keep the credential inside the tool's server environment rather than exposing it to the model.

## Getting a key

1. Sign in at [partners.rozo.ai](https://partners.rozo.ai) and complete email verification.
2. Configure the app for your integration. Merchant apps use their configured settlement wallet; Wallet apps accept a per-request recipient.
3. Open **Settings → API Keys**, create an **Orders** key, and save it in your secret manager. The full key is shown only once.
4. Set `ROZO_API_KEY` for your backend process. If the key is lost or exposed, revoke it and create a replacement through the portal.

The server sends the key in `X-API-Key`. Follow [Make Your First API Request](first-request.md) for a Node.js example that reads it from the environment, without passing credentials in command-line arguments.

## API hosts

| Operation | Base URL |
| --- | --- |
| Quote, create and read payments | `https://intentapiv4.rozo.ai/functions/v1/payment-api` |
| Merchant statistics and delivery history | `https://aozudqtlykbhzbuzalzz.supabase.co/functions/v1/merchant-api` |

These are programmatic API endpoints. Use the partner portal to manage your account.

## Creating a payment

Use `POST /payments?dryrun=true` to preview a request and `POST /payments` to create an order. Keep the same unique `orderId` when retrying the same request. Before paying, verify the created order's actual amount, asset, destination and expiry.

- [Merchant quick start](api-quick-start-merchant.md): leave `destination` unset; settlement uses your configured wallet.
- [Wallet quick start](api-quick-start.md): use a Wallet app and supply the intended recipient.

Do not use a shared demo app to accept your own customer payments.

## Reading order status

Use your app's key with either:

```text
GET /payments/{paymentId}
GET /payments/order/{appId}/{orderId}
```

The second path is useful when a create request timed out and you retained your own order reference. URL-encode path values. A missing order or an ID belonging to another app returns `paymentNotFound`; it is not a reason to send funds again.

Read the raw `status` field returned by this endpoint. A typical routed payment moves through:

```text
payment_unpaid → payment_payin_completed → payment_payout_started → payment_payout_completed
```

Intermediate states can be observed or skipped between polls. Direct payments can finish as `payment_completed`.

| Raw `status` | Meaning |
| --- | --- |
| `payment_unpaid` | Order created; waiting for the customer |
| `payment_started` | Payment detected; processing |
| `payment_payin_completed` | Incoming funds confirmed; merchant payout may still be pending |
| `payment_payout_started` | Merchant payout is in progress |
| `payment_payout_completed` | Routed payout completed |
| `payment_completed` | Completed direct-payment flow |

For settlement reconciliation, require raw `status` of `payment_payout_completed` or, for a direct payment, `payment_completed`, and reconcile the destination amount and transaction against your order. Handle non-success states through your support/recovery flow instead of fulfilling or paying again.

**Do not use `merchantStatus` as proof of settlement.** It is a separate convenience field: it can already be `payment_completed` at `payment_payin_completed` or `payment_payout_started`, before the merchant's payout finishes.

## Reading merchant statistics

Use an Admin key only when you need statistics. An Orders key is sufficient for the normal payment flow.

```js
// Run on your reporting server, with an Admin key in ROZO_API_KEY.
const apiKey = process.env.ROZO_API_KEY;
if (!apiKey) throw new Error('Set ROZO_API_KEY in your server environment.');
const response = await fetch(
  'https://aozudqtlykbhzbuzalzz.supabase.co/functions/v1/merchant-api/me/stats?period=7d',
  { headers: { 'X-API-Key': apiKey }, signal: AbortSignal.timeout(30_000) },
);
if (!response.ok) throw new Error(`Statistics request failed: HTTP ${response.status}`);
const stats = await response.json();
// Use stats in your private dashboard; never log the credential.
```

`period` accepts `today`, `7d` or `30d`. An Orders key cannot read this endpoint and returns `403 scope_insufficient`. Payment endpoints can use different permission-error codes; check the endpoint's response instead of assuming every service has the same error vocabulary.

## Webhooks and troubleshooting

Use the [webhook guide](api-for-advanced-used/webhook.md) for signature verification, retries and your delivery log. Consult [common setup errors](first-request.md#common-errors) for email verification, key scope and app-type mistakes. Preserve the order reference and request ID when reporting a problem, and never send your API key to support.
