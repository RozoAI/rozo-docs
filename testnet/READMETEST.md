# Rozo Intents — Testnet Integration Guide

A minimal, **public** testnet API for cross-chain USDC transfers between **Base Sepolia** and **Stellar testnet**. Intended for partners building integrations against the production API at <https://docs.rozo.ai/>.

## API endpoint

```
https://intentapitestnet.rozo.ai
```

All endpoints are public. No authentication header is required.

## Limits & behavior

| | |
|---|---|
| Token | USDC only |
| Chains | Base Sepolia (`84532`) ⇄ Stellar testnet (`1500`) |
| Amount range | 0.01 – 1.00 USDC |
| Fee | always 0 |
| Order TTL | 10 minutes (auto-expires if not paid) |
| Amount collision | auto-stepped +0.01 (so two pending orders never share `source.amount`) |

API surface mirrors the production API at <https://apidoc.rozo.ai/>.

---

## Endpoints

### Create payment — `POST /functions/v1/payment-api/payments`

```bash
curl -X POST https://intentapitestnet.rozo.ai/functions/v1/payment-api/payments \
  -H "Content-Type: application/json" \
  -d '{
    "appId": "your-app-id",
    "orderId": "order-12345",
    "type": "exactIn",
    "display": { "title": "Order #12345", "currency": "USD" },
    "source":      { "chainId": "84532", "tokenSymbol": "USDC", "amount": "0.10" },
    "destination": { "chainId": "1500",  "tokenSymbol": "USDC",
                     "receiverAddress": "G..." }
  }'
```

Response (`201 Created`):

```json
{
  "id": "pay_xxxxxxxxxxxxxxxxxxxxxxxx",
  "status": "payment_unpaid",
  "expiresAt": "2026-05-04T16:11:08.875+00:00",
  "source": {
    "chainId": "84532",
    "amount": "0.10",
    "receiverAddress": "0x4843B70de3Aa77CFbfDA0BAf468e3C4f32B1FA34"
  },
  "destination": {
    "chainId": "1500",
    "amount": "0.10",
    "receiverAddress": "G..."
  }
}
```

The user must send **exactly** `source.amount` USDC to `source.receiverAddress`. For Stellar source, also include the returned `source.receiverMemo` as `memo_text`.

### Fee preview (dryrun) — `POST /functions/v1/payment-api/payments?dryrun=true`

Same body as create, returns fee/receive amount preview without persisting. Always `fee: "0"` on testnet.

### Get payment — `GET /functions/v1/payment-api/payments/{id}`

```bash
curl https://intentapitestnet.rozo.ai/functions/v1/payment-api/payments/pay_xxx
```

Status transitions:
- `payment_unpaid` → `payment_payin_completed` → `payment_completed` (happy path)
- `payment_unpaid` → `payment_expired` (TTL hit)
- `payment_bounced` (payout-side error; rare on testnet)

### Get payment by orderId — `GET /functions/v1/payment-api/payments/order/{appId}/{orderId}`

Same response shape as get-by-id.

---

## Sample scripts

The `scripts/testnet-*.sh` scripts are runnable examples. They use bare `curl`, no SDK, no auth header.

| Script | Purpose |
|---|---|
| `scripts/testnet-get-fee.sh [AMOUNT] [DIRECTION]` | Fee preview (`?dryrun=true`) |
| `scripts/testnet-amount-collision.sh [AMOUNT]` | Verify amount auto-increment |
| `scripts/testnet-base-to-stellar.sh [AMOUNT]` | Full e2e Base Sepolia → Stellar |
| `scripts/testnet-stellar-to-base.sh [AMOUNT]` | Full e2e Stellar → Base Sepolia |

All `AMOUNT` arguments are USDC, must be in `[0.01, 1.00]`.

### Quick start

```bash
# fee preview, no chain action
bash scripts/testnet-get-fee.sh 0.10 base-to-stellar

# amount collision: 3 orders, same requested amount
bash scripts/testnet-amount-collision.sh 0.50

# full round trip (small amounts to save testnet USDC)
AUTO=1 bash scripts/testnet-base-to-stellar.sh 0.01
AUTO=1 bash scripts/testnet-stellar-to-base.sh 0.02
```

Or via npm aliases:

```bash
npm run testnet:fee
npm run testnet:collision
AUTO=1 npm run testnet:base-to-stellar
AUTO=1 npm run testnet:stellar-to-base
```

### `AUTO=1` mode

Without `AUTO=1` the e2e scripts pause and ask you to send the deposit transaction yourself (use any wallet — MetaMask, Phantom, Freighter, Rabby, etc.).

With `AUTO=1` the script broadcasts the deposit using the test keys in `.env.dev`:

| Variable | Used by |
|---|---|
| `TEST_EVM_PAYER_PRIVATE_KEY` + `TEST_EVM_PAYER_ADDRESS` | `testnet-base-to-stellar.sh` |
| `TEST_STELLAR_PAYER_SECRET` + `TEST_STELLAR_PAYER_ADDRESS` | `testnet-stellar-to-base.sh` |
| `TEST_EVM_RECEIVER_ADDRESS` | destination on Base side |
| `TEST_STELLAR_RECEIVER_ADDRESS` | destination on Stellar side |

Generate fresh test keys:

```bash
npm install
npx tsx scripts/gen-hub-keys.ts --test-wallets
```

Fund them at:
- Base Sepolia ETH: <https://www.alchemy.com/faucets/base-sepolia>
- USDC (Base / Stellar testnet): <https://faucet.circle.com/>
- Stellar XLM: <https://laboratory.stellar.org/#account-creator?network=test>
- The Stellar test payer also needs a USDC trustline opened (one-time tx).

---

## Expected output

```
=== Step 1: create payment ===
{
  "id": "pay_4zSN34u1mRKn9NShXvdrugoE",
  "status": "payment_unpaid",
  "source":      { "amount": "0.01", "receiverAddress": "0x4843..." },
  "destination": { "amount": "0.01", "receiverAddress": "G..." }
}

=== Step 2: auto-send ===
Sending 0.01 USDC from 0x4f8f... to 0x4843...
tx: 0x9138...
mined in block 41027894, status=success

=== Step 3: poll status ===
  [1] status = payment_unpaid
  [2] status = payment_completed

=== Final ===
{
  "status": "payment_completed",
  "source":      { "txHash": "0x9138...", "amountReceived": "0.01" },
  "destination": { "txHash": "8de9fd4c...", "confirmedAt": "..." }
}
```

End-to-end time observed in current deploys: ~10–15 seconds.
