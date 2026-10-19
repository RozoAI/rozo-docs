---
description: >-
  Beta. Give a Stellar smart account (C address) a fixed classic G address so
  exchanges and ordinary wallets can deposit to it, and withdraw from it to an
  exchange deposit address with the memo the exchange requires.
---

# Exchange Deposits and Withdrawals for Smart Accounts (Beta)

Stellar smart accounts (Soroban contract accounts, addresses starting with `C`) cannot receive a classic `payment` operation, and a transaction that invokes a contract cannot carry a memo. Exchanges only send classic payments and only credit deposits that carry their memo. This page describes the two Rozo flows that bridge that gap:

| Direction | What you get | Who pays the network fee |
| --- | --- | --- |
| Deposit: exchange or wallet → your C | A fixed `G` address bound to your `C`. Anything sent there in USDC is forwarded into your `C` automatically | Rozo (sponsored reserves and fee-bumped forwarding) |
| Withdraw: your C → exchange | A Rozo order you pay from your `C`; Rozo sends a classic payment to the exchange `G` address with the exact memo | Rozo, fee included in the order |

**Status**: Beta. Both flows are enabled per app. Ask us to enable your `appId`. Amount limits and the allowlist are set by Rozo during Beta.

## Deposit: a fixed G address for your C

### How it works

1. You bind your `C` once. Rozo derives a `G` address for it deterministically: the same `C` always gets the same `G`, on the same network.
2. Rozo creates the `G` account with sponsored reserves and a USDC trustline. You do not need to fund it.
3. Anyone sends USDC to the `G` address. Memo is not needed. If the sender's platform forces a memo, any value is fine; it is recorded and ignored.
4. Within a few minutes Rozo forwards the USDC into your `C` with a Soroban token transfer. If your `C` is not deployed yet, Rozo deploys it first.

The `G` address is operated by Rozo and can only move funds to the `C` it is bound to. It is an intake address, not a wallet: do not store other assets there.

### API

Host: `https://iufqieirueyalyxfzszh.supabase.co/functions/v1`

**Bind or look up the G address**

```bash
curl -X POST 'https://iufqieirueyalyxfzszh.supabase.co/functions/v1/app_stellar_intake' \
  -H 'Content-Type: application/json' \
  -d '{ "c_address": "C...your smart account..." }'
```

Response (201 on first bind, 200 afterwards):

```json
{
  "id": "7ac81248-...",
  "c_address": "C...",
  "g_address": "G...",
  "network": "public",
  "status": "allocated",
  "derivation_version": 1,
  "activation_tx_hash": null,
  "created": true
}
```

`id` is the mapping id used by the receipts endpoint.

`status` is `allocated` until the account is created on chain, then `active`. Only share the `G` address once it is `active`.

**Look up by address**

```bash
GET /app_stellar_intake/c/{c_address}
GET /app_stellar_intake/g/{g_address}
```

**Monitor incoming deposits**

```bash
GET /app_stellar_intake/{id}/receipts?limit=50&offset=0
```

The response is `{ "mapping_id", "limit", "offset", "receipts": [...] }`. Each receipt is one incoming transfer event:

| Field | Meaning |
| --- | --- |
| `tx_hash`, `op_index`, `event_index` | Where the money arrived on chain. One Soroban operation can carry several transfers, so the event index is part of the key |
| `from_address` | Who sent it |
| `asset_code`, `asset_issuer`, `amount_stroops` | What arrived, in stroops (7 decimals) |
| `fee_stroops`, `net_stroops` | Rozo fee and what was forwarded to your `C` |
| `state` | See below |
| `batch_id`, `batch_state` | Several receipts can be forwarded together in one batch |
| `forward_tx_hash` | The Soroban transaction that moved the net amount into your `C` |
| `fee_tx_hash` | The classic payment that moved the fee |

