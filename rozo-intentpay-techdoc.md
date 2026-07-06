# ROZO Intent Pay Tech Doc

<sub>Updated: 2026-05-08</sub>

## Update Notes — 2026-05-08

This revision deepens the technical architecture:

* Added deterministic invoice-resolution details, using OpenRouter/Coinbase Commerce as the first implementation and keeping the same pattern extensible to future invoice sources such as Stripe invoices.
* Added ROZO-owned LP inventory and asynchronous Stellar USDC → Base USDC rebalance, so checkout latency is optimized for payment SLA rather than bridge finality.
* Expanded failure modes to cover malformed invoices, expired charges, partial payments, duplicate submissions, LP insufficiency, network errors, provider delays, bridge/rebalance delays, and refund paths.
* Clarified Rewards/cashback as a lightweight account-based discount flow for now, kept separate from the core payment settlement path.

## 1. Summary

Today, Stellar users cannot easily pay for AI tokens. There is no direct path from Stellar USDC to OpenRouter, Claude, Gemini, ChatGPT, or other AI providers. This is the friction ROZO Intents removes.

ROZO Intents is a permissionless payment layer that lets Stellar USDC users pay for any AI service tokens via OpenRouter, and 485+ other agentic-economy services on Tempo and adjacent networks, without leaving the Stellar ecosystem and without any AI provider needing to integrate Stellar.

The system builds on ROZO's existing SCF #38 Stablecoin Abstraction API and adds three new components:

1. **Intent Extraction Layer**: parses AI provider invoices and checkout flows into a structured Stellar payment intent
2. **Settlement Adapter + Liquidity Layer**: translates a Stellar USDC payment into a Coinbase-Commerce-acceptable USDC settlement on the destination chain, using ROZO-owned liquidity so the user does not wait for bridge finality
3. **Rewards**: a lightweight cashback/discount system for repeat purchases, implemented separately from the core payment settlement path

All of it runs from a Stellar-native user experience. No provider partnership required. No bridge for the user to operate.

Existing SCF #38 infrastructure references:

