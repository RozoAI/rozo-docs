# ROZO Intents Technical Architecture Document

<sub>Updated: 2026-04-27</sub>

## 1. Summary

Today, Stellar users cannot easily pay for AI tokens. There is no direct path from Stellar USDC to OpenRouter, Claude, Gemini, ChatGPT, or other AI providers. This is the friction ROZO Intents removes.

ROZO Intents is a permissionless payment layer that lets Stellar USDC users pay for any AI service tokens via OpenRouter, and 485+ other agentic-economy services on Tempo and adjacent networks, without leaving the Stellar ecosystem and without any AI provider needing to integrate Stellar.

The system extends ROZO's Stablecoin Abstraction API (Hacken-audited with 1,032 users, $7.39M+ volume on Stellar) with three new components:

- [Hacken security audit](https://hacken.io/audits/rozo/sca-rozo-sdf-audit-mar2026/)
- [Dune dashboard (live)](https://dune.com/rozointents/stellar)


1. **Intent Extraction Layer**: parses AI provider invoices and checkout flows into a structured Stellar payment intent
2. **Settlement Adapter**: translates a Stellar USDC payment into a Coinbase-Commerce-acceptable USDC settlement on the destination chain (no provider-side change)
3. **Rewards**: a utility cashback issued to users, redeemable on the next purchase, funded by AI-provider referral commissions

All of it runs on Stellar mainnet. No provider partnership required. No bridge for the user to operate.

---

## 2. System Architecture

<img src="assets/permissionlesspay.png" alt="Permissionless Pay architecture" width="1400" style="max-width: 100%;">


### 2.1 Component Overview

```
  Stellar User (LOBSTR / Freighter / StellarExpert)
        │  paste invoice URL  /  natural-language ("buy $100 OpenRouter credits")
        ▼
  ROZO Intents UI  ──►  Intent Extraction Layer (NEW)
                              │  user signs once
                              ▼
                    Stablecoin Abstraction API (existing)
                              │
                              ▼
                    Settlement Adapter (NEW)
                              │
                ┌─────────────┴──────────────┐
                ▼                            ▼
       AI provider credited         Rewards Issuer (NEW)
       via Coinbase Commerce        cashback to user
```

### 2.2 Components

| Component | Status |
|---|---|
| Stablecoin Abstraction API (Stellar↔Base sub-second settlement) | ✅ Production, Hacken-audited |
| Soroban PayIn / PayOut contracts | ✅ Production |
| Passkey C-address wallet | 🆕 To build |
| Solver / liquidity routing | ✅ Production |
| Public Dune dashboard + Hacken audit report | ✅ Live |
| Intent Extraction Layer | 🆕 To build |
| Settlement Adapter (Coinbase Commerce path) | 🆕 To build |
| On-chain Rewards token + redemption flow | 🆕 To build |
| Wallet-embedded AI purchase flow (LOBSTR, Freighter, etc) | 🆕 To build |


---

## 3. Why This Architecture Is Permissionless

The unlock: OpenRouter and most AI providers already accept crypto via Coinbase Commerce. Their checkout flow exposes a unique pay-to address + amount on a chain Coinbase Commerce supports — the address itself is what correlates the payment to the order. They don't care who pays or how, as long as the funds settle to that address.

What ROZO does:
- Parse the Coinbase Commerce checkout (or the invoice URL the user pastes) into a structured intent
- On the Stellar side, take USDC from the user
- On the destination side (Base, ETH, etc.), settle the matching amount to Coinbase Commerce's endpoint
- Confirm settlement back to the user, deliver Rewards

The integration scales horizontally — every new AI service that accepts Coinbase Commerce becomes payable from Stellar without new provider work

---

## 4. Detailed Component Design

### 4.1 Intent Extraction Layer

Takes user input (URL, natural-language, or wallet deeplink) and produces a verified, structured `PaymentIntent`.

```typescript
interface PaymentIntent {
  source: { chain: "stellar"; asset: "USDC"; account: StellarAddress };
  destination: {
    provider: "openrouter" | "anthropic" | "openai" | string;
    chain: "base" | "ethereum" | string;
    asset: "USDC";
    address: EVMAddress;
    amount: BigInt;
    memo?: string;
    expiresAt: ISOString;
  };
  metadata: { invoiceUrl?: string; rewardsBps: number; ... };
  validation: { providerAllowlisted: boolean; coinbaseCommerceVerified: boolean; ... };
}
```

Extraction sources:
1. **URL paste** — fetch the public Coinbase Commerce charge, extract `{payTo, amount, chain}`, verify `NEW` status
2. **Natural-language** — LLM parses to a known provider's top-up; structured intent always shown for human confirmation before signing
3. **Wallet deeplink** — partner SDK constructs the intent client-side, no parsing needed

Safety: provider allowlist (hash-pinned), per-tx ceiling ($1,000 default), charge-status check, exact pay-to address preserved end-to-end. On expiry / 4xx / mis-parse / user edit → re-validate and re-confirm.

### 4.2 Settlement Adapter

After the user signs on Stellar, the solver makes an ERC-20 USDC `transfer()` call to the AI provider's unique Coinbase Commerce pay-to address on the destination chain, exact amount.

```
User signs → USDC locked in Soroban PayIn → solver calls USDC.transfer(payTo, amount)
on Base → Coinbase Commerce confirms PAID → provider credits user →
ROZO mints Rewards on Stellar → solver liquidity rebalanced
```

- **Speed:** 95% < 10s end-to-end (existing #38 SLA); destination-chain confirmation dominates latency
- **Liquidity:** reuses existing #38 solver pool — no new LP capital needed for Tranche 1 / 2
- **Risk:** ROZO is exposed between Stellar lock and EVM confirmation; mitigated by per-tx ceiling + circuit breaker (existing #38 infra, Hacken-audited)

### 4.3 Rewards

A Stellar Classic asset with a Soroban-controlled issuer for programmatic mint/burn — visible by default in any Stellar wallet via trustline, tradeable on Stellar DEX with no wrapping.

**Mint:** on confirmed purchase, mint `floor(purchaseUsd × rewardsBps / 10000)` to user; event emits `purchaseId` for the dashboard.

**Redeem:** at checkout, user opts to use Rewards. Burn `min(balance, purchaseUsd)`, discount the USDC settled to Coinbase Commerce, ROZO covers the gap from referral revenue.

**Sybil resistance:** per-purchase rate (not per-account), $1 minimum purchase, redemption binds to a real purchase, dashboard abuse monitoring.

### 4.4 Wallet Integration (Tranche 2)

Extends the existing #38 SDK with `payAiService(intent)`, a wallet-side UI primitive showing intent + Rewards preview, webhook hooks for "purchase complete" notifications, and a partner-onboarding flow (< 1 week kickoff to live). We are not building wallets — we are giving wallets a single SDK call to add AI-purchase as a feature.

---

## 5. Data Flows & State Machines

### 5.1 Happy Path: Pay $100 of OpenRouter via paste

```
t=0     User pastes OpenRouter Coinbase Commerce charge URL
t=0.2s  ROZO parses charge → { payTo, chain: base, USDC, $100 }
t=0.4s  UI shows intent: "Pay $100 USDC → OpenRouter, earn 500 Rewards (5%)"
t=Xs    User signs Stellar tx → USDC locked in Soroban PayIn
t=X+2s  Solver calls USDC.transfer(payTo, $100) on Base
t=X+5s  Coinbase Commerce sees PAID → OpenRouter credits user
t=X+6s  ROZO mints 500 Rewards to user on Stellar
t=X+7s  UI: "Done. $100 credited. 500 Rewards added."
```

Total user-perceived latency: 7 seconds, dominated by destination-chain confirmation.

### 5.2 Edge Cases & Mitigations

| Edge case | Handling |
|---|---|
| Charge expires after parse, before user confirms | Re-fetch on confirm click; if expired, show "this invoice expired, please get a new one" with a prefilled retry |
| User has insufficient Stellar USDC | Pre-flight balance check; offer one-click bridge from Base USDC via existing #38 path |
| Settlement Adapter fails on destination chain (gas spike, RPC failure) | Solver retries with exponential backoff; if N retries fail, refund user's Stellar USDC from PayIn lock (existing #38 mechanism) |
| Coinbase Commerce charge confirms but provider doesn't credit user | Record dispute; user-facing support flow; ROZO pursues via Coinbase Commerce dispute mechanics — tracked publicly on dashboard |
| Rewards mint fails (Soroban contract reverts) | Settlement is independent of Rewards mint; user's purchase still completes; Rewards mint retried via batch backfill within the hour |
| User edits the parsed intent | Treated as a new intent; full re-validation + re-confirm |
| Provider not on allowlist | UI shows a clear "we don't recognize this provider — paying anyway is at your own risk" gate; user explicit opt-in |
| Sybil attempts mass-mint Rewards via tiny purchases | Per-purchase minimum + per-account-per-window rate-limit + dashboard abuse monitoring |

---

## 6. Stellar-Specific Design Choices

This is an Open Track submission — a few choices are deliberately Stellar-native:

1. Settlement on Stellar mainnet, not Base. ROZO's #38 already settles cross-chain in seconds. The user's *experience* is Stellar-native: they sign on Stellar, their balance moves on Stellar, their Rewards live on Stellar, they see the result in their Stellar wallet. Base is invisible to the user.

2. Rewards as a Stellar-native asset (not an ERC-20). This means existing Stellar wallets (LOBSTR, Freighter, StellarExpert) display the asset by default after trustline, no Soroban-specific UI needed. It's also tradeable on Stellar DEX from day one — letting users who don't want to spend Rewards on AI services route them to liquidity instead.

3. Soroban for the issuer + redemption logic. Programmable mint/burn, event emission for the public dashboard, upgrade path for redemption-rule changes.

4. Coinbase Commerce as the bridge, not a custom relayer. Coinbase Commerce is the publicly-supported crypto checkout used by hundreds of merchants beyond AI — once we ship this for AI, the same architecture extends to any Coinbase-Commerce-accepting merchant. This is what "permissionless integration" buys us long-term: AI is the wedge, Stellar→Coinbase-Commerce is the durable infra.

5. Reuse of existing partner network — wallets (LOBSTR, Freighter) and ecosystem partners (Mykobo, Defindex, Soroswap). Wallet integration in Tranche 2 is BD-light because the relationships already exist — we are activating, not negotiating.

---

## 7. Security & Risk

| Risk | Mitigation |
|---|---|
| Settlement adapter exposed between Stellar lock and EVM confirmation | Per-tx and per-window ceilings; circuit breaker; existing #38 risk model + Hacken audit |
| Compromised provider allowlist (someone publishes a fake "OpenRouter" Coinbase Commerce charge) | Allowlist hash-pinned + signed updates; user-side warning if address not on allowlist; manual review for new providers |
| Rewards-token securities exposure | Utility-token design (only redeemable for service discount); no public sale; documented compliance review before mainnet |
| Solver liquidity drain (high-volume window) | Existing #38 throttling + replenishment; LP capital pool from #38 |
| LLM intent-parser hallucination on natural-language input | Parsed intent always shown structurally before signing; LLM never authorizes signing; allowlist gates destination |
| Provider-side credit failure post-settlement | Public dispute tracking; refund pathway via Coinbase Commerce |
| Stellar mainnet asset issuance compliance | Stellar Asset Sandbox listing; standard trustline + transfer-server posture |

The new Tranche 3 components (Rewards issuer + redemption) will be submitted to Audit Bank at Tranche 3 completion per SCF policy.

---

## 8. References

- [ROZO production data (live)](https://dune.com/rozointents/stellar)
- [Hacken security audit (March 2026)](https://hacken.io/audits/rozo/sca-rozo-sdf-audit-mar2026/)
- [ROZO website](https://rozo.ai/)
- [ROZO GitHub](https://github.com/rozoai)
- [SCF #38 award page](https://communityfund.stellar.org/projects/recN7Zf3kGBRIHVQy)
- [Coinbase Commerce documentation](https://commerce.coinbase.com/docs)
- [Stellar Asset Sandbox](https://www.stellar.org/asset-sandbox)

---
