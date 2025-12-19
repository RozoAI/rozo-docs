# API Reference

Complete reference for RozoAI Intent Pay SDK props, configuration, and customization options.

## 📋 Core Props (ALWAYS REQUIRED)

```tsx
<RozoPayButton
  appId="rozoDemo" // Demo app ID
  toChain={8453} // Base chain ID
  toAddress={getAddress("0x...")} // Your wallet address
  toToken={getAddress(baseUSDC.token)} // USDC token
  toUnits="10" // $10 USDC (optional)
  intent="Pay Now" // Button text (optional)
  preferredSymbol={[TokenSymbol.USDC, TokenSymbol.USDT]} // Optional: prioritize token symbols
/>
```

### Required Props

| Prop        | Type      | Description            | Example                      |
| ----------- | --------- | ---------------------- | ---------------------------- |
| `appId`     | `string`  | Your app identifier    | `"rozoDemo"`                 |
| `toChain`   | `number`  | Destination chain ID   | `8453` (Base)                |
| `toAddress` | `Address` | Your wallet address    | `getAddress("0x742d...")`    |
| `toToken`   | `Address` | Token contract address | `getAddress(baseUSDC.token)` |

### Semi-Optional Props

| Prop      | Type     | Description                                                                                                         | Default |
| --------- | -------- | ------------------------------------------------------------------------------------------------------------------- | ------- |
| `toUnits` | `string` | Human-readable amount as string (e.g., `"10"` for 10 USDC, no `parseFloat` needed). If not provided, user prompted. | -       |
| `intent`  | `string` | Button text/payment verb                                                                                            | `"Pay"` |

## 🎯 Event Handlers (RECOMMENDED)

```tsx
<RozoPayButton
  // ... required props
  onPaymentStarted={(event) => {
    console.log("Payment started:", event.paymentId);
    // Show loading state
  }}
  onPaymentCompleted={(event) => {
    console.log("Payment completed:", event.txHash);
    // Fulfill order, show success
  }}
  onPaymentBounced={(event) => {
    console.log("Payment failed:", event);
    // Handle refund, show error
  }}
/>
```

### Event Handler Types

```tsx
interface PaymentStartedEvent {
  type: RozoPayEventType.PaymentStarted;
  paymentId: string;
  chainId: number;
  txHash: string | null;
  payment: RozoPayment;
}

interface PaymentCompletedEvent {
  type: RozoPayEventType.PaymentCompleted;
  paymentId: string;
  chainId: number;
  txHash: string;
  payment: RozoPayment;
  rozoPaymentId?: string;
}

interface PaymentBouncedEvent {
  type: RozoPayEventType.PaymentBounced;
  paymentId: string;
  chainId: number;
  txHash: string;
  payment: RozoPayment;
  rozoPaymentId?: string;
}
```

## 🔧 Optional Customization Props

### Chain & Token Preferences

```tsx
<RozoPayButton
  // ... required props
  preferredChains={[8453, 137]} // Prefer Base, Polygon
  preferredTokens={[
    // Prefer specific tokens
    { chain: 8453, address: getAddress(baseUSDC.token) },
  ]}
  preferredSymbol={[TokenSymbol.USDC, TokenSymbol.USDT]} // Prioritize USDC and USDT across all chains
/>
```

| Prop              | Type                | Description                                                                                                                         | Default        |
| ----------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| `preferredChains` | `number[]`          | Preferred chain IDs in order                                                                                                        | -              |
| `preferredTokens` | `TokenPreference[]` | Preferred tokens with chain/address                                                                                                 | -              |
| `preferredSymbol` | `TokenSymbol[]`     | Prioritizes token symbols across all supported chains in token selection UI. If `preferredTokens` is provided, it takes precedence. | `[USDC, USDT]` |

```tsx
import { TokenSymbol } from "@rozoai/intent-common";

interface TokenPreference {
  chain: number;
  address: Address;
}
```

**Note:** `preferredSymbol` automatically finds matching tokens across all chains (Base, Polygon, Ethereum, Solana, Stellar). Only `USDC`, `USDT`, and `EURC` are supported values. Invalid symbols are filtered with a console warning.

**Important:** EURC can only be sent to EURC. When using `TokenSymbol.EURC`, ensure your `toToken` is also an EURC token address.

### Stellar Payout Support

For Stellar USDC payouts, use `rozoStellarUSDC` from `@rozoai/intent-common`:

```tsx
import { rozoStellarUSDC } from "@rozoai/intent-common";

<RozoPayButton
  appId="rozoDemo"
  toChain={rozoStellarUSDC.chainId} // Stellar chain (1500)
  toToken={rozoStellarUSDC.token} // Stellar USDC token
  toAddress="GABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZ" // Stellar address (no getAddress needed)
  toUnits="15"
  intent="Pay $15"
/>;
```

**Available Payout Options:**

