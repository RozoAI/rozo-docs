---
description: >-
  stellar_onboarding: a new or not yet ready Stellar account gets a USDC
  trustline, USDC and optional spendable XLM with one payment and one user
  signature. Available to approved apps.
---

# Stellar Wallet Onboarding (`stellar_onboarding`)

{% hint style="info" %}
**Available to approved apps.** The mode is enabled per app and needs an API key: the signing step must be tied to the app that created the order, so the keyless public app does not offer it. Check `GET /funding/capabilities`: `stellar_onboarding` must show `supported`. Ask the ROZO team to enable it for your app.
{% endhint %}

## Pricing and limits

| Item | Value |
| --- | --- |
| Account opening fee | **0.50 USDC per order**, taken from the USDC output. It covers the account and trustline reserves ROZO sponsors. |
| Address already has a USDC trustline | No claimable balance and **no signature**: the USDC is sent directly and the opening fee is not charged. |
| XLM output (optional) | 1 to 2 USD per order, about 5 % spread. |
| Source payment | 1 to 20 USD in Base USDC. |

Always read the live values from the quote: `fees` and `totals` are authoritative, this table is not.

For a user whose Stellar account does not exist yet, or exists without a USDC trustline. The user pays one stablecoin deposit on a supported chain and, after it is confirmed, signs **one** Stellar transaction that:

1. (if the account is new) creates the account with its reserve **sponsored by ROZO**,
2. adds the official USDC trustline (sponsored),
3. claims the USDC that ROZO set aside for this order,
4. pays the disclosed sponsor fee in USDC,
5. (optional) receives spendable XLM.

Everything above lands in **one Stellar transaction**: either all of it happens or none of it does.

ROZO never adds a trustline on the user's behalf without that signature, and never sees the user's secret key.

## 1. Prove control of the address (no funds)

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/ownership/challenges \
  -H "X-API-Key: $ROZO_API_KEY" -H "Content-Type: application/json" \
  -d '{ "chainId": "1500", "address": "<user G-address>", "userRef": "user-123" }'
```

The response has a server-built `message`, `challengeId` and `expiresAt`. The user signs the exact message with their wallet's SEP-53 message signing (`signatureScheme: sep53`). This signature does not authorize any payment. Then:

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/ownership/verify \
  -H "X-API-Key: $ROZO_API_KEY" -H "Content-Type: application/json" \
  -d '{ "challengeId": "<challengeId>", "signature": "<base64 signature>" }'
```

You receive a short-lived `ownershipProofId` bound to your app, `userRef`, address and purpose. A challenge can be verified once. A client-side "verified" flag is never accepted.

## 2. Quote

```json
{
  "mode": "stellar_onboarding",
  "userRef": "user-123",
  "ownershipProofId": "<ownershipProofId>",
  "signerProfileId": "<supported wallet profile from capabilities.stellar.signerProfiles>",
  "signerPreflight": { "passed": true, "checkedAt": "<ISO time of your in-browser wallet check>" },
  "reserveMode": "sponsored",
  "source": { "chainId": "8453", "assetId": "<Base USDC assetId>", "amount": "10.00" },
  "outputs": [
    { "id": "stable", "kind": "stable", "chainId": "1500", "assetId": "<Stellar USDC assetId>", "receiverAddress": "<user G-address>", "allocation": "remainder" },
    { "id": "native", "kind": "native", "chainId": "1500", "receiverAddress": "<same G-address>", "allocationUsd": "1.00" }
  ]
}
```

* The XLM output is optional and must go to the same address.
* With the sponsored reserve, all XLM the user buys is spendable; the quote shows the sponsor fee separately.
* Multisig accounts are not supported (`signer_unsupported`).

## 3. Order, deposit, then sign

Create the order and have the user pay the deposit as in [Buy Gas Tokens](buy-gas-tokens.md#2-create-the-order). After confirmation the order moves to `action_required` with a `sign_stellar_onboarding` action:

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/orders/<fundingId>/signing-requests \
  -H "X-API-Key: $ROZO_API_KEY" -H "Content-Type: application/json" \
  -d '{ "walletAddress": "<user G-address>", "signerProfileId": "<profile>" }'
```

The response holds the unsigned `xdr`, its `txHash`, `templateVersion`, a human-readable `operations` list and `expiresAt` (a few minutes). Pass the XDR only to the user's wallet, then submit what the wallet returns:

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/signing-requests/<signingRequestId>/submit \
  -H "X-API-Key: $ROZO_API_KEY" -H "Content-Type: application/json" \
  -d '{ "signedXdr": "<signed envelope>" }'
```

ROZO checks the signed transaction is byte-for-byte the issued template (any changed operation, amount, fee or timebound is refused), adds its own signatures and submits it. `submitted` is not delivery: keep polling the order until both legs are `confirmed`.

If the request expired, the account changed, or the user declined, call `signing-requests` again: you get a new request with a new hash. An old signature never carries over. The user's USDC stays reserved for the order until the claim window ends; ROZO handles anything not claimed in time through recovery.
