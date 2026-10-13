---
description: >-
  stellar_onboarding: pay USDC or USDT on Base, Ethereum, Arbitrum or Polygon
  and receive USDC on Stellar. A new address gets its account, USDC trustline
  and XLM in one transaction it signs once. No API key.
---

# Open a Stellar Wallet with One Payment and One Signature (`stellar_onboarding`)

No signup. No API key. One payment, one signature.

You send USDC or USDT from Base, Ethereum, Arbitrum or Polygon. We deliver USDC on Stellar to the address you choose. If that address is new or has no USDC trustline, we also create the account, add the trustline and give it some XLM for fees, all in one transaction the address signs once. We never see the secret key.

## Three ways to use it

| Way | For | How |
| --- | --- | --- |
| API | Apps, backends, agents | The steps below. No key |
| Web page | People, no code | Coming soon: connect any Stellar wallet, pick amount and chain, pay, sign once |
| MCP | AI agents (Claude, Cursor, ...) | Coming soon: Rozo MCP tools `stellar_wallet_quote`, `stellar_wallet_create_order`, `stellar_wallet_order_status`, `stellar_wallet_get_signing_request`, `stellar_wallet_submit_signed`. The MCP never holds keys: your agent's wallet pays and signs |

## Supported chains and tokens

| You pay from | Quote with `source.chainId` / USDC `assetId` | USDT also accepted at payment |
| --- | --- | --- |
| Base | `8453` / `erc20:0x833589fcd6edb6e08f4c7c32d4f71b54bda02913` | `0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2` |
| Ethereum | `1` / `erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` | `0xdAC17F958D2ee523a2206206994597C13D831ec7` |
| Arbitrum | `42161` / `erc20:0xaf88d065e77c8cc2239327c5edb3a432268e5831` | `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9` |
| Polygon | `137` / `erc20:0x3c499c542cef5e3811e1192ce70d8cc03d5c3359` | `0xc2132D05D31c914a87C6611C10748AEb04B58e8F` |

| You receive | `assetId` |
| --- | --- |
| USDC on Stellar | `stellar:USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN` |

- Always quote with the chain's USDC `assetId`. When you pay, USDC or USDT (the contracts above) on any of the four chains is accepted 1:1.
- Live list: `GET /funding/capabilities` (`sourceAssets`, `stableOutputs`, `gasOptions`, `limits`).

## Limits

| Limit | Value |
| --- | --- |
| Per order | 1 to 1,000 USD, on every chain |
| Per client IP | 2,000 USD per day (UTC) |
| All keyless traffic together | 10,000 USD per day (UTC) |
| Request rate | Limited per client IP (`429 rate_limited`) |

The per-order limit is checked at quote time and the daily limits when you create the order. Either way the answer is `limit_exceeded`.

## Fees

| Fee | When | Amount |
| --- | --- | --- |
| Bridge fee | Every order | Same as the ROZO bridge: 0.1 %, minimum 0.01 USDC (Ethereum minimum 0.10 USDC) |
| XLM and account opening (`usdGas`) | Optional | `"0"` = no XLM, `"0.5"` = 1.6 XLM, `"1"` = 3.2 XLM. Fixed amounts, no price spread. For a new address this also covers the account and trustline: there is no other opening fee |
| Sponsor fee | Only if the address is new or has no USDC trustline **and** `usdGas` is `"0"` | Same as the ROZO bridge (about 0.44 USDC) |

`usdGas` default: `"0.5"` if the address is new or has no USDC trustline; `"0"` if it already has a USDC trustline. Set it yourself to override. The smallest USDC delivery is 0.01.

| You pay (Base) | Address | `usdGas` | You get |
| --- | --- | --- | --- |
| 1 USDC | New | `"0.5"` (default) | 1.6 XLM + about 0.49 USDC, account and trustline ready |
| 10 USDC | New | `"0.5"` (default) | 1.6 XLM + about 9.49 USDC |
| 10 USDC | New | `"0"` | about 9.55 USDC (sponsor fee charged) |
| 10 USDC | Has USDC trustline | `"0"` (default) | about 9.99 USDC, no signature |

The quote is authoritative: read `fees` and `totals` from it.

## Step by step: 10 USDC on Ethereum to a new Stellar address

No `X-API-Key`. Replace `GABC...XYZ` with the receiving G-address. Send a normal `User-Agent` header: some default library user agents are refused.

