# ROZO Intent Pay SDK

> **Cross-chain crypto payments made simple** – Accept payments from any blockchain with a single component

[![npm version](https://badge.fury.io/js/@rozoai%2Fintent-pay.svg)](https://badge.fury.io/js/@rozoai%2Fintent-pay) [![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/) [![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)

## 🎯 What RozoAI Intent Pay Does

RozoAI Intent Pay SDK is a React component that lets users pay you in crypto from supported networks — Base, Polygon, Solana, Stellar, and BSC. Your users can pay with their preferred wallet, while you receive exactly what you want.

**Key Benefits:**

* ✅ **One Component** - Add `<RozoPayButton>` and you're done
* ✅ **Supported Chains** - Base, Polygon, Solana, Stellar, BSC
* ✅ **Any Wallet** - MetaMask, Phantom, Coinbase Wallet, and more
* ✅ **Supported Tokens** - USDC on Base/Polygon/Solana/Stellar; USDT on BSC
* ✅ **Mobile Ready** - Works perfectly on mobile apps
* ✅ **Zero Config** - Smart defaults, easy customization

## 📚 Documentation

| Document                                    | Description                                        |
| ------------------------------------------- | -------------------------------------------------- |
| [**Quick Start Guide**](quick-start.md)     | Get up and running in 5 minutes                    |
| [**Complete Examples**](examples.md)        | Copy-paste ready examples for different frameworks |
| [**API Reference**](api-reference.md)       | Complete props and configuration reference         |
| [**Troubleshooting**](troubleshooting.md)   | Common mistakes and how to avoid them              |
| [**AI Prompts & Templates**](ai-prompts.md) | Templates for AI services to generate code         |

## 🚀 Quick Example

```tsx
import { RozoPayButton } from "@rozoai/intent-pay";
import { baseUSDC } from "@rozoai/intent-common";
import { getAddress } from "viem";

<RozoPayButton
  appId="rozoDemo"
  toChain={baseUSDC.chainId}
  toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
  toToken={getAddress(baseUSDC.token)}
  toUnits="10"
  intent="Pay $10"
  onPaymentCompleted={() => alert("Payment successful! 🎉")}
/>;
```

## 🔗 Supported Chains & Tokens

| Chain       | Chain ID | Token | Supported |
| ----------- | -------- | ----- | :-------: |
| **Base**    | 8453     | USDC  |     ✅     |
| **Polygon** | 137      | USDC  |     ✅     |
| **BSC**     | 56       | USDT  |     ✅     |
| **Solana**  | -        | USDC  |     ✅     |
| **Stellar** | -        | USDC  |     ✅     |

## 💳 Payment Methods

Supported wallets:

* **Desktop**: MetaMask, Coinbase Wallet, Rainbow, Trust Wallet, Phantom, Albedo, etc.
* **Mobile**: All wallets via deep-linking

## 🔧 Installation

```bash
npm install @rozoai/intent-pay @rozoai/intent-common @tanstack/react-query wagmi viem
```

## 📞 Support & Resources

* 📖 **Documentation**: [docs.rozo.ai](https://docs.rozo.ai)
* 💬 **Discord**: [discord.gg/rozoai](https://discord.com/invite/EfWejgTbuU)
* 🐛 **Issues**: [GitHub Issues](https://github.com/rozoai/intent-pay/issues)
* 📧 **Email**: support@rozo.ai
* 🔗 **Demo**: [demo.rozo.ai](https://demo.rozo.ai/)

## 📄 License

MIT License - see [LICENSE](../../intent-pay/LICENSE/) for details.

***

**Made with ❤️ by the RozoAI team**

_Simplifying crypto payments, one transaction at a time._
