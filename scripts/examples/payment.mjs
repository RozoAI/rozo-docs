import { readFileSync, writeFileSync, existsSync } from 'node:fs';

// Node.js 18+. Credentials stay in the server environment.
const mode = process.argv[2] ?? 'quote';
if (!['quote', 'create', 'status', 'lookup'].includes(mode)) {
  throw new Error('Usage: node payment.mjs quote|create|status|lookup');
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

if (mode === 'lookup') {
  const appId = process.env.ROZO_APP_ID;
  const orderId = process.env.ROZO_ORDER_ID;
  if (!appId || !orderId) throw new Error('Set ROZO_APP_ID and the original ROZO_ORDER_ID for lookup.');
  const payment = await request(`/payments/order/${encodeURIComponent(appId)}/${encodeURIComponent(orderId)}`);
  console.log({ id: payment.id, status: payment.status });
} else if (mode === 'status') {
  if (!existsSync(receiptFile)) {
    throw new Error('No local receipt. If create was attempted, run lookup with the original order reference. Do not create again.');
  }
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
  let result;
  try {
    result = await request(mode === 'quote' ? '/payments?dryrun=true' : '/payments', body);
  } catch (error) {
    if (mode === 'create') {
      throw new Error(`${error.message} Create did not complete locally. Run lookup with the original reference before taking further action; do not create or pay again.`);
    }
    throw error;
  }
  if (mode === 'quote') {
    console.log({ status: result.status, sourceAmount: result.source?.amount,
      destinationAmount: result.destination?.amount, sourceFee: result.source?.fee, feeInfo: result.feeInfo });
  } else {
    if (!result.id) throw new Error('No payment ID returned. Run lookup with the original order reference. Do not create again.');
    try {
      writeFileSync(receiptFile, JSON.stringify(result, null, 2), { flag: 'wx', mode: 0o600 });
    } catch {
      throw new Error('Order created, but receipt could not be saved. Run lookup with the original order reference. Do not create or pay again.');
    }
    console.log('Order saved privately to .rozo-payment.json. No wallet transaction was sent.');
  }
}
