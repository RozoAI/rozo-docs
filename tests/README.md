# Tests — Base Sepolia → Stellar Testnet

End-to-end testnet bridges from **Base Sepolia USDC** to **Stellar testnet USDC**, covering both Stellar destination types:

- **G-address** (classic Stellar account) — payout via Horizon `Operation.payment`
- **C-address** (Soroban smart-contract account, e.g. smart wallets, AMMs) — payout via the **Stellar Asset Contract (SAC)** `transfer(from, to, i128)` over Soroban RPC

Both flows hit the public testnet API at:

```
https://intentapitestnet.rozo.ai
```

No auth header required. USDC only. Amount range 0.01–1.00. Order TTL 10 min.

---

## Scripts

| Script | Destination | Default amount |
|---|---|---|
| [`testnet-base-to-stellar.sh`](./testnet-base-to-stellar.sh) | G-address (`G…`) | `0.01` |
| [`testnet-base-to-stellar-c.sh`](./testnet-base-to-stellar-c.sh) | C-address (`C…`) | `0.02` |

Both scripts:

1. `POST /payments` with `type=exactIn`, `source.chainId=84532` (Base Sepolia), `destination.chainId=1500` (Stellar testnet).
2. Print the returned `source.receiverAddress` (Rozo hub) and `source.amount` (may be auto-incremented by $0.01 for collision avoidance).
3. Either pause for a manual deposit, or — with `AUTO=1` — auto-broadcast using the test keys in `.env.dev`.
4. Poll `GET /payments/{id}` until `payment_completed`, `payment_bounced`, or `payment_expired`.

---

## Quick start

```bash
# Manual deposit (you send the USDC yourself from any wallet)
bash tests/testnet-base-to-stellar.sh 0.01
bash tests/testnet-base-to-stellar-c.sh 0.02

# Auto-deposit using TEST_EVM_PAYER_PRIVATE_KEY
AUTO=1 bash tests/testnet-base-to-stellar.sh 0.01
AUTO=1 bash tests/testnet-base-to-stellar-c.sh 0.02
```

Override the C-address destination:

```bash
AUTO=1 bash tests/testnet-base-to-stellar-c.sh 0.02 CCYO2DDE3ZWBGGRTGOWJOV4KO2HLXHCT7WN7TH7BOYUGQMXTGKWU4IGV
```

---

## `.env.dev` requirements

| Variable | Purpose |
|---|---|
| `TEST_EVM_PAYER_PRIVATE_KEY` + `TEST_EVM_PAYER_ADDRESS` | Source-side signer (Base Sepolia) |
| `TEST_STELLAR_RECEIVER_ADDRESS` | Default G-address destination |
| `TEST_STELLAR_C_RECEIVER_ADDRESS` | Default C-address destination |

Generate fresh test keys: `npx tsx scripts/gen-hub-keys.ts --test-wallets`. Fund payer at the [Circle USDC faucet](https://faucet.circle.com/) and [Alchemy Base Sepolia faucet](https://www.alchemy.com/faucets/base-sepolia).

---

## What's different about the C-address payout

A Stellar **C-address** is a Soroban contract identifier, not a classic account. Three differences vs. the G-path:

1. **No `memo_text`.** Soroban contract calls have no memo field. Any memo passed in the order is dropped with a log warning.
2. **SAC contract call, not `payment` op.** The hub invokes `transfer(from, to, i128)` on the auto-deployed Stellar Asset Contract for USDC. The contract id is derived deterministically from `(asset, networkPassphrase)`.
3. **Submitted via Soroban RPC**, not Horizon. Status is polled with `getTransaction(hash)` and the `meta` returned is Protocol-23 `TransactionMeta v4` — make sure any client decoding it uses `@stellar/stellar-sdk` ≥ 15 (older SDKs throw `Bad union switch: 4` on the decode).

The order schema is identical for both — clients pass `destination.receiverAddress` as either a `G…` or a `C…` and the API routes correctly.

---

## Verified end-to-end run

A run of `testnet-base-to-stellar-c.sh 0.02` against `CCYO2DDE3ZWBGGRTGOWJOV4KO2HLXHCT7WN7TH7BOYUGQMXTGKWU4IGV`:

```text
Payment id : pay_ewHL66ke5XdqP7GLZ8xnkVPh
Send TO    : 0x4843B70de3Aa77CFbfDA0BAf468e3C4f32B1FA34
Send AMOUNT: 0.03 USDC (Base Sepolia)   ← 0.02 + $0.01 collision step
Dest C-addr: CCYO2DDE3ZWBGGRTGOWJOV4KO2HLXHCT7WN7TH7BOYUGQMXTGKWU4IGV
…
[1] status = payment_unpaid
[2] status = payment_completed
```

| Leg | Tx hash | Confirmation |
|---|---|---|
| Base Sepolia payin (USDC → hub) | `0x92d4ed6ab6270c9d7e0db4b251ccd2c8aef41f9be311678491e6cf6caa199237` | block 41065985, success |
| Stellar payout (SAC `transfer` → C-address) | `e7eedc04fb5605550a0e5c8c98ad310fe26f93b3bee5c6bf65af24d6477c4572` | ledger 2378571, SUCCESS, 0.0300000 USDC credited to the contract |

End-to-end time: ~10 seconds.

---

## Status transitions

```
payment_unpaid → payment_payin_completed → payment_completed   (happy path)
payment_unpaid → payment_expired                                 (TTL)
              ↘ payment_bounced                                   (payout error)
```

`payment_bounced` with `errorMessage: "Bad union switch: 4"` on a C-address destination means the deployed payout function is on an outdated `@stellar/stellar-sdk` (Protocol 23 `TransactionMeta` decoding broke pre-15.0). Bump the SDK and redeploy.
