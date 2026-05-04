# Scripts — Mainnet integration samples

End-to-end mainnet flows against the public Rozo API at:

```
https://intentapiv4.rozo.ai
```

No auth header required. USDC only.

---

## Stellar G-account → Stellar C-address

`stellar-g-to-c.sh` sends USDC from a classic Stellar **G-account** to a Soroban **C-address** (smart wallet / contract account) on the same chain, routed through Rozo.

### Why route this through Rozo?

A classic Stellar G-account cannot natively `payment` to a Soroban contract address — the Stellar network rejects the op. Rozo's hub bridges the two halves:

- **Payin (G side)**: user sends USDC to the Rozo Stellar hub G-address with a unique `memo_text`. Hub matches the deposit to the order via the memo.
- **Payout (C side)**: hub invokes `transfer(from, to, i128)` on the USDC Stellar Asset Contract over Soroban RPC. The destination C-address is credited.

Both legs ride the same `POST /payments` endpoint with `source.chainId = destination.chainId = 1500`.

### Usage

```bash
# Manual deposit
bash scripts/stellar-g-to-c.sh 0.10 CCYO2DDE3ZWBGGRTGOWJOV4KO2HLXHCT7WN7TH7BOYUGQMXTGKWU4IGV

# Auto-deposit using TEST_STELLAR_PAYER_SECRET
AUTO=1 bash scripts/stellar-g-to-c.sh 0.10
```

If you omit the C-address, the script reads `STELLAR_C_RECEIVER_ADDRESS` from `.env.dev`.

### `.env.dev` requirements

| Variable                      | Required for | Purpose                                                          |
|-------------------------------|--------------|------------------------------------------------------------------|
| `STELLAR_C_RECEIVER_ADDRESS`  | optional     | Default destination C-address when no CLI arg is passed          |
| `TEST_STELLAR_PAYER_SECRET`   | `AUTO=1`     | Stellar G-account secret (S…) used to auto-broadcast the payin   |
| `TEST_STELLAR_PAYER_ADDRESS`  | optional     | Public G-address of the payer, printed for confirmation          |

`.env.dev` is gitignored. **Never commit secrets.**

The `AUTO=1` mode shells out to `scripts/_send-stellar-usdc.ts` — keep that helper consistent with the existing testnet helper of the same name.

### Status transitions

```
payment_unpaid → payment_payin_completed → payment_completed   (happy path)
payment_unpaid → payment_expired                                 (TTL)
              ↘ payment_bounced                                   (payout error)
```

`payment_bounced` with `errorMessage: "Bad union switch: 4"` means the deployed payout function is on an outdated `@stellar/stellar-sdk` (pre-15 cannot decode Protocol-23 `TransactionMeta v4`). Bump the SDK and redeploy.
