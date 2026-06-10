# Merchant API Keys — Admin vs Orders scope, and using them from an AI agent

Rozo merchant API keys let you create and reconcile payments programmatically — from a
POS, a backend service, or an autonomous AI agent. Every key carries a **scope** that
controls what it can do. This page explains the two scopes, when to use each, the
endpoints they unlock, and how to wire a key into an AI agent safely.

All keys share the `rz_live_` prefix and are passed in the `X-API-Key` header.

## Scopes at a glance

| Scope | What it can do | Where it's safe | Default |
| ----- | -------------- | --------------- | ------- |
| **Orders** | Create payments + read payment status | Backend, POS, server-rendered checkout | ✅ Recommended default |
| **Admin** | Everything Orders can do **+ read merchant stats** | Your own backend only | Only when explicitly chosen |

- **Orders key** — the default and recommended choice. It can create payment orders and
  read their status. This is everything a checkout flow needs. Because it cannot read
  account-level stats or change settings, it is safe to place in a POS terminal, a backend
  payment service, or a server-rendered checkout.
- **Admin key** — a full-power key. In addition to creating and reading orders, it can read
  your merchant statistics (volume, payment counts, payouts). It is sensitive and must
  **never** ship to a frontend, a mobile app, or a shared device. Keep it on a server you
  control.

When you create a key, the scope defaults to **Orders**. You only get an Admin key if you
explicitly select the Admin scope.

## API hosts

Different capabilities live behind two services. Use the right base URL for each call.

| Capability | Service | Base URL |
| ---------- | ------- | -------- |
| Create / read orders | `payment-api` | `https://intentapiv4.rozo.ai/functions/v1/payment-api` |
| Read merchant stats | `merchant-api` | `https://aozudqtlykbhzbuzalzz.supabase.co/functions/v1/merchant-api` |

Authenticate every request with your key:

```
X-API-Key: rz_live_xxx
```

## Getting a key

1. Sign in at [partners.rozo.ai](https://partners.rozo.ai) with your email (one-time
   passcode / OTP login).
2. Go to **Settings → API Keys**.
3. Click **New key** and choose the scope (**Orders** by default, or **Admin** if you need
   stats).
4. **Copy the full key immediately — it is shown only once.** Store it in your secret
   manager. If you lose it, revoke it and issue a new one.

## Creating a payment order

Both Orders and Admin keys can create orders. Use the `payment-api` host.

- Leave `destination` **unset** — the payout is locked to your merchant wallet on the
  server side. You only declare what the customer pays (`source`).
- `orderId` is **idempotent**: re-sending the same `orderId` returns the existing order
  instead of creating a duplicate. Use your own internal order reference.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api' \
  --header 'X-API-Key: rz_live_xxx' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "type": "exactIn",
    "orderId": "order_123",
    "display": {
      "name": "Cappuccino"
    },
    "source": {
      "chainId": "8453",
      "tokenSymbol": "USDC",
      "amount": "5.00"
    }
  }'
```

The response includes the order `id`, its `status` (starts at `unpaid`), and a hosted
payment link / deposit address you can present to the customer.

## Reading order status

Both scopes can read orders. Poll this endpoint to reconcile.

```bash
curl --location \
  'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/order/<appId>/<orderId>' \
  --header 'X-API-Key: rz_live_xxx'
```

Order status moves through:

```
unpaid → payin_completed → payout_completed
```

- `unpaid` — order created, customer has not paid yet.
- `payin_completed` — the customer's funds have arrived.
- `payout_completed` — funds have settled to your merchant wallet. The order is done.

## Reading merchant stats (Admin only)

Stats live on the `merchant-api` host and require an **Admin** key. Calling this endpoint
with an Orders key returns `403 scope_insufficient`.

```bash
curl --location \
  'https://aozudqtlykbhzbuzalzz.supabase.co/functions/v1/merchant-api/me/stats?period=7d' \
  --header 'X-API-Key: rz_live_xxx'
```

`period` accepts `today`, `7d`, or `30d`.

```json
{
  "period": "7d",
  "volumeUsdc": "1240.50",
  "paymentCount": 248,
  "avgOrderUsdc": "5.00",
  "netToWalletUsdc": "1228.10",
  "chart": [
    { "date": "2026-06-02", "volumeUsdc": "180.00", "paymentCount": 36 },
    { "date": "2026-06-03", "volumeUsdc": "210.50", "paymentCount": 42 }
  ]
}
```

If you call it with an Orders key:

```json
{
  "error": "scope_insufficient",
  "message": "This endpoint requires an admin-scope API key."
}
```

## Using a key from an AI agent

A common AI-native pattern is to hand a single API key to an autonomous backend agent that
operates the merchant account programmatically — taking payments and reporting on them
without a human in the loop.

Match the scope to what the agent does:

- **Taking payments / reconciling** → give the agent an **Orders** key. It can create
  collection orders for a customer and poll them to confirm settlement. Nothing more.
- **Building reports / dashboards** → give the agent an **Admin** key so it can pull
  `/me/stats`. Only do this if the agent runs entirely on infrastructure you control.

### Example agent workflow

A typical "take a payment and reconcile it" loop:

1. **Create the order** (Orders or Admin key):

   ```bash
   curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api' \
     --header 'X-API-Key: rz_live_xxx' \
     --header 'Content-Type: application/json' \
     --data-raw '{
       "type": "exactIn",
       "orderId": "order_123",
       "display": { "name": "AI agent invoice" },
       "source": { "chainId": "8453", "tokenSymbol": "USDC", "amount": "5.00" }
     }'
   ```

2. **Give the customer the payment link** returned in the response.

3. **Poll for status** until it reaches `payout_completed`:

   ```bash
   curl --location \
     'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/order/yourAppId/order_123' \
     --header 'X-API-Key: rz_live_xxx'
   ```

4. **Reconcile**: when status is `payout_completed`, mark the order paid in your own
   system. For periodic reporting, an Admin-keyed agent calls
   `/me/stats?period=today` and writes the numbers to your dashboard.

In pseudocode the agent loop is:

```
order = POST /payment-api  { orderId, source }
present(order.paymentLink)
loop:
    status = GET /payment-api/payments/order/{appId}/{orderId}
    if status == "payout_completed": break
    sleep(interval)
mark_paid(order)
```

## Security

- Treat every key as a **server-side secret**. Store it in environment variables or a
  secret manager (not in code).
- **Never** put a key in git, in a frontend bundle, in a mobile app, in logs, or in a chat
  message.
- An **Admin** key is full-power — keep it on your own backend only. If your agent's code
  or runtime could be touched by a third party, give it an **Orders** key, never Admin.
- Keys are shown **only once** at creation. If a key leaks, **revoke it in the
  [partners.rozo.ai](https://partners.rozo.ai) dashboard and issue a new one** immediately.

> **Tip:** Start with an Orders key. Only mint an Admin key when you have a concrete need
> to read stats, and scope it to a single backend process you fully control.
