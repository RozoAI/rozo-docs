# AI Prompts & Templates

## 🤖 Quick Implementation Prompt

Use this prompt with any AI service to generate a complete RozoAI Intent Pay implementation:

```text
Create a React component with RozoAI Intent Pay SDK for crypto payments.

Key points:
- Use demo app ID "rozoDemo" for testing
- CRITICAL: Use getDefaultConfig from @rozoai/intent-pay
  (NOT createConfig from wagmi)
- For Base USDC: use baseUSDC, wrap addresses with getAddress()
- For Stellar USDC: use rozoStellarUSDC, use Stellar addresses as strings
- toUnits: human-readable string (e.g., "10" for 10 USDC)
- Must call resetPayment() when payment params change
- Add onPaymentStarted and onPaymentCompleted handlers

For complete setup instructions and requirements, refer to:
https://docs.rozo.ai/integration/rozointentpay/quick-start.md
```

## 🚀 One-Click Generation

### Lovable

[![Generate with Lovable](https://img.shields.io/badge/Generate%20with-Lovable-FF6B6B?style=for-the-badge&logo=rocket)](https://lovable.dev/?autosubmit=true#prompt=Create%20a%20React%20component%20with%20RozoAI%20Intent%20Pay%20SDK%20for%20crypto%20payments.%20Use%20demo%20app%20ID%20%22rozoDemo%22.%20CRITICAL%3A%20Use%20getDefaultConfig%20from%20%40rozoai%2Fintent-pay%20%28NOT%20createConfig%20from%20wagmi%29.%20For%20Base%20USDC%3A%20use%20baseUSDC%2C%20wrap%20addresses%20with%20getAddress%28%29.%20For%20Stellar%20USDC%3A%20use%20rozoStellarUSDC%2C%20use%20Stellar%20addresses%20as%20strings.%20toUnits%3A%20human-readable%20string%20%28e.g.%20%2210%22%20for%2010%20USDC%29.%20Must%20call%20resetPayment%28%29%20when%20payment%20params%20change.%20Add%20onPaymentStarted%20and%20onPaymentCompleted%20handlers.%20Use%20TypeScript%2C%20TailwindCSS%20for%20mobile-responsive%20design.%20For%20complete%20setup%2C%20refer%20to%20https%3A%2F%2Fdocs.rozo.ai%2Fintegration%2Frozointentpay%2Fquick-start.md)
