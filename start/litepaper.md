# 🧾 ROZO Lite Paper

### Overview

Rozo is building the Visa for crypto-native payments — enabling users to tap and pay with stablecoins as effortlessly as using Apple Pay. By abstracting away the complexity of blockchains, wallets, gas fees, and token types, Rozo delivers a frictionless experience for both users and merchants, online and in the real world.

#### ROZO Intents

We hide the complexity, and it's referred as ROZO Intents (intent bsed) or stablecoin abstractions.

Intents based is the way to transact with others focusing on outcomes not processes.  As the user, you only need to declare an end result without stating how to accomplish it.

### 1. 🎯 The Problem: Fragmented Stablecoin Payments

Crypto users and merchants face overwhelming fragmentation:

* Every chain has its own token formats, gas requirements, and wallet UX.
* Stablecoins are scattered across Solana, Ethereum, Base, Arbitrum, Tron, and more.
* Current crypto payments require multi-step processes: wallet approvals, token bridging, and manual chain switching.

This fragmentation severely limits crypto’s usability in real-world commerce — from cafés and coworking spaces to online SaaS and AI agents.

<figure><img src=".gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

### 2. 🧠 Solution: Intent-Based Stablecoin Abstraction

Rozo introduces a cross-chain payment abstraction powered by intent-based infrastructure. With Rozo, users pay in one click — any token, any chain — and merchants receive stablecoins seamlessly.

Key abstractions:

* Token: Users can pay with any token they hold.
* Chain: Rozo handles bridging and routing under the hood.
* Flow: One-click checkout — no approve + send, no gas setup.

Core components:

* Intent Addresses: Deterministically generated smart contracts (via CREATE2 on EVM, PDA on Solana) that encode payment parameters.
* Liquidity Solvers: Third parties who observe incoming payments and instantly settle to the merchant, recovering funds via cross-chain bridges or swaps.

### 3. 🧱 Architecture Overview

a. Intent Address Layer

* Deterministic addresses encode {amount, fromChain, toChain, token, receiver}.
* On EVM chains: Generated via a CREATE2 smart contract factory.
* On Solana: Built using Program Derived Addresses (PDAs).

b. Execution Layer

* User sends funds to the intent address.
* Solvers detect the payment and front settlement to the merchant in 1–3 seconds.
* Rozo routes funds through protocols or p2p as needed.

***

### 4. 🧩 Use Cases

Rozo powers stablecoin payments across both online platforms and physical storefronts — without subscriptions, wallet friction, or gas management.

#### A. Online Use Cases.

**🧰 SaaS & Online Merchants - Pay as you go**

* Rozo powers “pay-as-you-go” payments for SaaS without Stripe or fiat friction.
* Users can top-up stablecoins and use balance across services — just like credits.
* Suited for indie hackers, no-code tools, and global creators who need permissionless monetization.
* Use cases like OpenRouter, Creatify.ai

**🧠 MCP & AI Services**

Rozo is compatible with the emerging x402 payment protocol launched by Coinbase, which enables instant stablecoin payments over HTTP. This allows Rozo-integrated services — including APIs, SaaS apps, and AI agents — to monetize through standard web infrastructure without wallets or subscriptions. Developers can embed Rozo’s intent-based payment system directly into HTTP 402 flows, enabling seamless microtransactions for API access, software features, or metered compute. Rozo aligns with this standard to support the next generation of agent-native commerce and programmable internet value transfer.

#### B. IRL (In-Real-Life) Use Cases

**☕️ Cafés & Restaurants, Spas, Wellness & Lifestyle Vendors**

* Tourists, nomads, and locals pay in seconds using their crypto balance — no wallet popups or tokens to approve.
* Merchants can offer promotions or loyalty via Rozo incentives (e.g., cashback, credits).

**🏬** Tap to pay via Rozo POS.

* IRL businesses are listed on Rozo’s Web App, discoverable by crypto-paying users nearby.

#### C. Privacy

Rozo is built with privacy as a core principle Instead of tying payments to identity, Rozo uses single-use intent addresses and ephemeral data flows to minimize metadata leakage. Merchants receive funds without knowing a payer’s wallet history, and users transact without exposing their holdings, device info, or behavioral patterns. For off-chain flows, Rozo supports anonymous top-ups and proxy checkout layers that resemble the privacy of handing over physical cash — giving users control over when and how they reveal information, if ever.

Join us in building the “Visa for for Stablecoins” with Tap to Pay experience.