```bash
BASE=https://intentapiv4.rozo.ai/functions/v1/payment-api
UA="User-Agent: my-app/1.0"
ADDR=GABC...XYZ        # Stellar G-address that receives the funds

# 1. Quote: 10 USDC on Ethereum -> USDC on Stellar (usdGas omitted = default)
curl -s -X POST $BASE/funding/quotes -H "Content-Type: application/json" -H "$UA" -d '{
  "mode": "stellar_onboarding",
  "reserveMode": "sponsored",
  "source": { "chainId": "1", "assetId": "erc20:0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "amount": "10.00" },
  "outputs": [{ "id": "stable", "kind": "stable", "chainId": "1500",
    "assetId": "stellar:USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
    "receiverAddress": "'$ADDR'", "allocation": "remainder" }]
}'
# -> quoteId, planDigest, usdGas, gasAmount, fees, totals, expiresAt

# 2. Order (within 10 minutes of the quote)
curl -s -X POST $BASE/funding/orders -H "Content-Type: application/json" -H "$UA" \
  -H "Idempotency-Key: my-order-0001" \
  -d '{ "quoteId": "<quoteId>", "planDigest": "<planDigest>", "orderId": "my-order-0001" }'
# -> fundingId, deposit.address (0x...), deposit.amount, deposit.payBefore

# 3. Pay: send exactly deposit.amount of USDC or USDT to deposit.address
#    on Base, Ethereum, Arbitrum or Polygon, before payBefore.

# 4. Poll until pendingActions contains sign_stellar_onboarding (or status is completed)
curl -s $BASE/funding/orders/<fundingId> -H "$UA"

# 5a. Get the transaction to sign
curl -s -X POST $BASE/funding/orders/<fundingId>/signing-requests \
  -H "Content-Type: application/json" -H "$UA" -d '{ "walletAddress": "'$ADDR'" }'
# -> signingRequestId, xdr, operations, expiresAt

# 5b. Submit the signed transaction (this is the claim)
curl -s -X POST $BASE/funding/signing-requests/<signingRequestId>/submit \
  -H "Content-Type: application/json" -H "$UA" -d '{ "signedXdr": "<signed xdr>" }'

# 6. Poll the order until status is completed
curl -s $BASE/funding/orders/<fundingId> -H "$UA"
```

With `usdGas` omitted, a new address gets 1.6 XLM and about 9.39 USDC (10 minus 0.50 for XLM and opening, minus the 0.10 Ethereum bridge fee).

Timing:

- A quote is valid for 10 minutes. `deposit.payBefore` is the quote's expiry, so create the order and pay promptly.
- The signature request usually appears a few minutes after the payment (Ethereum takes longer to confirm). Poll every 10 seconds.
- A signing request is valid for up to 5 minutes (`expiresAt`). If it expires, call step 5a again for a new one.

Retrying the order with the same `Idempotency-Key` and body returns the same order. The deposit address is one-time and the same on all four chains.

## What a real order returns

These are the responses of a real 1 USDC order on Base to a new address (2026-10-12), read back afterwards with the GET endpoints. Ids, addresses and hashes are shortened; long fields are trimmed (`...`).

**Quote** (`POST /funding/quotes`, also `GET /funding/quotes/{quoteId}`):

```json
{
  "quoteId": "49fedc82-...",
  "planDigest": "16a06871...",
  "mode": "stellar_onboarding",
  "appId": "rozoNativeGas",
  "usdGas": "0.5",
  "gasAmount": "1.6",
  "gasAsset": "XLM",
  "gasDefaulted": true,
  "expiresAt": "2026-10-12T21:06:15.773Z",
  "source": { "chainId": "8453", "symbol": "USDC", "amount": "1", "priceUsd": "0.999734", "valuationUsd": "0.99" },
  "legs": [
    { "outputId": "native", "kind": "native", "symbol": "XLM", "receiverAddress": "GAGZ4L...WHQ4",
      "minimumAmount": "1.6", "budgetUsd": "0.50",
      "stellar": { "totalXlm": "1.6", "reserveXlm": "0", "spendableXlm": "1.6", "actionKind": "onboarding_template" } },
    { "outputId": "stable", "kind": "stable", "symbol": "USDC", "receiverAddress": "GAGZ4L...WHQ4",
      "minimumAmount": "0.4898642", "principalUsd": "0.48" }
  ],
  "fees": [ { "kind": "bridge_fee", "usd": "0.01", "refundable": true, "appliesTo": "stable" } ],
  "totals": {
    "sourceValueUsd": "0.99", "nativeBudgetsUsd": "0.50", "stableDeliveryUsd": "0.48",
    "sharedFeesUsd": "0.01", "roundingRemainderUsd": "0.000001", "totalFeesUsd": "0.01"
  },
  "userActions": [
    { "kind": "pay_source", "dueBy": "2026-10-12T21:06:15.773Z" },
    { "kind": "sign_stellar_onboarding", "dueBy": null, "legIds": ["native", "stable"] }
  ]
}
```