* [Hacken security audit](https://hacken.io/audits/rozo/sca-rozo-sdf-audit-mar2026/)
* [Dune dashboard (live)](https://dune.com/rozointents/stellar)

***

## 2. System Architecture

<figure><img src=".gitbook/assets/permissionlesspay-vs.png" alt="Permissionless Pay architecture"><figcaption></figcaption></figure>

### 2.1 Component Overview

```
  Stellar user via dapp
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
       AI provider credited         Rewards Ledger / Issuer (NEW)
       via Coinbase Commerce        discount or cashback to user
```

### 2.2 Components

| Component                                                              | Status                       |
| ---------------------------------------------------------------------- | ---------------------------- |
| Stablecoin Abstraction API (Stellar↔Base sub-second settlement)        | ✅ Production, Hacken-audited |
| Soroban PayIn / PayOut contracts                                       | ✅ Production                 |
| ROZO settlement account for AI checkout                                | 🆕 To build                  |
| ROZO-owned LP inventory for Base-side advance                          | 🆕 To build                  |
| Passkey C-address wallet support                                       | 🆕 To build                  |
| Solver / liquidity routing                                             | ✅ Production                 |
| Public Dune dashboard + Hacken audit report for SCF #38 infrastructure | ✅ Live                       |
| Intent Extraction Layer                                                | 🆕 To build                  |
| Settlement Adapter (Coinbase Commerce + Base USDC path)                | 🆕 To build                  |
| Rewards / cashback design (account-based discount flow)                | 🆕 To build                  |
| Mobile-friendly dapp for AI purchase flow                              | 🆕 To build                  |

***

## 3. Why This Architecture Is Permissionless

The unlock: OpenRouter and most AI providers already accept crypto via Coinbase Commerce. Their checkout flow exposes a unique pay-to address, amount, asset, destination chain, charge status, and expiry. The unique charge address/reference is what correlates the payment to the order. They do not need to know that the user started from Stellar, as long as the exact funds settle to the Coinbase Commerce charge.

What ROZO does:

* Parse the Coinbase Commerce checkout (or the invoice URL the user pastes) into a structured intent
* On the Stellar side, receive USDC from the user into a ROZO settlement account
* On the destination side, use ROZO-owned LP inventory to settle the matching amount to Coinbase Commerce's Base USDC endpoint
* Rebalance Stellar USDC to Base USDC asynchronously after the provider-side payment is completed
* Confirm settlement back to the user, then apply Rewards/discounts where enabled

The integration scales horizontally — every new AI service that accepts Coinbase Commerce becomes payable from Stellar without new provider work

***

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
    reference?: string;
    expiresAt: ISOString;
  };
  metadata: {
    invoiceUrl?: string;
    coinbaseChargeId?: string;
    userCreditTarget?: string;
    rewardsBps?: number;
    ...
  };
  validation: {
    providerAllowlisted: boolean;
    coinbaseCommerceVerified: boolean;
    schemaVerified: boolean;
    referencePreserved: boolean;
    amountExact: boolean;
    ...
  };
}
```

Extraction sources:

1. **URL paste** — fetch the public Coinbase Commerce charge, extract `{payTo, amount, asset, chain, chargeId, expiresAt}`, verify `NEW` status
2. **Natural-language** — LLM parses to a known provider's top-up; structured intent always shown for human confirmation before signing
3. **Wallet deeplink** — partner SDK constructs the intent client-side, no parsing needed

#### General invoice resolution

The first implementation resolves OpenRouter invoices through Coinbase Commerce. The design is intentionally general: the same resolver pattern can support future invoice sources such as Stripe invoices, SaaS checkout pages, API top-up links, and other provider-issued payment URLs.

ROZO does not rely on an LLM to infer payment-critical fields.

1. Normalize the pasted URL and verify it matches an allowlisted OpenRouter/Coinbase Commerce pattern.
2. Fetch the Coinbase Commerce charge payload.
3. Verify charge status is payable, such as `NEW`, and re-fetch it again when the user clicks confirm.
4. Extract the exact destination chain, asset, pay-to address, amount, charge ID/reference, and expiry from the charge payload.
5. Validate the extracted data against the provider schema and per-transaction limits.
6. Display the structured intent to the user for confirmation.
7. If the user edits amount, address, reference, or provider target, discard the intent and restart validation.

For a future Stripe invoice integration, the provider adapter would follow the same pattern: fetch the invoice or payment intent from the provider source, extract exact amount, currency, invoice ID/reference, customer/payment target, status, and expiry, then produce the same internal `PaymentIntent` structure. The provider adapter changes; the ROZO intent, validation, wallet signing, liquidity settlement, and reconciliation flow remain the same.

Reference safety: the destination address and reference/charge ID are payment-critical fields. They are preserved from provider data end-to-end. The AI interface can explain the fields to the user, but it cannot infer, rewrite, repair, or invent them. On expiry / 4xx / malformed URL / schema mismatch / missing reference / user edit, ROZO blocks signing and asks the user to create or paste a fresh invoice.

Monitoring: the Intent Extraction Layer records parser success rate, provider fetch errors, schema validation failures, expired invoices, missing references, user edits, and blocked signing attempts. Alerts are triggered on abnormal failure rates or provider-specific parsing regressions, so ROZO can detect and fix invoice-resolution issues before they affect a large number of users.

### 4.2 Settlement Adapter

After the user signs on Stellar, ROZO verifies the Stellar USDC payment and then uses ROZO-owned LP inventory to make an ERC-20 USDC `transfer()` call to the AI provider's unique Coinbase Commerce pay-to address on Base, exact amount.

```
User signs → Stellar USDC received in ROZO settlement account →
ROZO verifies Stellar payment → ROZO LP calls USDC.transfer(payTo, amount) on Base →
Coinbase Commerce confirms PAID → provider credits user →
ROZO rebalances Stellar USDC to Base USDC asynchronously → Rewards/discount applied where enabled
```

* **Speed:** target payment-grade SLA measured in seconds; user does not wait for Stellar-to-Base bridge finality
* **Liquidity:** uses ROZO-owned prefunded LP inventory for provider-side payment advance
* **Rebalancing:** replenishes Base-side LP inventory asynchronously through the existing ROZO Intent API for Stellar USDC → Base USDC bridge/rebalance
* **Risk:** ROZO is exposed between Stellar payment verification, Base-side Coinbase Commerce payment, and later rebalance; mitigated by per-tx ceiling, LP inventory limits, circuit breakers, retry logic, and reconciliation monitoring

### 4.3 Liquidity Settlement and Rebalancing

ROZO Intent is the user-facing abstraction: the user says what they want to buy, ROZO turns that request or invoice into a verified payment intent, and the user signs once on Stellar. The Liquidity Layer is what makes that intent usable as real checkout. It removes the waiting time and operational uncertainty that would otherwise come from bridging or provider-side confirmation.

ROZO optimizes this flow for payments, not just bridging. For a $10 AI top-up, a usage-based API purchase, or a larger $10,000 invoice, it is not reasonable to make the user wait next to a computer for one or two minutes of bridge confirmation. Some external bridge/provider services can also halt or delay for hours. That may be acceptable for treasury movement, but it is not acceptable for financial checkout or micropayments.

To make intent payment feel like one-tap checkout, ROZO brings its own liquidity. For invoices under **$10,000**, the target is to confirm provider-side payment within seconds after Stellar payment verification, subject to risk controls and LP inventory availability. In practice, if a user pays $10,000 in Stellar USDC, ROZO can immediately pay the corresponding Base USDC amount to the provider from ROZO-owned liquidity, then use the ROZO Intent API in the background to bridge/rebalance Stellar USDC back to Base USDC. This lets ROZO provide payment reliability and success-rate guarantees without depending on third-party bridge timing for the user-facing checkout.

ROZO therefore separates user-side payment from provider-side settlement:

1. User pays Stellar USDC to the ROZO settlement account.
2. ROZO verifies the Stellar payment on-chain.
3. ROZO-owned LP inventory advances the Base USDC payment to the Coinbase Commerce charge, without waiting for Stellar-to-Base bridge completion.
4. Coinbase Commerce marks the charge paid and the AI provider credits the user.
5. ROZO asynchronously rebalances Stellar USDC to Base USDC through the ROZO Intent API to restore LP inventory.
6. The order records Stellar payment, Coinbase Commerce payment, LP advance, rebalance status, and final completion.

This makes the user-facing SLA measured in seconds while preserving an auditable reconciliation trail.

### 4.4 Rewards

Rewards are intentionally separated from settlement. A failed reward action must not block a successful AI purchase.

The initial implementation can be account-based Rewards for checkout discounts: after confirmed provider fulfillment, ROZO records `purchaseId`, user account, purchase amount, reward amount, and redemption status in the rewards ledger. On the next checkout, the user can apply Rewards as a discount, and ROZO reduces the required USDC amount or covers the discounted portion from program budget/referral revenue.

Reward events are still auditable at the order level: dashboard records can link purchase ID, purchase amount, reward amount, redemption status, and the Stellar payment that funded the order. If ROZO later enables a Stellar-native reward asset, the asset/issuer/trustline and redemption mechanics will be specified separately. They are not required for the core AI checkout settlement flow.

Sybil resistance: per-purchase rate, minimum purchase size, per-account/per-window caps, and abuse monitoring.

### 4.5 Wallet Integration

Extends the existing #38 SDK with `payAiService(intent)`, a wallet-side UI primitive showing intent + Rewards preview, webhook hooks for "purchase complete" notifications, and a partner-onboarding flow (< 1 week kickoff to live). We are not building wallets — we are giving wallets a single SDK call to add AI-purchase as a feature.

***

## 5. Data Flows & State Machines

### 5.1 Happy Path: Pay $100 of OpenRouter via paste

```
t=0     User pastes OpenRouter Coinbase Commerce charge URL
t=0.2s  ROZO parses charge → { payTo, chain: base, USDC, $100 }
t=0.4s  UI shows intent: "Pay $100 USDC → OpenRouter"
t=Xs    User signs Stellar tx → USDC received in ROZO settlement account
t=X+1s  ROZO verifies Stellar payment on-chain
t=X+2s  ROZO LP inventory calls USDC.transfer(payTo, $100) on Base
t=X+5s  Coinbase Commerce sees PAID → OpenRouter credits user
t=X+6s  ROZO records Rewards/discount eligibility where enabled
t=X+7s  UI: "Done. $100 credited."
t+async ROZO rebalances Stellar USDC → Base USDC and marks LP inventory restored
```

Total user-perceived latency target: seconds. Rebalance can complete asynchronously after checkout.

### 5.2 Order State Machine

```
created
-> parsed
-> user_confirmed
-> stellar_submitted
-> stellar_paid
-> lp_advanced
-> provider_fulfilled
-> bridge_pending
-> lp_rebalanced
-> completed
```

Failure states:

```
parse_failed
expired
user_rejected
stellar_failed
partial_payment
duplicate_payment
lp_insufficient
provider_pending
provider_failed
bridge_delayed
bridge_failed
refund_required
rewards_failed
```

### 5.3 Edge Cases & Mitigations

| Edge case                                                          | Handling                                                                                                                         |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Malformed invoice URL                                              | Reject before signing; show a retry prompt and ask the user to paste a fresh provider URL                                        |
| Coinbase Commerce charge fetch returns 4xx / 5xx                   | Do not create a payable intent; retry fetch where safe, otherwise ask user to refresh the invoice                                |
| Charge expires after parse, before user confirms                   | Re-fetch on confirm click; if expired, show "this invoice expired, please get a new one" with a prefilled retry                  |
| Missing or changed reference / charge ID                           | Block signing; payment-critical reference fields must be preserved from provider data                                            |
| User edits the parsed intent                                       | Treated as a new intent; full re-validation + re-confirm                                                                         |
| User has insufficient Stellar USDC                                 | Pre-flight balance check; offer one-click bridge from Base USDC via existing #38 path                                            |
| Partial Stellar payment                                            | Keep order in `partial_payment`; ask user to top up or initiate refund/manual review depending on amount and timeout             |
| Duplicate payment / duplicate submit                               | Idempotency key and charge ID prevent double settlement; duplicate Stellar payment is flagged for refund/manual review           |
| LP inventory insufficient                                          | Do not advance provider-side payment; throttle new orders and show retry timing until inventory is replenished                   |
| Settlement Adapter fails on Base (gas spike, RPC failure)          | Retry with exponential backoff; if retries fail, mark `provider_failed` / `refund_required` and reconcile the Stellar-side funds |
| Stellar Horizon/RPC/network failure                                | Do not mark `stellar_paid` until transaction can be independently verified; user sees pending/retry state                        |
| Bridge/rebalance delayed                                           | User purchase remains complete after provider fulfillment; LP inventory stays marked `bridge_pending` until rebalance completes  |
| Bridge/rebalance failed                                            | Retry alternate route or manual rebalance; no user action required unless refund is triggered before provider fulfillment        |
| Coinbase Commerce charge confirms but provider doesn't credit user | Record dispute; user-facing support flow; ROZO pursues via Coinbase Commerce dispute mechanics — tracked publicly on dashboard   |
| Rewards action fails                                               | Settlement is independent of Rewards; user's purchase still completes; Rewards are retried or backfilled                         |
| Provider not on allowlist                                          | UI shows a clear "we don't recognize this provider — paying anyway is at your own risk" gate; user explicit opt-in               |
| Sybil attempts to farm Rewards via tiny purchases                  | Per-purchase minimum + per-account-per-window rate-limit + dashboard abuse monitoring                                            |

***

## 6. Stellar-Specific Design Choices

A few choices are deliberately Stellar-native:

1. User experience on Stellar mainnet. The user signs on Stellar, pays Stellar USDC, and sees a Stellar-side payment record. Base is used for OpenRouter/Coinbase Commerce settlement behind the scenes, but the user does not operate the bridge or switch chains.
2. ROZO settlement account for checkout SLA. For the OpenRouter flow, Stellar USDC currently enters a ROZO settlement account. ROZO verifies that payment before advancing Base-side provider settlement from its own LP inventory.
3. Rewards as a separate checkout discount path. Rewards can start account-based for repeat-purchase discounts and dashboard reporting. This keeps rewards separate from payment settlement, so reward operations never block a successful AI purchase.
4. Coinbase Commerce as the permissionless merchant rail. Coinbase Commerce is the publicly-supported crypto checkout used by merchants beyond AI. Once ROZO ships this for OpenRouter, the same architecture extends to any Coinbase-Commerce-accepting merchant without requiring provider-side Stellar integration.

***

## 8. References

* [ROZO production data (live)](https://dune.com/rozointents/stellar)
* [Hacken security audit (March 2026)](https://hacken.io/audits/rozo/sca-rozo-sdf-audit-mar2026/)
* [ROZO website](https://rozo.ai/)
* [ROZO GitHub](https://github.com/rozoai)
* [SCF #38 award page](https://communityfund.stellar.org/projects/recN7Zf3kGBRIHVQy)

***