| `state` | Meaning | What to do |
| --- | --- | --- |
| `detected` | Seen on chain, not yet forwarded | Wait |
| `accumulated` | Smaller than the minimum fee, held until more arrives and forwarded together | Nothing, or send more |
| `claimed` | A forwarding transaction is being built or submitted | Wait |
| `confirmed` | Forwarded, `forward_tx_hash` is set | Done |
| `retryable` | A transient failure, will be retried | Wait, contact us if it stays for over an hour |
| `manual_review` | Needs a human. Also used for XLM or unsupported assets sent to the `G` | Contact support with the receipt id |

### Fees and limits

| Item | Value |
| --- | --- |
| Forwarding fee | 0.1% of the amount, minimum 0.05 USDC, taken from the amount |
| Minimum forwarded amount | Deposits at or below the minimum fee are held as `accumulated` and forwarded together once the total exceeds it |
| Supported asset | USDC (issuer `GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN`) only. XLM and other assets are not forwarded and go to manual review |
| Memo | Not required for deposits. Any memo is recorded and ignored |

## Withdraw: from your C to an exchange with a memo

### How it works

Use the Intent API with `intent: "stellar_exchange_withdraw"`. The order behaves like [Stellar Smart Account Payments](stellar-contract-payments.md): you receive a per-order contract address and pay it from your `C`. Once the payment is detected, Rozo sends a classic payment to the exchange `G` address with the memo you provided.

Intent API host: `https://intentapiv4.rozo.ai/functions/v1`

```bash
curl -X POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
  -H 'Content-Type: application/json' \
  -d '{
    "appId": "yourAppId",
    "intent": "stellar_exchange_withdraw",
    "type": "exactIn",
    "display": { "title": "Withdraw to exchange", "currency": "USD" },
    "source": {
      "senderAddress": "C...your smart account...",
      "chainId": 1500,
      "tokenSymbol": "USDC",
      "amount": "25"
    },
    "destination": {
      "receiverAddress": "G...exchange deposit address...",
      "receiverMemo": "1234567890",
      "memoType": "text",
      "chainId": 1500,
      "tokenSymbol": "USDC"
    }
  }'
```

Rules:

| Field | Rule |
| --- | --- |
| `source` | Stellar (`1500`) USDC, `senderAddress` is your `C` |
| `destination.receiverAddress` | The exchange's Stellar deposit address (`G...`). Copy it from the exchange deposit page, never from wallet history |
| `destination.receiverMemo` | Exactly what the exchange shows. Required. Text memo, at most 28 bytes UTF-8 |
| `destination.memoType` | Optional. Only `text` is supported in Beta. If your exchange shows "Memo ID", contact us before sending |
| Fee | Fixed 0.1 USDC per withdrawal during Beta, taken from the amount. Shown in `feeBreakdown` on the order |

Pay the order from your `C` as described in [Stellar Smart Account Payments](stellar-contract-payments.md). Then poll:

```bash
GET /payment-api/payments/{paymentId}
```

`payment_payout_completed` means the exchange has received the classic payment. `destinationTxHash` is the Stellar transaction; its memo is the one you provided.

### Why the withdrawal goes through Rozo

Your `C` cannot attach a memo to anything it sends (Soroban transactions have no memo field), and most exchanges ignore deposits without their memo. Rozo pays the exchange from a classic account and carries the memo for you.

## Monitoring checklist for integrators

- Deposits: poll `GET /app_stellar_intake/{id}/receipts` or watch your `C` balance. A receipt in `manual_review` or `retryable` for more than an hour is worth a support ticket; include the receipt id.
- Withdrawals: poll the order until `payment_payout_completed`; if it stays `payment_started` for more than 30 minutes after you paid, send us the `paymentId`.
- Never send XLM to the `G` address. It is not forwarded.
- The `G` address does not change. If Rozo ever rotates derivation keys, your old `G` keeps working and you will be told the new one in the bind response (`derivation_version` increases).

## Beta limitations

- Enabled per `appId`; destinations and amounts may be capped.
- Text memo only. Memo ID is not supported yet.
- USDC only.
- No fee refund for a withdrawal the exchange refuses to credit because of a wrong memo. Double check the memo before you pay.
