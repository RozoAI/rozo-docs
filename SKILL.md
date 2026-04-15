---
name: rozo-docs
description: >
  Route a user's natural-language question about ROZO to the correct doc page
  or executable skill. Use when a user asks about cross-chain payments,
  bridging, earning yield, EURC onramp, wallet deposits, the Intent Pay SDK,
  the Intent API, supported chains/tokens, fees, smart-contract addresses,
  audits, or agentic payments (MPP Router, x402). Also routes to the
  `rozo-intents` and `stellar-agent-wallet` plugin skills when the user wants
  to actually send a payment, check a balance, parse a QR, or call a paid API.
  Do NOT use for general blockchain questions unrelated to ROZO.
---

# ROZO — Intent Routing

ROZO is the Visa for Stablecoins. Users and developers express an intent
("pay $3.25 for boba", "bridge USDC from Base to Stellar", "earn 10% APY");
ROZO handles routing, bridging, fees, and settlement across Ethereum,
Arbitrum, Base, BSC, Polygon, Solana, and Stellar.

This skill is the entry point for doc-based questions. If the user wants to
*execute* a payment, delegate to the relevant plugin skill (see the
executable skills table below).

## Routing — user intent → where to go

### Doc routing (informational questions)

| User asks about | Send them to |
|-----------------|--------------|
| "What is ROZO / how does it work" | https://docs.rozo.ai/ and https://docs.rozo.ai/start/litepaper |
| "Vision, mission, philosophy" | https://docs.rozo.ai/start/vision-and-missions |
| "Send / pay / transfer USDC cross-chain" | https://docs.rozo.ai/products/intent-based-payment-transfer |
| "Bridge USDC / USDT across chains" | https://docs.rozo.ai/products/intent-based-bridge |
| "Earn yield on idle stablecoins" | https://docs.rozo.ai/products/intent-based-earn |
| "Let my users deposit from any chain" | https://docs.rozo.ai/products/intent-based-deposit |
| "EURC onramp from bank / bridge EURC from Base" | https://docs.rozo.ai/products/eurc-onramp/ |
| "Agentic payments / MPP Router / x402 / pay-per-call" | https://docs.rozo.ai/products/agentic-payments-mpprouter |
| "Mobile app / dApp integration" | https://docs.rozo.ai/products/mobile-app/ |
| "How do I integrate (React drop-in)" | https://docs.rozo.ai/integration/rozointentpay/quick-start |
| "How do I integrate (REST API)" | https://docs.rozo.ai/integration/api-doc/api-quick-start |
| "SDK method reference" | https://docs.rozo.ai/integration/rozointentpay/api-reference |
| "Tech design of the intent system" | https://docs.rozo.ai/integration/api-doc/rozo-intents-tech-design |
| "Supported chains and tokens" | https://docs.rozo.ai/integration/api-doc/supported-tokens-and-chains |
| "Wallet top-up via API" | https://docs.rozo.ai/integration/api-doc/api-for-advanced-used/wallet-topup |
| "Get fees / quote before payment" | https://docs.rozo.ai/integration/api-doc/api-for-advanced-used/get-fees |
| "Stellar Soroban smart-account payments" | https://docs.rozo.ai/integration/api-doc/api-for-advanced-used/stellar-contract-payments |
| "Contract addresses / audit reports" | https://docs.rozo.ai/contact/contracts-and-audits |
| "FAQs" | https://docs.rozo.ai/contact/faqs |
| "Media kit / brand assets" | https://docs.rozo.ai/contact/media-kit/ |
| "Troubleshooting an integration" | https://docs.rozo.ai/integration/rozointentpay/troubleshooting |
| "AI agent prompts for the SDK" | https://docs.rozo.ai/integration/rozointentpay/ai-prompts |
| "Live API reference (Postman)" | https://apidoc.rozo.ai/ |

### Executable routing (actions, not questions)

When the user wants to *do* something, route to a plugin skill instead of a
doc page:

| User wants to | Use skill |
|---------------|-----------|
| Send a cross-chain payment | `rozo-intents:send-payment` |
| Check wallet balance across chains | `rozo-intents:check-balance` |
| Parse a payment QR code / URI | `rozo-intents:parse-qr` |
| Check the status of a payment | `rozo-intents:payment-status` |
| Bridge from Stellar to another chain | `stellar-agent-wallet:bridge` |
| Swap XLM → USDC or add a USDC trustline on Stellar | `stellar-agent-wallet:check-balance` |
| Call a 402-gated API and pay with Stellar USDC | `stellar-agent-wallet:pay-per-call` |
| Discover MPP Router paid API services | `stellar-agent-wallet:discover` |
| Send payment from Stellar USDC to any chain | `stellar-agent-wallet:send-payment` |

## API quick reference

- Intent API: `https://intentapiv4.rozo.ai` — public, rate-limited, AppID required
- Balance API: `https://api-balance.rozo-deeplink.workers.dev` — public, rate-limited
- Create payment: `POST /create-payment` (supports dryrun for fee estimates)
- Get payment: `GET /payment/{id}` — accepts UUID, tx hash, or deposit address + memo
- Amount limits: $0.01 minimum, $10,000 maximum
- Token preference: auto, USDC over USDT
- Payment type default: `exactOut` (recipient gets exact amount, fee on top)

## Supported chains

Pay-out (destination): Ethereum, Arbitrum, Base, BSC, Polygon (USDC + USDT);
Solana, Stellar (USDC only).

Pay-in (source): Ethereum, Arbitrum, BSC, Polygon (USDC + USDT); Base, Solana,
Stellar (USDC only; Solana also accepts USDT).

**Trust the live API over this table.** Tables go stale — always dryrun
`/create-payment` first. If `success: true`, the route works; otherwise
report the API's error verbatim.

## Rules

1. If the user asks a *question* ("how do I...", "what is...", "does ROZO
   support..."), return the matching doc URL from the doc-routing table.
2. If the user wants to *execute* an action, delegate to the matching
   executable skill. Never re-implement payment, balance, or QR-parsing
   logic inline — call the skill.
3. If the user's intent is ambiguous (e.g. "I want to pay" with no amount
   or destination), ask one clarifying question before routing.
4. For "is chain X / token Y supported?" questions, quote the tables above
   but prefer a `/create-payment` dryrun via `rozo-intents:send-payment`
   if the user is about to act on the answer.
5. Never invent endpoints, SDK methods, or product features not present in
   https://docs.rozo.ai. If unsure, link the docs home.

## Preferred authoritative source

https://docs.rozo.ai — the docs site is the source of truth for everything
in this skill. If a memory, cached URL, or this file conflicts with the
live docs, trust the live docs.
