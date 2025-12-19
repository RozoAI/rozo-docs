# Complete Examples

Copy-paste ready examples for different frameworks and use cases.

## 🎯 Framework-Specific Examples

### Next.js App Router Example

```tsx
// app/providers.tsx
"use client";
import { getDefaultConfig, RozoPayProvider } from "@rozoai/intent-pay";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createConfig, WagmiProvider } from "wagmi";

const wagmiConfig = createConfig(getDefaultConfig({ appName: "Demo" }));
const queryClient = new QueryClient();

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <RozoPayProvider debugMode>{children}</RozoPayProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}

// app/layout.tsx
import { Providers } from "./providers";
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

// app/page.tsx
("use client");
import { RozoPayButton } from "@rozoai/intent-pay";
import { baseUSDC } from "@rozoai/intent-common";
import { getAddress } from "viem";

export default function HomePage() {
  return (
    <RozoPayButton
      appId="rozoDemo"
      toChain={baseUSDC.chainId}
      toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
      toToken={getAddress(baseUSDC.token)}
      toUnits="5"
      intent="Pay $5"
      onPaymentCompleted={() => alert("Payment successful! 🎉")}
    />
  );
}
```

### Vite/CRA Example

```tsx
// src/providers.tsx
import { getDefaultConfig, RozoPayProvider } from "@rozoai/intent-pay";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createConfig, WagmiProvider } from "wagmi";

const wagmiConfig = createConfig(getDefaultConfig({ appName: "Demo" }));
const queryClient = new QueryClient();

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <RozoPayProvider debugMode>{children}</RozoPayProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}

// src/App.tsx
import { RozoPayButton } from "@rozoai/intent-pay";
import { baseUSDC } from "@rozoai/intent-common";
import { getAddress } from "viem";
import { Providers } from "./providers";

function PaymentApp() {
  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h1>Crypto Payment Demo</h1>
      <RozoPayButton
        appId="rozoDemo"
        toChain={baseUSDC.chainId}
        toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
        toToken={getAddress(baseUSDC.token)}
        toUnits="10"
        intent="Pay $10"
        onPaymentCompleted={() => console.log("Payment completed! 🎉")}
      />
    </div>
  );
}

export default function App() {
  return (
    <Providers>
      <PaymentApp />
    </Providers>
  );
}
```

## 🎯 Use Case Examples

### E-commerce Checkout

```tsx
"use client";

import { RozoPayButton, useRozoPayUI } from "@rozoai/intent-pay";
import { baseUSDC } from "@rozoai/intent-common";
import { getAddress } from "viem";
import { useState, useEffect } from "react";

const PRODUCTS = [
  { id: 1, name: "Basic Plan", price: "5", description: "Essential features" },
  { id: 2, name: "Pro Plan", price: "25", description: "Advanced features" },
  { id: 3, name: "Enterprise", price: "100", description: "Full features" },
];

function EcommerceCheckout() {
  const { resetPayment } = useRozoPayUI();
  const [selectedProduct, setSelectedProduct] = useState(PRODUCTS[0]);

  // Reset payment when selected product changes
  useEffect(() => {
    resetPayment({
      toChain: baseUSDC.chainId,
      toAddress: getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2"),
      toToken: getAddress(baseUSDC.token),
      toUnits: selectedProduct.price,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedProduct]);

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Choose Your Plan</h1>

      <div className="grid gap-4 mb-8">
        {PRODUCTS.map((product) => (
          <div
            key={product.id}
            className={`p-4 border rounded-lg cursor-pointer ${
              selectedProduct.id === product.id
                ? "border-blue-500 bg-blue-50"
                : "border-gray-200"
            }`}
            onClick={() => setSelectedProduct(product)}
          >
            <h3 className="font-semibold">{product.name}</h3>
            <p className="text-gray-600">{product.description}</p>
            <p className="text-xl font-bold">${product.price}</p>
          </div>
        ))}
      </div>

      <RozoPayButton
        appId="rozoDemo"
        toChain={baseUSDC.chainId}
        toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
        toToken={getAddress(baseUSDC.token)}
        toUnits={selectedProduct.price}
        intent={`Buy ${selectedProduct.name}`}
        metadata={{ productId: selectedProduct.id }}
        onPaymentCompleted={(event) => {
          console.log("Purchase completed!", event);
          alert(`${selectedProduct.name} purchased successfully! 🎉`);
        }}
      />
    </div>
  );
}
```

### Donation Component