- **Base USDC**: Use `baseUSDC.chainId` (8453), `baseUSDC.token`, and Base address with `getAddress()`
- **Stellar USDC**: Use `rozoStellarUSDC.chainId` (1500), `rozoStellarUSDC.token`, and Stellar address (no `getAddress()` needed)

For a complete list of supported payout chains and tokens, see [Supported Tokens and Chains](../api-doc/supported-tokens-and-chains.md).

### UI Customization

```tsx
<RozoPayButton
  // ... required props
  theme="minimal" // Built-in themes
  mode="auto" // Light/dark mode
  disabled={false} // Enable/disable button
  className="custom-button-class" // Custom CSS class
/>
```

| Prop        | Type      | Description      | Options                                                                                     |
| ----------- | --------- | ---------------- | ------------------------------------------------------------------------------------------- |
| `theme`     | `string`  | Built-in theme   | `"minimal"`, `"rounded"`, `"retro"`, `"midnight"`, `"web95"`, `"soft"`, `"nouns"`, `"auto"` |
| `mode`      | `string`  | Color mode       | `"light"`, `"dark"`, `"auto"`                                                               |
| `disabled`  | `boolean` | Button state     | `true`, `false`                                                                             |
| `className` | `string`  | Custom CSS class | Any valid CSS class                                                                         |

### Advanced Configuration

```tsx
<RozoPayButton
  // ... required props

  // Tracking & Metadata
  metadata={{ orderId: "123", userId: "user456" }} // Custom metadata
  externalId="order_456" // Your tracking ID
  // Smart Contract Calls
  toCallData="0x..." // Optional calldata for contract interaction
  // Payment Options
  paymentOptions={["card", "crypto"]} // Limit payment methods
  evmChains={[1, 8453, 137]} // Restrict to specific EVM chains
  // Refund Configuration
  refundAddress={getAddress("0x...")} // Address for refunds
/>
```

| Prop            | Type                  | Description                              |
| --------------- | --------------------- | ---------------------------------------- |
| `metadata`      | `Record<string, any>` | Custom data to include with payment      |
| `externalId`    | `string`              | Your internal tracking identifier        |
| `toCallData`    | `Hex`                 | Optional calldata for contract calls     |
| `evmChains`     | `number[]`            | Restrict payments to specific EVM chains |
| `refundAddress` | `Address`             | Address to receive refunds if needed     |

## 🎨 Built-in Themes

### Theme Options

```tsx
theme = "minimal"; // Clean, minimal design (default)
theme = "rounded"; // Rounded corners, modern
theme = "retro"; // Retro/vintage style
theme = "midnight"; // Dark theme
theme = "web95"; // Windows 95 nostalgic
theme = "soft"; // Soft, gentle colors
theme = "nouns"; // Nouns DAO inspired
theme = "auto"; // Matches system preference
```

### Custom Styling

```tsx
// Use className for custom styling
<RozoPayButton
  className="bg-purple-500 hover:bg-purple-600 text-white font-bold py-3 px-6 rounded-lg"
  // ... other props
/>

// Or use customTheme for advanced theming
<RozoPayButton
  customTheme={{
    colors: {
      primary: "#8B5CF6",
      secondary: "#A78BFA",
      background: "#F3F4F6",
      text: "#1F2937"
    },
    borderRadius: "12px",
    fontFamily: "Inter, sans-serif"
  }}
  // ... other props
/>
```

## 🎆 Modal Control & Behavior

### Modal Options

```tsx
<RozoPayButton
  // ... required props
  defaultOpen={true} // Open modal immediately
  closeOnSuccess={true} // Auto-close after payment
  resetOnSuccess={false} // Keep payment state after success
  connectedWalletOnly={true} // Skip payment method selection
  // Modal event handlers
  onOpen={() => console.log("Modal opened")}
  onClose={() => console.log("Modal closed")}
/>
```

| Prop                   | Type       | Description                                    | Default |
| ---------------------- | ---------- | ---------------------------------------------- | ------- |
| `defaultOpen`          | `boolean`  | Open modal automatically when component mounts | `false` |
| `closeOnSuccess`       | `boolean`  | Close modal after successful payment           | `false` |
| `resetOnSuccess`       | `boolean`  | Reset payment state after success              | `true`  |
| `connectedWalletOnly`  | `boolean`  | Skip to wallet tokens (embedded flows)         | `false` |
| `confirmationMessage`  | `string`   | Custom message on confirmation screen          | -       |
| `redirectReturnUrl`    | `string`   | Return URL for external payment providers      | -       |
| `showProcessingPayout` | `boolean`  | Show processing state after payment completion | `false` |
| `onOpen`               | `function` | Called when modal opens                        | -       |
| `onClose`              | `function` | Called when modal closes                       | -       |

## 🚀 Alternative: Pre-created Payments

### Using PayId

For server-side payment creation, use the `payId` prop instead:

