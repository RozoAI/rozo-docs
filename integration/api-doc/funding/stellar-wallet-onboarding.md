---
description: >-
  stellar_onboarding: a new or not yet ready Stellar account gets a USDC
  trustline, USDC and optional spendable XLM with one user funding signature.
  Contract published; not yet available.
---

# Stellar Wallet Onboarding (`stellar_onboarding`)

{% hint style="danger" %}
**Not yet available.** The contract below is final (OpenAPI `1.0.0`), but capabilities report this mode as `disabled` with reason `executor_unavailable`, quotes are refused, and the signing endpoints answer `409 state_changed` / `404`. Build against it, but do not offer it to users until capabilities show `supported`.
{% endhint %}

For a user whose Stellar account does not exist yet, or exists without a USDC trustline. The user pays one stablecoin deposit on a supported chain and, after it is confirmed, signs **one** Stellar transaction that:

1. (if the account is new) creates the account with its reserve **sponsored by ROZO**,
2. adds the official USDC trustline (sponsored),
3. claims the USDC that ROZO set aside for this order,
4. pays the disclosed sponsor fee in USDC,
5. (optional) receives spendable XLM.

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
