---
description: >-
  native_and_stable: one stablecoin payment delivers a native gas token and a
  stablecoin, each tracked and confirmed separately. Gated beta.
---

# Gas + Stablecoin Funding (`native_and_stable`)

{% hint style="warning" %}
Gated beta. Read the [Funding API overview](README.md) first. Only combinations listed in `capabilities.routes` are available.
{% endhint %}

One deposit funds **two outputs**: a native gas token and a stablecoin (USDC where supported). They can be on the same chain or on two different supported chains, for example ETH on Arbitrum plus USDC on Stellar. Each output is its own leg with its own status and transaction hash. The order is `completed` only when **both** are confirmed.

## Quote

```bash
curl -s -X POST https://intentapiv4.rozo.ai/functions/v1/payment-api/funding/quotes \
  -H "X-API-Key: $ROZO_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "mode": "native_and_stable",
    "userRef": "user-123",
    "source": { "chainId": "8453", "assetId": "<Base USDC assetId>", "amount": "10.00" },
    "outputs": [
      { "id": "native", "kind": "native", "chainId": "42161", "receiverAddress": "<Arbitrum address>", "allocationUsd": "2.00" },
      { "id": "stable", "kind": "stable", "chainId": "1500", "assetId": "<Stellar USDC assetId>",
        "receiverAddress": "<ready Stellar G-address>", "allocation": "remainder", "minimumAmount": "7.00" }
    ],
    "limits": { "maxTotalFeesUsd": "1.00" }
  }'
```

* `allocationUsd` is the **total USD budget of the gas leg**: the coin itself plus that leg's own fees. It must respect the min, max and step in capabilities.
* The stable output takes the **remainder** after the gas budget and shared fees. Use `minimumAmount` to refuse a quote that would deliver less.
* Each leg shows `sourceAllocationAmount`: the part of the deposit backing it. If a leg can never be delivered, recovery is based on that frozen allocation, never on a new market price.

## Receivers

* Both receiver addresses, assets and amounts are frozen into the plan the user approves (`planDigest`). They cannot change after the deposit is paid.
* A Stellar USDC output needs an existing account **with** a USDC trustline. If the account is not ready, the quote fails with `stellar_account_not_ready` and `details.suggestedMode = stellar_onboarding`; it never switches mode silently.

## Create, pay, track

Identical to [Buy Gas Tokens](buy-gas-tokens.md#2-create-the-order): create with `Idempotency-Key`, pay the one-time deposit exactly, poll the order.

## When one output fails

The two outputs are delivered separately and are not atomic, even on the same chain. If one is confirmed and the other fails, the order becomes `recovery_required`:

```json
"recovery": {
  "state": "open",
  "reason": "leg_failed",
  "deliveredLegIds": ["<native leg>"],
  "owedLegIds": ["<stable leg>"]
}
```

The delivered output stays delivered. ROZO resolves only the owed output (re-delivery or a refund of that leg's allocation); nothing is refunded automatically, and a leg whose outcome is `unknown` is never re-sent or refunded until it is known.
