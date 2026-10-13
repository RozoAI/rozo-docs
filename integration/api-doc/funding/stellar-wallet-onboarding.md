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
| Web page | People, no code | [intents.rozo.ai/stellar-wallet](https://intents.rozo.ai/stellar-wallet): connect any Stellar wallet, pick amount and chain, pay, sign once |
| MCP | AI agents (Claude Code, Codex, Cursor, ...) | Rozo MCP at `https://mcp.rozo.ai/mcp` with tools `funding_capabilities`, `stellar_wallet_quote`, `stellar_wallet_create_order`, `stellar_wallet_order_status`, `stellar_wallet_get_signing_request`, `stellar_wallet_submit_signed`. The MCP never holds keys: your agent's wallet pays and signs. See [Prompt for your agent](#prompt-for-your-agent) |

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
| Request rate | Per client IP, per 10 minutes: 30 quotes, 6 orders, 20 signing requests, 10 submits. Order reads are not limited (`429 rate_limited`) |

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

# 3. Pay once before payBefore, following deposit.amountPolicy.
#    exact (or absent): send deposit.amount. any_amount: read
#    minAcceptedAmount/maxPricedAmount; deposit.amount is suggested.
#    Use USDC or USDT on an enabled Base, Ethereum, Arbitrum or Polygon route.

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

No Stellar address yet? Create one locally first and keep the secret on that machine (never send it to any server, including ROZO):

```js
// npm i @stellar/stellar-sdk   (Node 18+), run once
import { Keypair } from "@stellar/stellar-sdk";
import { writeFileSync } from "node:fs";

const kp = Keypair.random();
writeFileSync("stellar-wallet.secret", kp.secret() + "\n", { mode: 0o600, flag: "wx" }); // never overwrites
console.log(kp.publicKey()); // the G-address: use it as receiverAddress
```

Then, after payment:

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

## Prompt for your agent

Have an AI coding agent (Claude Code, Codex, Cursor) open the wallet for you through the Rozo MCP. Connect it first, for example `claude mcp add --transport http rozo-checkout "https://mcp.rozo.ai/mcp?src=docs"`. The agent needs an EVM wallet it controls on the chosen chain, holding the USDC or USDT plus a little native gas, and Node 18+. The same prompt is in the [MCP README](https://github.com/RozoAI/rozo-checkout-mcp#prompt-for-your-agent-open-a-stellar-wallet).

Fill in the four inputs and paste:

```text
Open (or top up) a Stellar wallet for me with the rozo-checkout MCP tools.

Inputs:
- Receiving Stellar address: <G... address, or "generate a new one">
- Pay from: <base | ethereum | arbitrum | polygon>, USDC or USDT, from the EVM wallet you control
- Amount in USD: <1 to 1000>
- XLM tier (usdGas): <"0" = no XLM, "0.5" = 1.6 XLM, "1" = 3.2 XLM, or "default">

Safety rules (never break these):
- The Stellar secret key (S...) stays on this machine. Never print it, never pass it to any tool, API, MCP or server.
- Sign the XDR the server returns unchanged. Check its operations before signing; if anything looks wrong, stop and ask me.
- Pay once, before payBefore, exactly as deposit.amountPolicy says. Never send a second payment to fix a problem.

Steps:
1. New address only: generate the keypair locally with the Node code below. It saves the secret to
   ./stellar-wallet.secret (mode 600, refuses to overwrite). Tell me the file path and the G address.
   Make sure the file is not inside a git repo and ask me to back it up.
2. Call funding_capabilities. Stop if stellarOnboarding.status is not "supported". Check my amount is within
   sourceAssets minAmount/maxAmount and my XLM tier is one of gasOptions.options.
3. Call stellar_wallet_quote with receiverAddress, sourceChain, amountUsd (decimal string, e.g. "10") and
   usdGas (leave it out for "default"). Show me receives.usdcMinimum, receives.xlm, fees, totals,
   signatureNeeded and expiresAt. Wait for my yes. The quote is valid about 10 minutes.
4. Call stellar_wallet_create_order with quoteId, planDigest and a new orderId (8 to 128 chars of
   A-Z a-z 0-9 _ . : -, for example agent-stellar-20261013-0001). Save fundingId and orderId to a local file
   before paying. Keep fundingId private. If the call fails, retry with the same quoteId and orderId: it
   returns the same order, never a second one.
5. Pay: one ERC-20 transfer from my EVM wallet on the chosen chain to deposit.address. Use the USDC or USDT
   contract for that chain from deposit.acceptedTokens (both use 6 decimals). Amount: with amountPolicy
   "exact", send exactly deposit.amount; with "any_amount", send deposit.amount (anything from
   minAcceptedAmount up to maxPricedAmount is accepted and repriced). Send before deposit.payBefore.
   Check the token balance and native gas first. Pay on one chain only.
6. Call stellar_wallet_order_status every 15 seconds. source_confirming, funds_confirmed and executing
   mean the payment was seen: do not pay again. An address that already has a USDC trustline needs no
   signature and goes straight to completed.
7. When signatureNeeded is true (pendingActions has sign_stellar_onboarding), call
   stellar_wallet_get_signing_request with fundingId and the receiving G address. Before signing check:
   networkPassphrase is "Public Global Stellar Network ; September 2015"; the operations create or use
   my address, add the USDC trustline, claim USDC equal to the current stable leg minimumAmount from
   order status (it can differ from the quote after repricing) and pay me the XLM of my tier. Decode the
   XDR locally (code below) and confirm it matches the operations list.
8. Sign with the code below and call stellar_wallet_submit_signed with signingRequestId and the signed
   XDR. A signing request expires after about 5 minutes; if it expired or submit says failed, get a new
   signing request and sign again. Submitting the same signed XDR twice is safe.
9. Keep polling until status is "completed" (every leg confirmed). Report the USDC and XLM delivered
   and each leg's txHash.

If something goes wrong:
- expired_unpaid or cancelled_unpaid: nothing was lost. Quote again with a new orderId.
- recovery_required, a late or wrong payment, or a closed payment window after you paid: stop, do not
  pay again, and send the fundingId to hi@rozo.ai.
- rate_limited: wait a few minutes and retry once. Do not loop.

Node code (npm i @stellar/stellar-sdk), two small ES module files:

  // keygen.mjs (step 1, run once): node keygen.mjs
  import { Keypair } from "@stellar/stellar-sdk";
  import { writeFileSync } from "node:fs";
  const kp = Keypair.random();
  writeFileSync("stellar-wallet.secret", kp.secret() + "\n", { mode: 0o600, flag: "wx" });
  console.log(kp.publicKey()); // the G address: the only part you share

  // sign.mjs (steps 7 and 8). First run: node sign.mjs "<xdr>" prints the decoded operations only.
  // After they match, run: node sign.mjs "<xdr>" --sign to print the signed XDR.
  import { Keypair, TransactionBuilder } from "@stellar/stellar-sdk";
  import { readFileSync } from "node:fs";
  const networkPassphrase = "Public Global Stellar Network ; September 2015";
  const kp = Keypair.fromSecret(readFileSync("stellar-wallet.secret", "utf8").trim());
  const tx = TransactionBuilder.fromXDR(process.argv[2], networkPassphrase);
  console.error(tx.operations.map((op) => [op.type, op.destination ?? op.source ?? "", op.amount ?? "", op.asset?.code ?? op.line?.code ?? ""]));
  if (process.argv[3] !== "--sign") process.exit(0);
  tx.sign(kp); // signs the server transaction as is, nothing is changed
  console.log(tx.toXDR()); // signed XDR, base64: pass it to stellar_wallet_submit_signed
```

Through the MCP, rate limits count against the MCP server's outbound address, which other MCP users can share: on `rate_limited`, wait and retry later instead of looping.

## Checklist for agents and integrators

- **Never pay twice.** Save `fundingId` and the order `Idempotency-Key` before paying. After a crash, resume by polling the order; do not create a new order for the same intent.
- **Keep `fundingId` private.** Without an API key it is the only handle to the order: anyone holding it can read the order.
- **Check before you sign.** Compare the signing request's `operations` with what you expect: your address, the USDC amount in the current order's refreshed `legs[].minimumAmount`, and the unchanged XLM tier from `usdGas`. Refuse to sign anything else.
- **A new account with 0 XLM balance is fine.** Reserves are sponsored by ROZO, so readiness checks must not require a minimum XLM balance.
- **Quote first, pay second.** If the quote expired before the order, quote again. Pay before `payBefore`; a late payment is not delivered automatically and goes to manual handling.
- **Current output amounts.** Show the quote before payment. After payment, read the refreshed order: a valid smaller deposit can deliver less USDC than the original quote. Sign only the exact server-provided XDR for that order; do not modify its operations or amounts.
- **Partial delivery is visible.** Each leg (USDC, XLM) has its own status and tx hash in the order. Show both to the user.
- **Mainnet only.** There is no testnet endpoint today; test with 1 USDC orders.

## Good to know

- Read `deposit.amountPolicy`. With `exact` or an absent field, follow the quoted deposit amount; a short payment requires recovery and overpayment does not increase delivery. With `any_amount`, `deposit.amount` is suggested: a single on-time payment at or above `minAcceptedAmount` is repriced using frozen prices and fees. The quoted XLM tier stays unchanged and USDC adjusts after fees. A payment below the minimum cannot cover the tier, fees and minimum USDC output, so it requires recovery.
- `maxPricedAmount` is the per-order pricing ceiling. The remaining daily allowance can impose a lower ceiling. Only the amount that fits is delivered; the excess is held for manual handling, not automatically refunded. If the remaining allowance is below the deliverable minimum, nothing is delivered automatically. Unsupported chains (for example BSC), wrong assets, late payments and a second payment also require manual handling. Never send another payment to top up a short order.
- For a repriced order, `repricing` reports `quotedAmount`, `receivedAmount`, `pricedAmount`, `excessAmount` and `quotedPlanDigest`; otherwise it is `null`. The order's current `planDigest`, `legs`, `fees` and `totals` reflect the priced amount. For example, a 1 USDC quote paid with 0.80 USDC can keep its XLM tier and deliver less USDC if 0.80 meets the returned minimum; paying 1.30 can increase USDC if it fits the returned ceiling and daily allowance. Calculate the net amounts from the actual frozen plan, not these example numbers.
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
