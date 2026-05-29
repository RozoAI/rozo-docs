---
description: >-
  ROZO CCTP Bridge. Native USDC bridging between Stellar and Base, Ethereum, and
  Solana — powered by Circle CCTP V2. Self-custody, no Rozo fee, ~30–120s.
icon: right-left
---

# CCTP Bridge

Move native **USDC** between **Stellar** and **Base, Ethereum, and Solana** in a single flow — no wrapped tokens, no Rozo custody. The bridge is built directly on **Circle's Cross-Chain Transfer Protocol (CCTP) V2**, so every transfer is a native burn-and-mint of canonical USDC, not a liquidity-pool swap.

Try it at [bridge.rozo.ai/cctp](https://bridge.rozo.ai/cctp).

## Why it's different

* **Self-custody, always.** Rozo's operator can never move or redirect your funds. On EVM chains each transfer routes through an immutable forwarder contract whose destination is locked at creation; on Stellar you sign a single atomic transaction; on Solana the burn goes straight to Circle's TokenMessenger. A compromised Rozo key still cannot take user funds.
* **Native USDC on both ends.** Circle CCTP burns USDC on the source chain and mints canonical USDC on the destination — no wrapped or bridged representations.
* **Fast.** Built on CCTP V2 **Fast Transfer**, most bridges complete in **~30–120 seconds**.
* **No Rozo fee (v1).** You only pay Circle's protocol fee (~1.3 bps). The minimum transfer is **1 USDC**.
* **Stellar `G…` and `C…` addresses** are both supported as destinations.

## Supported routes

Native USDC ↔ USDC, both directions, with **Stellar** on one side of every route:

| Route | Status |
|---|---|
| Base ↔ Stellar | Live |
| Ethereum ↔ Stellar | Live |
| Solana ↔ Stellar | Live |

## How it works

**To Stellar** (e.g. Base → Stellar)

1. You send USDC to a unique deposit address (EVM), or sign one transaction (Stellar/Solana source).
2. Circle attests the burn.
3. Rozo relays the mint, and native USDC lands on your Stellar address.

**From Stellar** (e.g. Stellar → Base)

1. You sign one transaction in your Stellar wallet to burn USDC.
2. Circle attests the burn.
3. Rozo relays the mint to your address on the destination chain.

Either way, Rozo only sponsors gas and relays the message — it never holds your USDC.

## Good to know

* Send only to **self-custody wallets**. Exchange deposit addresses that require a memo are not supported yet.
* When bridging **to Stellar**, make sure the destination account already has a **USDC trustline**.
* CCTP attestations are valid for ~24 hours. If one expires before the mint lands, it can be re-attested from Circle.