```tsx
"use client";

import { RozoPayButton, useRozoPayUI } from "@rozoai/intent-pay";
import { baseUSDC, TokenSymbol } from "@rozoai/intent-common";
import { getAddress } from "viem";
import { useState, useEffect } from "react";

const DONATION_AMOUNTS = ["5", "10", "25", "50", "100"];

function DonationComponent() {
  const { resetPayment } = useRozoPayUI();
  const [customAmount, setCustomAmount] = useState("");
  const [selectedAmount, setSelectedAmount] = useState("10");

  const finalAmount = customAmount || selectedAmount;

  // Reset payment when donation amount changes
  useEffect(() => {
    if (finalAmount && parseFloat(finalAmount) > 0) {
      resetPayment({
        toChain: baseUSDC.chainId,
        toAddress: getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2"),
        toToken: getAddress(baseUSDC.token),
        toUnits: finalAmount,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [finalAmount]);

  return (
    <div className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-6">Support Our Project</h1>

      <div className="mb-6">
        <p className="text-gray-600 mb-4">Choose donation amount:</p>

        <div className="grid grid-cols-3 gap-2 mb-4">
          {DONATION_AMOUNTS.map((amount) => (
            <button
              key={amount}
              className={`p-2 border rounded ${
                selectedAmount === amount && !customAmount
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200"
              }`}
              onClick={() => {
                setSelectedAmount(amount);
                setCustomAmount("");
              }}
            >
              ${amount}
            </button>
          ))}
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">
            Custom amount ($):
          </label>
          <input
            type="number"
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="Enter amount"
            value={customAmount}
            onChange={(e) => setCustomAmount(e.target.value)}
          />
        </div>
      </div>

      {finalAmount && parseFloat(finalAmount) > 0 && (
        <RozoPayButton
          appId="rozoDemo"
          toChain={baseUSDC.chainId}
          toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
          toToken={getAddress(baseUSDC.token)}
          toUnits={finalAmount}
          intent={`Donate $${finalAmount}`}
          preferredChains={[8453, 137]} // Prefer Base and Polygon
          preferredSymbol={[TokenSymbol.USDC, TokenSymbol.USDT]} // Prioritize USDC and USDT
          onPaymentCompleted={() => {
            alert(`Thank you for your $${finalAmount} donation! 🙏`);
          }}
        />
      )}

      {(!finalAmount || parseFloat(finalAmount) <= 0) && (
        <div className="p-3 bg-gray-100 rounded text-sm text-gray-600">
          Please select or enter a donation amount
        </div>
      )}
    </div>
  );
}
```

### Stellar Payout Example

```tsx
"use client";

import { RozoPayButton } from "@rozoai/intent-pay";
import { rozoStellarUSDC } from "@rozoai/intent-common";

export default function StellarPayment() {
  return (
    <RozoPayButton
      appId="rozoDemo"
      toChain={rozoStellarUSDC.chainId} // Stellar chain (1500)
      toToken={rozoStellarUSDC.token} // Stellar USDC token
      toAddress="GABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZ" // Stellar address
      toUnits="25"
      intent="Pay $25 to Stellar"
      onPaymentCompleted={(event) => {
        console.log("Stellar payment completed!", event.txHash);
        alert("Payment successful! 🎉");
      }}
    />
  );
}
```

### Token Symbol Preference Example

```tsx
"use client";

import { RozoPayButton } from "@rozoai/intent-pay";
import { baseUSDC, TokenSymbol } from "@rozoai/intent-common";
import { getAddress } from "viem";

// Default behavior (no prop needed) - prioritizes USDC and USDT
export default function DefaultPayment() {
  return (
    <RozoPayButton
      appId="rozoDemo"
      toChain={baseUSDC.chainId}
      toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
      toToken={getAddress(baseUSDC.token)}
      toUnits="10"
      intent="Pay $10"
    />
  );
}

// Prioritize USDC and USDT across all chains
export function PreferredSymbolsPayment() {
  return (
    <RozoPayButton
      appId="rozoDemo"
      toChain={baseUSDC.chainId}
      toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
      toToken={getAddress(baseUSDC.token)}
      toUnits="10"
      intent="Pay $10"
      preferredSymbol={[TokenSymbol.USDC, TokenSymbol.USDT]}
    />
  );
}

// Prioritize EURC only
// Note: EURC can only be sent to EURC - ensure toToken is an EURC token address
export function EURCPayment() {
  return (
    <RozoPayButton
      appId="rozoDemo"
      toChain={baseUSDC.chainId}
      toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
      toToken={getAddress(baseUSDC.token)} // Must be EURC token address
      toUnits="10"
      intent="Pay $10"
      preferredSymbol={[TokenSymbol.EURC]}
    />
  );
}
```

## 📖 Next Steps

- [Check API reference](api-reference.md) for all available props
- [See troubleshooting guide](troubleshooting.md) for common issues
- [Use AI prompts](ai-prompts.md) for code generation
