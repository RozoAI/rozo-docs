# RozoAI Intent Pay SDK

> **Cross-chain crypto payments made simple** – Accept payments from any blockchain with a single component

[![npm version](https://badge.fury.io/js/@rozoai%2Fintent-pay.svg)](https://badge.fury.io/js/@rozoai%2Fintent-pay)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)

## 🚀 What is RozoAI Intent Pay?

RozoAI Intent Pay SDK is a React component that lets your users pay you in crypto **from any blockchain** - whether they have Ethereum, Solana, Polygon, or dozens of other tokens. Your users can pay with their preferred wallet and token, while you receive exactly what you want.

**Key Benefits:**

- ✅ **One Component** - Add `<RozoPayButton>` and you're done
- ✅ **Any Chain** - Users can pay from 15+ blockchains
- ✅ **Any Wallet** - MetaMask, Phantom, Coinbase Wallet, and more
- ✅ **Any Token** - USDC, ETH, SOL, MATIC, and hundreds more
- ✅ **Mobile Ready** - Works perfectly on mobile apps
- ✅ **Zero Config** - Smart defaults, easy customization

## 📦 Installation

```bash
npm install @rozoai/intent-pay
# or
yarn add @rozoai/intent-pay
# or
pnpm add @rozoai/intent-pay
```

## 🏃‍♂️ Quick Start (2 minutes)

### 1. Wrap Your App

```tsx
import { RozoPayProvider } from "@rozoai/intent-pay";

function App() {
  return (
    <RozoPayProvider>
      <YourApp />
    </RozoPayProvider>
  );
}
```

### 2. Add the Payment Button

```tsx
import { RozoPayButton } from "@rozoai/intent-pay";

function CheckoutPage() {
  return (
    <RozoPayButton
      appId="your-app-id" // Get this from RozoAI dashboard
      toAddress="0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2" // Your wallet
      toToken="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" // USDC on Base
      toUnits="10" // $10 USDC
      toChain={8453} // Base chain
      intent="Purchase" // Button text
      onPaymentStarted={(event) => {
        console.log("Payment started!", event);
        // User has initiated payment
      }}
      onPaymentCompleted={(event) => {
        console.log("Payment completed!", event);
        // Payment successful - fulfill order
      }}
      onPaymentBounced={(event) => {
        console.log("Payment bounced!", event);
        // Payment failed - handle refund
      }}
    />
  );
}
```

That's it! 🎉 Your users can now pay you from any supported blockchain.

## 🎯 Supported Chains & Tokens

### 🔗 Blockchains

| Chain        | Chain ID | Popular Tokens    |
| ------------ | -------- | ----------------- |
| **Ethereum** | 1        | ETH, USDC, USDT   |
| **Base**     | 8453     | ETH, USDC         |
| **Polygon**  | 137      | MATIC, USDC, USDT |
| **Solana**   | 900      | SOL, USDC         |
| **Stellar**  | 1500     | XLM, USDC         |
| **BSC**      | 56       | BNB, USDC, USDT   |

## 💳 Payment Methods Your Users Can Use

### 🔌 Crypto Wallets

- **Desktop**: MetaMask, Coinbase Wallet, Rainbow, Trust Wallet
- **Mobile**: All wallets via deep-linking
- **Solana**: Phantom, Backpack, Solflare
- **Advanced**: Hardware wallets, multisig wallets

## 📋 Complete API Reference

### RozoPayButton Props

```tsx
interface RozoPayButtonProps {
  // Payment Configuration - Either use appId + params OR payId

  // Option 1: Direct parameters
  appId: string; // Your app ID from RozoAI dashboard
  toChain: number; // Destination chain ID
  toToken: Address; // Token contract address ("0x0" for native token)
  toAddress: Address; // EVM destination address
  toUnits?: string; // Amount in smallest token units (optional)
  toStellarAddress?: string; // Stellar destination address
  toSolanaAddress?: string; // Solana destination address
  toCallData?: Hex; // Optional contract call data
  intent?: string; // Button text (e.g., "Pay", "Purchase", "Donate")

  // Option 2: Pre-generated payment
  payId: string; // Payment ID from RozoAI API (replaces above params)

  // Payment Options & Preferences
  paymentOptions?: ExternalPaymentOptionsString[]; // Available payment methods
  preferredChains?: number[]; // Chains shown first in UI
  preferredTokens?: {
    // Tokens shown first in UI
    chain: number;
    address: Address;
  }[];
  evmChains?: number[]; // Restrict to specific EVM chains only

  // Metadata & Tracking
  externalId?: string; // Your correlation ID
  metadata?: RozoPayUserMetadata; // Custom metadata for tracking
  refundAddress?: Address; // Where to refund if payment bounces

  // UI Customization
  mode?: "light" | "dark" | "auto"; // Color scheme
  theme?:
    | "auto"
    | "minimal"
    | "rounded"
    | "retro"
    | "soft"
    | "midnight"
    | "web95"
    | "nouns";
  customTheme?: CustomTheme; // Custom theme object
  disabled?: boolean; // Disable button interaction

  // Modal Behavior
  defaultOpen?: boolean; // Open modal immediately
  closeOnSuccess?: boolean; // Auto-close after successful payment
  resetOnSuccess?: boolean; // Reset payment state after success
  connectedWalletOnly?: boolean; // Skip method selection, use connected wallets only

  // Messages & URLs
  confirmationMessage?: string; // Custom success message
  redirectReturnUrl?: string; // Return URL after external payment flows
  showProcessingPayout?: boolean; // Show processing state after payment

  // Event Handlers
  onPaymentStarted?: (event: PaymentStartedEvent) => void;
  onPaymentCompleted?: (event: PaymentCompletedEvent) => void;
  onPaymentBounced?: (event: PaymentBouncedEvent) => void;
  onOpen?: () => void; // Modal opened
  onClose?: () => void; // Modal closed
}
```

### Event Types

```tsx
interface PaymentStartedEvent {
  type: "payment_started";
  paymentId: string; // Rozo payment ID
  chainId: number; // Source chain where user paid
  txHash?: string; // Transaction hash on source chain
  payment: RozoPayment; // Full payment details
}

interface PaymentCompletedEvent {
  type: "payment_completed";
  paymentId: string; // Rozo payment ID
  chainId: number; // Destination chain
  txHash: string; // Destination transaction hash
  payment: RozoPayment; // Full payment details
  rozoPaymentId?: string; // Your external/correlation ID
}

interface PaymentBouncedEvent {
  type: "payment_bounced";
  paymentId: string; // Rozo payment ID
  chainId: number; // Chain where refund occurred
  txHash: string; // Refund transaction hash
  payment: RozoPayment; // Full payment details
  rozoPaymentId?: string; // Your external/correlation ID
}

// Payment details object
interface RozoPayment {
  id: string;
  status: string;
  fromChain: number;
  fromToken: string;
  fromAmount: string;
  toChain: number;
  toToken: string;
  toAmount: string;
  // ... additional payment metadata
}
```

## 🎨 Themes & Customization

### Built-in Themes

```tsx
<RozoPayButton
  theme="minimal" // Clean, minimal design
  theme="rounded" // Rounded corners, modern
  theme="retro" // Retro/vintage style
  theme="midnight" // Dark theme
  theme="web95" // Windows 95 nostalgic
  theme="soft" // Soft, gentle colors
  theme="nouns" // Nouns DAO inspired
  theme="auto" // Matches system preference
/>
```

### Custom Styling

```tsx
<RozoPayProvider
  customTheme={{
    primaryColor: "#ff6b35",
    borderRadius: "12px",
    fontFamily: "Inter, sans-serif",
  }}
>
  <YourApp />
</RozoPayProvider>
```

## 🔧 Advanced Features

### Custom Button Component

```tsx
import { RozoPayButton } from "@rozoai/intent-pay";

// Use your own button design
<RozoPayButton.Custom
  appId="your-app-id"
  toAddress="0x..."
  toToken="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
  toUnits="10"
  toChain={8453}
>
  {({ show, hide }) => (
    <button
      onClick={show}
      className="my-custom-button-class"
      style={{ background: "linear-gradient(45deg, #ff6b35, #f7931e)" }}
    >
      💰 Pay with Crypto
    </button>
  )}
</RozoPayButton.Custom>;
```

### Payment Method Restrictions

```tsx
<RozoPayButton
  appId="your-app-id"
  toAddress="0x..."
  toToken="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
  toUnits="10"
  toChain={8453}
  // Only allow these payment methods
  paymentOptions={["wallet", "coinbase", "binance"]}
  // Only allow these EVM chains
  evmChains={[1, 8453, 137]} // Ethereum, Base, Polygon only
  // Skip method selection for connected wallets
  connectedWalletOnly={true}
/>
```

### Advanced Event Handling

```tsx
<RozoPayButton
  appId="your-app-id"
  toAddress="0x..."
  toToken="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
  toUnits="10"
  toChain={8453}
  externalId="order_12345" // Your tracking ID
  onOpen={() => {
    // Track modal opened
    analytics.track("payment_modal_opened");
  }}
  onClose={() => {
    // Track modal closed
    analytics.track("payment_modal_closed");
  }}
  onPaymentStarted={(event) => {
    // Payment initiated - show loading state
    setPaymentStatus("processing");

    // Track the start with your analytics
    analytics.track("payment_started", {
      paymentId: event.paymentId,
      sourceChain: event.chainId,
      amount: event.payment.toAmount,
    });
  }}
  onPaymentCompleted={(event) => {
    // Payment successful - fulfill the order
    fulfillOrder(event.rozoPaymentId || event.paymentId);

    // Show success message
    toast.success("Payment completed successfully!");

    // Track completion
    analytics.track("payment_completed", {
      paymentId: event.paymentId,
      txHash: event.txHash,
      amount: event.payment.toAmount,
    });
  }}
  onPaymentBounced={(event) => {
    // Payment failed/bounced - handle refund
    handlePaymentFailure(event.paymentId);

    // Show error message
    toast.error("Payment failed. You will receive a refund.");

    // Track failure
    analytics.track("payment_bounced", {
      paymentId: event.paymentId,
      reason: "bounced",
    });
  }}
/>
```

## 🔧 Advanced Configuration

### Custom Wagmi Config

```tsx
import { createConfig } from "wagmi";
import { RozoPayProvider } from "@rozoai/intent-pay";

const customWagmiConfig = createConfig({
  // Your custom wagmi configuration
});

<RozoPayProvider wagmiConfig={customWagmiConfig}>
  <YourApp />
</RozoPayProvider>;
```

### Multiple Payment Buttons & Advanced Usage

```tsx
// Different products with custom button text
<RozoPayButton
  appId="your-app-id"
  toAddress="0x..."
  toToken="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  // USDC
  toUnits="5"   // $5
  intent="Buy Basic Plan"  // Custom button text
  theme="minimal"
  preferredChains={[8453, 137]}  // Prefer Base and Polygon
/>

<RozoPayButton
  appId="your-app-id"
  toAddress="0x..."
  toToken="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  // USDC
  toUnits="20"  // $20
  intent="Buy Pro Plan"
  theme="rounded"
  closeOnSuccess={true}  // Auto-close modal after payment
  confirmationMessage="Welcome to Pro! 🎉"
/>

// Multi-chain support with Solana and Stellar
<RozoPayButton
  appId="your-app-id"

  // REQUIRED for Solana/Stellar: Base chain config
  toChain={8453}  // MUST be Base chain
  toToken="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  // MUST be Base USDC
  toAddress="0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2"  // Any valid EVM address

  toUnits="10"  // $10 USDC
  intent="Donate"
  preferredTokens={[
    { chain: 8453, address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" }, // Base USDC
    { chain: 137, address: "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174" },  // Polygon USDC
  ]}
  metadata={{
    orderId: "order_123",
    userId: "user_456",
    campaign: "donation_drive_2024"
  }}
/>

// Using pre-generated payment ID (from your backend)
<RozoPayButton
  payId="pay_abc123xyz"  // Generated via RozoAI API
  intent="Complete Purchase"
  onPaymentCompleted={(event) => {
    // Redirect to success page
    window.location.href = `/success?payment=${event.paymentId}`;
  }}
/>
```

## 🔍 Testing & Development

### Test Mode

```tsx
<RozoPayButton
  appId="test-app-id" // Use test app ID for development
  // ... other props
/>
```

### Local Development

```bash
git clone https://github.com/rozoai/intent-pay
cd intent-pay
pnpm install
pnpm dev

# Run example app
cd examples/nextjs-app
pnpm dev
```

## 🐛 Troubleshooting

### Common Issues

**❌ "Payment failed" error**

```tsx
// Make sure all required fields are properly typed
toAddress = "0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2" as Address; // Use Address type
toToken = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" as Address; // Use Address type
```

**❌ "Chain not supported" error**

```tsx
// Use supported chain IDs
toChain={8453}  // Base ✅
toChain={999}   // Unknown chain ❌
```

**❌ Button not appearing**

```tsx
// Make sure RozoPayProvider wraps your component
<RozoPayProvider>
  <ComponentWithRozoPayButton />
</RozoPayProvider>
```

**❌ "Must specify either payId or appId, not both" error**

```tsx
// Don't mix payId with appId parameters
// ✅ Use appId approach:
<RozoPayButton appId="app_123" toAddress="0x..." toToken="0x..." />

// ✅ OR use payId approach:
<RozoPayButton payId="pay_abc123" />

// ❌ Don't do this:
<RozoPayButton appId="app_123" payId="pay_abc123" />
```

**❌ Button showing wrong text**

```tsx
// Use 'intent' prop, not 'text'
<RozoPayButton intent="Purchase Now" />  // ✅
<RozoPayButton text="Purchase Now" />    // ❌ Won't work
```

## ⚠️ Important Multi-Chain Notes

### Solana & Stellar Configuration Requirements

When accepting payments to Solana or Stellar addresses, you **must** configure the button with these specific settings:

```tsx
<RozoPayButton
  // REQUIRED settings for Solana/Stellar support
  toChain={8453} // MUST be Base chain (8453)
  toToken="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" // MUST be Base USDC
  toAddress="0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2" // Any valid EVM address
  // Your actual destination addresses
  toSolanaAddress="DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK" // Optional
  toStellarAddress="GABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZ" // Optional
  // Other props...
  appId="your-app-id"
  toUnits="1"
  intent="Pay"
/>
```

**Why these requirements?**

- RozoAI uses Base chain as the settlement layer for cross-chain payments
- Base USDC is the canonical token for cross-chain transfers
- The EVM `toAddress` serves as a fallback/reference address
- Users can still pay from any supported chain - the restrictions only apply to your configuration

### Debug Mode

```tsx
<RozoPayProvider debugMode={true}>
  <YourApp />
</RozoPayProvider>
```

## 📱 Mobile Integration

### React Native (Expo)

```tsx
import { RozoPayProvider, RozoPayButton } from "@rozoai/intent-pay";

// Works the same as web!
<RozoPayProvider>
  <RozoPayButton {...props} />
</RozoPayProvider>;
```

### Deep Links

The SDK automatically handles wallet deep-linking on mobile devices.

## 🔐 Security & Best Practices

### ✅ Do's

- Always validate payments on your backend
- Use HTTPS in production
- Store sensitive data server-side
- Monitor payment events

### ❌ Don'ts

- Never store private keys in your app
- Don't rely only on frontend payment confirmation
- Don't hardcode sensitive configuration

## 📊 Analytics & Monitoring

```tsx
<RozoPayButton
  onPaymentStarted={(event) => {
    // Track payment initiation
    analytics.track("payment_started", {
      amount: event.toAmount,
      chain: event.toChain,
    });
  }}
  onPaymentCompleted={(event) => {
    // Track successful payments
    analytics.track("payment_completed", {
      paymentId: event.paymentId,
      amount: event.toAmount,
    });
  }}
/>
```

## 🆘 Support & Resources

- 📖 **Documentation**: [docs.rozo.ai](https://docs.rozo.ai)
- 💬 **Discord**: [discord.gg/rozoai](https://discord.gg/rozoai)
- 🐛 **Issues**: [GitHub Issues](https://github.com/rozoai/intent-pay/issues)
- 📧 **Email**: support@rozo.ai

## 🚗 Roadmap

- ✅ Multi-chain payments (Done)
- ✅ Mobile wallet support (Done)
- 🔄 Fiat on-ramps integration (In Progress)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Made with ❤️ by the RozoAI team**

_Simplifying crypto payments, one transaction at a time._