**Order** (`POST /funding/orders`): `status` is `awaiting_payment`, `pendingActions` is `pay_source`, and the deposit to pay is:

```json
{
  "fundingId": "eac09c0c-...",
  "status": "awaiting_payment",
  "deposit": {
    "chainId": "8453",
    "assetId": "erc20:0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    "symbol": "USDC",
    "address": "0x3c7a92...c776",
    "memo": null,
    "amount": "1",
    "payBefore": "2026-10-12T21:06:15.773+00:00"
  }
}
```

After the payment, the order moved to `source_confirming`, then `action_required` with `sign_stellar_onboarding`.

**Signing request** (`POST /funding/orders/{fundingId}/signing-requests`). Check `operations` before you sign:

```json
{
  "signingRequestId": "4325eb4b-...",
  "fundingId": "eac09c0c-...",
  "templateVersion": "funding_onboarding_v1",
  "networkPassphrase": "Public Global Stellar Network ; September 2015",
  "xdr": "AAAAAgAAAAB7qgLS...",
  "txHash": "e681c291...",
  "expiresAt": "2026-10-12T21:18:44.000Z",
  "accountState": "missing",
  "operations": [
    { "index": 0, "type": "beginSponsoringFutureReserves", "summary": "ROZO sponsors the reserves of GAGZ4L...WHQ4" },
    { "index": 1, "type": "createAccount", "summary": "Create account GAGZ4L...WHQ4 (reserve sponsored)" },
    { "index": 2, "type": "changeTrust", "summary": "Add the official USDC trustline" },
    { "index": 3, "type": "endSponsoringFutureReserves", "summary": "End reserve sponsorship" },
    { "index": 4, "type": "claimClaimableBalance", "summary": "Claim 0.4898643 USDC" },
    { "index": 5, "type": "payment", "summary": "Pay the disclosed 0.0000001 USDC sponsor fee" },
    { "index": 6, "type": "payment", "summary": "Receive 1.6000000 XLM" }
  ]
}
```

With a paid `usdGas` option the sponsor fee is 0.0000001 USDC, the smallest amount the claim accepts. The submit call returned `confirmed` with the same transaction hash, and the final order was `completed` with both legs `confirmed`: 1.6 XLM and 0.4898642 USDC delivered.

## Variations

- **Address already has a USDC trustline**: no opening cost, no signature, `usdGas` defaults to `"0"`. Steps 1 to 4 only; the order completes by itself.
- **No XLM**: add `"usdGas": "0"` to the quote (a new address then pays the sponsor fee instead).
- **More XLM**: `"usdGas": "1"` gives 3.2 XLM.
- **Other chains**: change `source.chainId` and `assetId` from the table.

## How to sign and claim

**A. Secret key (agents, servers, scripts): full flow after payment**

```js
// npm i @stellar/stellar-sdk   (Node 18+)
import { Keypair, TransactionBuilder, Networks } from "@stellar/stellar-sdk";

const BASE = "https://intentapiv4.rozo.ai/functions/v1/payment-api";
const H = { "Content-Type": "application/json", "User-Agent": "my-app/1.0" };
const kp = Keypair.fromSecret(process.env.STELLAR_SECRET); // read from env, never hardcode

async function claim(fundingId) {
  // wait until the order asks for the signature
  for (;;) {
    const o = await (await fetch(`${BASE}/funding/orders/${fundingId}`, { headers: H })).json();
    if (o.status === "completed") return o;                       // trustline existed: nothing to sign
    if (o.pendingActions?.some(a => a.kind === "sign_stellar_onboarding")) break;
    await new Promise(r => setTimeout(r, 10_000));
  }
  const req = await (await fetch(`${BASE}/funding/orders/${fundingId}/signing-requests`, {
    method: "POST", headers: H, body: JSON.stringify({ walletAddress: kp.publicKey() }),
  })).json();
  const tx = TransactionBuilder.fromXDR(req.xdr, Networks.PUBLIC);
  tx.sign(kp);                                                     // do not modify the transaction
  await fetch(`${BASE}/funding/signing-requests/${req.signingRequestId}/submit`, {
    method: "POST", headers: H, body: JSON.stringify({ signedXdr: tx.toEnvelope().toXDR("base64") }),
  });
}
```

