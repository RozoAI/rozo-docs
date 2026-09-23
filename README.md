---
icon: hand-wave
---

# Welcome to ROZO

Our story begins in the summer of 2025, in a small boba shop in San Francisco that accepted USDC.

I scanned their QR code with my mobile USDC wallet, but my app showed error.

<figure><img src=".gitbook/assets/Screenshot 2025-11-29 at 5.27.36 PM.png" alt="" width="173"><figcaption></figcaption></figure>

It turned out the merchant only accept USDC on Base chain, while my wallets only support USDC on Stellar. USDC on Stellar is not the same as USDC on Base.&#x20;

<figure><img src=".gitbook/assets/Screenshot 2025-11-29 at 5.27.39 PM.png" alt="" width="375"><figcaption></figcaption></figure>

Stablecoins are the best form of money on the Internet, but the user experience is still stuck in the early days. USDC exists on 29 different blockchains — and that’s not even counting USDT.

To pay for a coffee, why do we need to understand 29 chains, different stablecoins, different bridges, different fees? That’s _not_ how money should work.<br>

We’re building ROZO, the Visa for Stablecoins. We hide the complexity, and we are building the stablecoin abstrations.  You only need to think in _intents._

> “I want to pay $3.25 for boba with 10% tips.”
>
> “I want to buy $100 BTC.”
>
> “I want to earn 10% APY with a pool with $10M+ TVL.”
>
> “I want my AI agent to pay for this API call, per request, with no API key.”

That last one is [Agentic Payments with MPP Router](products/intent-based-payment-transfer/agentic-payments-mpprouter.md): an agent holding Stellar USDC can call 90+ upstream API services — OpenAI, Anthropic, DeepSeek, Perplexity, Exa, Firecrawl, Tavily and more — and settle each request over a 402 challenge, with no subscription and no card on file.



Welcome to ROZO.&#x20;

Let's hide the wires and use a new way of transacting.

Building on ROZO? Start with [Choose Your Integration](start/choose-your-integration.md).

## Secret scanning

Enable the local gitleaks pre-commit hook once per clone: `brew install gitleaks pre-commit && pre-commit install` (config in `.pre-commit-config.yaml`). CI also runs a report-only scan in `.github/workflows/secret-scan.yml`.