```tsx
// Create payment server-side first
const payId = await createRozoPayment({
  appId: "rozoDemo",
  toChain: 8453,
  toAddress: "0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2",
  toToken: baseUSDC.token,
  toUnits: "10",
  intent: "Pay Now",
});

// Then use payId in component
<RozoPayButton
  payId={payId}
  onPaymentCompleted={(event) => {
    // Handle completion
  }}
/>;
```

| Prop    | Type     | Description            |
| ------- | -------- | ---------------------- |
| `payId` | `string` | Pre-created payment ID |

**⚠️ IMPORTANT:** You must specify EITHER `appId` (with payment params) OR `payId`, but not both.

## 🎨 Custom Component Variant

### RozoPayButton.Custom

For complete UI control, use the Custom variant with a render prop:

```tsx
<RozoPayButton.Custom
  appId="rozoDemo"
  toChain={8453}
  toAddress={getAddress("0x...")}
  toToken={getAddress(baseUSDC.token)}
  toUnits="10"
  onPaymentCompleted={(event) => {
    console.log("Payment completed:", event.txHash);
  }}
>
  {({ show, hide }) => (
    <button
      onClick={show}
      className="custom-pay-button"
      style={{
        background: "linear-gradient(45deg, #FF6B6B, #4ECDC4)",
        border: "none",
        padding: "12px 24px",
        borderRadius: "8px",
        color: "white",
        fontWeight: "bold",
        cursor: "pointer",
      }}
    >
      🚀 Pay with Rozo
    </button>
  )}
</RozoPayButton.Custom>
```

**Render Props:**

- `show()` - Function to open the payment modal
- `hide()` - Function to close the payment modal

## 🔍 TypeScript Types

### Core Types

```tsx
import type { Address, Hex } from "viem";
import { TokenSymbol } from "@rozoai/intent-common";

// Main component props (using appId)
interface RozoPayButtonProps {
  // Required
  appId: string;
  toChain: number;
  toAddress: Address;
  toToken: Address;

  // Semi-optional
  toUnits?: string;
  intent?: string;

  // Optional
  toCallData?: Hex;

  // Preferences
  preferredChains?: number[];
  preferredTokens?: TokenPreference[];
  preferredSymbol?: TokenSymbol[];
  evmChains?: number[];

  // UI
  theme?: ThemeType;
  mode?: "light" | "dark" | "auto";
  customTheme?: CustomTheme;
  disabled?: boolean;
  className?: string;

  // Tracking
  metadata?: Record<string, any>;
  externalId?: string;
  refundAddress?: Address;

  // Modal behavior
  defaultOpen?: boolean;
  closeOnSuccess?: boolean;
  resetOnSuccess?: boolean;
  connectedWalletOnly?: boolean;
  confirmationMessage?: string;
  redirectReturnUrl?: string;
  showProcessingPayout?: boolean;

  // Events
  onPaymentStarted?: (event: PaymentStartedEvent) => void;
  onPaymentCompleted?: (event: PaymentCompletedEvent) => void;
  onPaymentBounced?: (event: PaymentBouncedEvent) => void;
  onOpen?: () => void;
  onClose?: () => void;
}

type ThemeType =
  | "minimal"
  | "rounded"
  | "retro"
  | "midnight"
  | "web95"
  | "soft"
  | "nouns"
  | "auto";

interface TokenPreference {
  chain: number;
  address: Address;
}

interface CustomTheme {
  colors?: {
    primary?: string;
    secondary?: string;
    background?: string;
    text?: string;
  };
  borderRadius?: string;
  fontFamily?: string;
}
```

## 🔄 Dynamic Payment Updates

### Using resetPayment() Hook

When payment parameters (`toChain`, `toAddress`, `toToken`, or `toUnits`) change dynamically, you **must** call `resetPayment()` from the `useRozoPayUI()` hook:

```tsx
import { useRozoPayUI } from "@rozoai/intent-pay";

function PaymentComponent() {
  const { resetPayment } = useRozoPayUI();
  const [amount, setAmount] = useState("10");

  useEffect(() => {
    resetPayment({
      toChain: baseUSDC.chainId,
      toAddress: getAddress("0x742d..."),
      toToken: getAddress(baseUSDC.token),
      toUnits: amount, // Human-readable string (e.g., "10" for 10 USDC)
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [amount]); // Call resetPayment() when amount changes

  return (
    <RozoPayButton
      appId="rozoDemo"
      toChain={baseUSDC.chainId}
      toAddress={getAddress("0x742d...")}
      toToken={getAddress(baseUSDC.token)}
      toUnits={amount}
    />
  );
}
```

**Important Notes:**

- `toUnits` accepts human-readable amounts as strings (e.g., `"10"` for 10 USDC, no `parseFloat` needed)
- You **must** call `resetPayment()` whenever `toChain`, `toAddress`, `toToken`, or `toUnits` values change
- Use `useRozoPayUI()` hook to access the `resetPayment` function

## 📖 Next Steps

- [View complete examples](examples.md) for implementation patterns
- [Check troubleshooting guide](troubleshooting.md) for common issues
- [Use AI prompts](ai-prompts.md) for code generation
