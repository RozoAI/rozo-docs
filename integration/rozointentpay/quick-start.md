# Quick Start Guide

Get up and running with RozoAI Intent Pay SDK in 5 minutes.

## 🚀 Installation

```bash
npm install @rozoai/intent-pay @rozoai/intent-common @tanstack/react-query wagmi viem @creit.tech/stellar-wallets-kit @stellar/stellar-sdk
```

## 📁 Basic Setup

### 1. Create Providers File

Create `src/providers.tsx`:

```tsx
"use client";

import { getDefaultConfig, RozoPayProvider } from "@rozoai/intent-pay";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { type ReactNode } from "react";
import { createConfig, WagmiProvider } from "wagmi";

export const wagmiConfig = createConfig(
  getDefaultConfig({
    appName: "Your App Name",
  })
);

const queryClient = new QueryClient();

export function Providers({ children }: { children: ReactNode }) {
  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <RozoPayProvider debugMode>{children}</RozoPayProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
```

### 2. Wrap Your App

```tsx
// App.tsx or layout.tsx
import { Providers } from "./providers";

export default function App() {
  return <Providers>{/* Your app components */}</Providers>;
}
```

### 3. Add Payment Button with Dynamic Form

**Important Notes:**

- `toUnits` prop accepts human-readable amounts as strings (e.g., `"10"` for 10 USDC, no `parseFloat` needed)
- You **must** call `resetPayment()` whenever `toChain`, `toAddress`, `toToken`, or `toUnits` values change
- Use `useRozoPayUI()` hook to access the `resetPayment` function

```tsx
"use client";

import { useState, useEffect } from "react";
import { RozoPayButton, useRozoPayUI } from "@rozoai/intent-pay";
import { baseUSDC } from "@rozoai/intent-common";
import { getAddress, isAddress } from "viem";

function PaymentDemo() {
  const { resetPayment } = useRozoPayUI();
  const [formData, setFormData] = useState({
    recipientAddress: "",
    tokenAddress: baseUSDC.token,
    amount: "5",
  });

  // PayButton only visible when Address and Token Address are filled
  const canShowButton =
    formData.recipientAddress &&
    isAddress(formData.recipientAddress) &&
    formData.tokenAddress &&
    isAddress(formData.tokenAddress) &&
    formData.amount &&
    parseFloat(formData.amount) > 0;

  // IMPORTANT: Must call resetPayment() whenever toChain, toAddress, toToken, or toUnits changes
  // toUnits is a human-readable amount as string (e.g., "10" for 10 USDC, no parseFloat needed)
  useEffect(() => {
    if (canShowButton) {
      resetPayment({
        toChain: baseUSDC.chainId,
        toAddress: getAddress(formData.recipientAddress),
        toToken: getAddress(formData.tokenAddress),
        toUnits: formData.amount, // Human-readable amount as string
      });
    }
  }, [formData, canShowButton]);

  return (
    <div className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6">Crypto Payment Demo</h1>

      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium mb-1">
            Recipient Address *
          </label>
          <input
            type="text"
            className="w-full p-2 border rounded"
            placeholder="0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2"
            value={formData.recipientAddress}
            onChange={(e) =>
              setFormData((prev) => ({
                ...prev,
                recipientAddress: e.target.value,
              }))
            }
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Token Address *
          </label>
          <input
            type="text"
            className="w-full p-2 border rounded"
            placeholder="USDC Token Address"
            value={formData.tokenAddress}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, tokenAddress: e.target.value }))
            }
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Amount *</label>
          <input
            type="number"
            step="0.01"
            min="0"
            className="w-full p-2 border rounded"
            placeholder="5.00"
            value={formData.amount}
            onChange={(e) =>
              setFormData((prev) => ({ ...prev, amount: e.target.value }))
            }
          />
        </div>
      </div>

      {canShowButton && (
        <RozoPayButton
          appId="rozoDemo" // Demo app ID
          toChain={baseUSDC.chainId} // Base chain (8453)
          toAddress={getAddress(formData.recipientAddress)} // Your wallet
          toToken={getAddress(formData.tokenAddress)} // USDC on Base
          toUnits={formData.amount} // Human-readable amount as string (e.g., "10" for 10 USDC)
          intent={`Pay $${formData.amount}`} // Button text
          onPaymentStarted={(event) => {
            console.log("✅ Payment started!", event.paymentId);
          }}
          onPaymentCompleted={(event) => {
            console.log("🎉 Payment completed!", event.txHash);
            alert("Payment successful! 🎉");
          }}
          onPaymentBounced={(event) => {
            console.log("❌ Payment bounced!", event);
            alert("Payment failed. You'll receive a refund.");
          }}
        />
      )}

      {!canShowButton && (
        <div className="p-3 bg-gray-100 rounded text-sm text-gray-600">
          Please fill in all required fields to show the payment button
        </div>
      )}
    </div>
  );
}
```

## 🎯 Quick Customization

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

## 📖 Next Steps

- [View complete examples](examples.md) for different frameworks
- [Read API reference](api-reference.md) for all available props
- [See troubleshooting guide](troubleshooting.md) for common issues
