---
description: Make a read-only discovery request, configure access, and run the payment examples.
---

# Make Your First API Request

The examples use Node.js 18 or later and no additional packages. Start with a read-only request, then choose the Merchant or Wallet quick start.

## 1. Check the API without an account

```bash
curl --fail-with-body 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/supported?provider=auto'
```

Expect HTTP 200 and JSON containing supported-chain data. This request does not create an order or move funds. The general list is for discovery; a successful quote for your app confirms the selected combination is available.

## 2. Set up your app

1. Register at [partners.rozo.ai](https://partners.rozo.ai) and verify your email.
2. Use a **Merchant app** for payments into a configured settlement wallet, or a **Wallet app** when you supply a destination per request. If the required app type is not available to your account, [contact Rozo](../../contact/contact-us/README.md) before continuing.
3. Create an **Orders** API key under **Settings → API Keys**. See [key scopes](merchant-api-keys.md#scopes-at-a-glance).
4. Set `ROZO_API_KEY` through your local or server secret manager. Keep it out of browser code, screenshots, chat messages and source control. The examples read it from the environment; do not put the key in command-line arguments.

New integrations use `X-API-Key`. No additional Bearer token is needed for these payment examples. The key identifies your app. App-specific capabilities can still require separate enablement.

## 3. Save the example client

Save the following as `payment.mjs` in your local example directory. It only contacts the API; it never signs or sends a wallet transaction. `quote` is the default mode. The [source file](https://github.com/RozoAI/rozo-docs/blob/main/scripts/examples/payment.mjs) contains the same code.

```js
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

// Node.js 18+. Credentials stay in the server environment.
const mode = process.argv[2] ?? 'quote';
if (!['quote', 'create', 'status'].includes(mode)) {
  throw new Error('Usage: node payment.mjs quote|create|status');
}
const apiKey = process.env.ROZO_API_KEY;
if (!apiKey) throw new Error('Set ROZO_API_KEY in your server environment.');
const base = 'https://intentapiv4.rozo.ai/functions/v1/payment-api';
const receiptFile = '.rozo-payment.json';

async function request(path, body) {
  const response = await fetch(`${base}${path}`, {
    method: body ? 'POST' : 'GET',
    headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
    ...(body ? { body: JSON.stringify(body) } : {}),
    signal: AbortSignal.timeout(30_000),
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const code = data?.data?.errorCode ?? data?.error?.code ?? 'request_failed';
    throw new Error(`HTTP ${response.status}: ${code}. Request ID: ${data?.requestId ?? 'unavailable'}`);
  }
  if (!data) throw new Error('Expected a JSON response.');
  return data;
}

if (mode === 'status') {
  const saved = JSON.parse(readFileSync(receiptFile, 'utf8'));
  if (!saved.id) throw new Error('No payment ID saved.');
  const payment = await request(`/payments/${encodeURIComponent(saved.id)}`);
  console.log({ status: payment.status, destinationAmount: payment.destination?.amount,
    destinationTxHash: payment.destination?.txHash });
} else {
  const body = JSON.parse(readFileSync('payment-request.json', 'utf8'));
  if (body.destination) {
    if (!process.env.ROZO_RECEIVER_ADDRESS) {
      throw new Error('Set ROZO_RECEIVER_ADDRESS before quoting or creating a wallet transfer.');
    }
    body.destination.receiverAddress = process.env.ROZO_RECEIVER_ADDRESS;
  }
  if (mode === 'create') {
    if (existsSync(receiptFile)) {
      throw new Error('An order is already saved. Run status to resume it.');
    }
    if (!process.env.ROZO_ORDER_ID) {
      throw new Error('Set ROZO_ORDER_ID to your own stable, unique order reference.');
    }
    body.orderId = process.env.ROZO_ORDER_ID;
  }
  const result = await request(mode === 'quote' ? '/payments?dryrun=true' : '/payments', body);
  if (mode === 'quote') {
    console.log({ status: result.status, sourceAmount: result.source?.amount,
      destinationAmount: result.destination?.amount, sourceFee: result.source?.fee, feeInfo: result.feeInfo });
  } else {
    if (!result.id) throw new Error('No payment ID returned. Reconcile by order reference before retrying.');
    writeFileSync(receiptFile, JSON.stringify(result, null, 2), { flag: 'wx', mode: 0o600 });
    console.log('Order saved privately to .rozo-payment.json. No wallet transaction was sent.');
  }
}

```

Keep `.rozo-payment.json` private and add it to your project's `.gitignore`. It stores the order response so you can resume status checks. Use a separate example directory for each new order. If a create request times out before the file is saved, keep the same `ROZO_ORDER_ID` and reconcile through [order lookup](merchant-api-keys.md#reading-order-status); do not switch to a new order reference or pay twice.

## 4. Choose a request

- [Merchant quick start](api-quick-start-merchant.md): configure a merchant wallet, quote, create, present payment instructions and reconcile.
- [Wallet quick start](api-quick-start.md): quote a transfer, set the intended destination, create and check settlement.

Each guide supplies `payment-request.json`. Before creating an order, set `ROZO_ORDER_ID` to your application's unique order reference. Keep that reference unchanged when retrying the same request. Wallet transfers require `ROZO_RECEIVER_ADDRESS` before both quoting and creating the order.

## Common errors

| Result | What to check |
| --- | --- |
| `missing_api_key` or `invalid_api_key` | Ensure `ROZO_API_KEY` is available to Node and belongs to your app |
| `insufficient_scope` | Use a key with permission to create and read orders |
| `email_not_verified` | Complete email verification in the partner portal |
| `destination_not_allowed` | Use a Wallet app for a caller-selected destination; Merchant apps use their configured wallet |
| `paymentNotFound` | Check the payment ID and use the same app's key that created it |
| `authorization_unavailable` or a network timeout | Preserve the order reference and retry later; do not bypass authentication |
| A quote or route error | Follow the returned code and [quote error reference](api-for-advanced-used/get-fees.md#error-responses) |

The client reports HTTP status, error code and request ID without printing credentials or the full order. Share the request ID with [support](../../contact/contact-us/README.md) when needed.