**B. Browser: let the user pick any Stellar wallet (Freighter, LOBSTR, xBull, Albedo, Hana, ...)**

```js
// npm i @creit.tech/stellar-wallets-kit   (v1.x)
import { StellarWalletsKit, WalletNetwork, allowAllModules, FREIGHTER_ID } from "@creit.tech/stellar-wallets-kit";

const kit = new StellarWalletsKit({
  network: WalletNetwork.PUBLIC,
  selectedWalletId: FREIGHTER_ID,
  modules: allowAllModules(),
});

// 1. connect: shows a wallet picker, the user can switch wallets here
let address;
await kit.openModal({
  onWalletSelected: async (option) => {
    kit.setWallet(option.id);
    ({ address } = await kit.getAddress());   // use this as receiverAddress in the quote
  },
});

// 2. after payment, when the order asks for the signature:
const req = await (await fetch(`${BASE}/funding/orders/${fundingId}/signing-requests`, {
  method: "POST", headers: H, body: JSON.stringify({ walletAddress: address }),
})).json();
const { signedTxXdr } = await kit.signTransaction(req.xdr, {
  address, networkPassphrase: WalletNetwork.PUBLIC,
});
await fetch(`${BASE}/funding/signing-requests/${req.signingRequestId}/submit`, {
  method: "POST", headers: H, body: JSON.stringify({ signedXdr: signedTxXdr }),
});
```

**C. Freighter only**: `import { signTransaction } from "@stellar/freighter-api"`, then `signTransaction(xdr, { networkPassphrase: "Public Global Stellar Network ; September 2015", address })` returns `{ signedTxXdr }`.

The submit call is the claim: in that one transaction the account is created, the USDC trustline is added, and the USDC and XLM arrive. `walletAddress` must be the address you quoted for, and only that address's signature on the exact transaction is accepted. Multisig accounts are not supported.

## Checklist for agents and integrators

- **Never pay twice.** Save `fundingId` and the order `Idempotency-Key` before paying. After a crash, resume by polling the order; do not create a new order for the same intent.
- **Keep `fundingId` private.** Without an API key it is the only handle to the order: anyone holding it can read the order.
- **Check before you sign.** Compare the signing request's `operations` with what you expect: your address, a USDC claim at least the quote's minimum, the XLM amount from `usdGas`. Refuse to sign anything else.
- **A new account with 0 XLM balance is fine.** Reserves are sponsored by ROZO, so readiness checks must not require a minimum XLM balance.
- **Quote first, pay second.** If the quote expired before the order, quote again. Pay before `payBefore`; a late payment is not delivered automatically and goes to manual handling.
- **Exact amounts.** Read output amounts from the quote; never assume fees.
- **Partial delivery is visible.** Each leg (USDC, XLM) has its own status and tx hash in the order. Show both to the user.
- **Mainnet only.** There is no testnet endpoint today; test with 1 USDC orders.

## Good to know

- Pay the exact amount. Underpayment, other chains (for example BSC) or other tokens are not delivered and need manual handling. Overpayment completes the order but the extra is not refunded automatically.
- If the user pays but never signs, the USDC waits in a claimable balance only that address can claim, for 30 days. After that ROZO reclaims it and the order is handled manually (refund on request).
- Never send to a deposit address after its order has expired. Request a new quote.

## Errors

Every error has the shape `{ "code", "message", "retryable", "nextAction", "correlationId" }`.

| Code | HTTP | Meaning |
| --- | --- | --- |
| `rate_limited` | 429 | Too many requests from your IP, retry later |
| `invalid_request` | 400 | Bad input, for example a `usdGas` value that is not allowed |
| `limit_exceeded` | 422 | Amount outside 1 to 1,000 USD, or above a daily limit |
| `quote_expired` | 410 | Request a new quote |
| `quote_consumed` | 409 | The quote already has an order; request a new quote |
| `idempotency_conflict` | 409 | Same `Idempotency-Key` with a different body |
| `price_unavailable` | 503 | No valid price right now, retry later |
| `inventory_unavailable` | 409 | XLM temporarily out of stock, retry later or use `"usdGas": "0"` |
| `signer_unsupported` | 422 | Multisig or unsupported account |
| `template_expired` | 410 | The signing request expired, create a new one (step 5a) |
| `signature_invalid` | 422 | The signed transaction is not the one issued, create a new signing request |

## Reference

Order statuses, recovery and the shared error format are on the [Funding API overview](README.md). Full contract: [OpenAPI `openapi-funding-v1.2.0.yaml`](../../../docs/openapi-funding-v1.2.0.yaml).
