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
  if (mode === 'create') {
    if (existsSync(receiptFile)) {
      throw new Error('An order is already saved. Run status to resume it.');
    }
    if (!process.env.ROZO_ORDER_ID) {
      throw new Error('Set ROZO_ORDER_ID to your own stable, unique order reference.');
    }
    body.orderId = process.env.ROZO_ORDER_ID;
    if (body.destination) {
      if (!process.env.ROZO_RECEIVER_ADDRESS) {
        throw new Error('Set ROZO_RECEIVER_ADDRESS to the intended destination.');
      }
      body.destination.receiverAddress = process.env.ROZO_RECEIVER_ADDRESS;
    }
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
