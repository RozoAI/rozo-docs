# Troubleshooting Guide

Common mistakes and solutions when implementing RozoAI Intent Pay SDK.

## ⚠️ COMMON MISTAKES TO AVOID

### ❌ Missing getAddress() Wrapper

**Problem:**

```tsx
// ❌ DON'T DO THIS - Raw strings
toAddress = "0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2";
toToken = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
```

**Solution:**

```tsx
// ✅ DO THIS - Wrapped with getAddress()
toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
toToken={getAddress(baseUSDC.token)}
```

**Why it happens:** TypeScript requires proper Address types from viem.

### ❌ Wrong Stellar Configuration

**Problem:**

```tsx
// ❌ DON'T DO THIS - Wrong chain/token for Stellar payout
<RozoPayButton
  appId="rozoDemo"
  toChain={8453} // ❌ Wrong chain for Stellar
  toToken={getAddress(baseUSDC.token)} // ❌ Wrong token for Stellar
  toAddress={getAddress("GABC123...")} // ❌ Don't use getAddress() for Stellar
/>
```

**Solution:**

```tsx
// ✅ DO THIS - Correct Stellar config
import { rozoStellarUSDC } from "@rozoai/intent-common";

<RozoPayButton
  appId="rozoDemo"
  toChain={rozoStellarUSDC.chainId} // ✅ Stellar chain (1500)
  toToken={rozoStellarUSDC.token} // ✅ Stellar USDC token
  toAddress="GABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZ" // ✅ Stellar address (no getAddress)
/>;
```

**Why it happens:** Stellar payouts require Stellar chain ID (1500) and Stellar token format. Stellar addresses should not be wrapped with `getAddress()`.

### ❌ Not Calling resetPayment() When Payment Params Change

**Problem:**

```tsx
// ❌ DON'T DO THIS - Payment params change but resetPayment() not called
function PaymentComponent() {
  const [amount, setAmount] = useState("10");

  return (
    <RozoPayButton
      appId="rozoDemo"
      toChain={baseUSDC.chainId}
      toAddress={getAddress("0x742d...")}
      toToken={getAddress(baseUSDC.token)}
      toUnits={amount} // ❌ Changed but resetPayment() not called
    />
  );
}
```

**Solution:**

```tsx
// ✅ DO THIS - Call resetPayment() when params change
import { useRozoPayUI } from "@rozoai/intent-pay";

function PaymentComponent() {
  const { resetPayment } = useRozoPayUI();
  const [amount, setAmount] = useState("10");

  useEffect(() => {
    resetPayment({
      toChain: baseUSDC.chainId,
      toAddress: getAddress("0x742d..."),
      toToken: getAddress(baseUSDC.token),
      toUnits: amount, // ✅ resetPayment() called when amount changes
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [amount]);

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

**Why it happens:** You **must** call `resetPayment()` from `useRozoPayUI()` hook whenever `toChain`, `toAddress`, `toToken`, or `toUnits` values change to update the payment state.

### ❌ Using parseFloat() for toUnits

**Problem:**

```tsx
// ❌ DON'T DO THIS - Using parseFloat() unnecessarily
const amount = parseFloat("10"); // ❌ Not needed
<RozoPayButton toUnits={amount.toString()} />;
```

**Solution:**

```tsx
// ✅ DO THIS - Use human-readable string directly
<RozoPayButton
  toUnits="10" // ✅ Human-readable amount as string
/>
```

**Why it happens:** The `toUnits` prop accepts human-readable amounts as strings (e.g., `"10"` for 10 USDC). No `parseFloat()` conversion is needed.

## 🐛 Debugging Tools

### Enable Debug Mode

```tsx
<RozoPayProvider debugMode={true}>{children}</RozoPayProvider>
```

This will log:

- Payment flow steps
- API requests/responses
- Wallet connection status
- Error details

### Browser Developer Tools

1. **Console Logs:**

   - Check for RozoAI debug messages
   - Look for wallet connection errors
   - Monitor network requests

2. **Network Tab:**

   - Verify API calls to `intentapi.rozo.ai`
   - Check for CORS errors
   - Monitor WebSocket connections

3. **Application Tab:**
   - Check localStorage for cached data
   - Verify wallet connection status

### Common Error Messages

| Error                    | Cause                   | Solution                               |
| ------------------------ | ----------------------- | -------------------------------------- |
| `Provider not found`     | Missing RozoPayProvider | Wrap app with providers                |
| `Invalid address format` | Raw string address      | Use `getAddress()` wrapper             |
| `Chain not supported`    | Wrong chain ID          | Use supported chain (8453, 137, 56)    |
| `Token not found`        | Wrong token address     | Verify token address for chain         |
| `Wallet not connected`   | No wallet connection    | User needs to connect wallet           |
| `Payment not updating`   | Missing resetPayment()  | Call resetPayment() when params change |

## 📞 Getting Help

If you're still experiencing issues:

1. **Check Documentation:**

   - [Examples](examples.md) - Working code examples
   - [API Reference](api-reference.md) - Complete prop reference

2. **Community Support:**

   - 💬 **Discord**: [discord.gg/rozoai](https://discord.com/invite/EfWejgTbuU)
   - 🐛 **GitHub Issues**: [GitHub Issues](https://github.com/rozoai/intent-pay/issues)

3. **Direct Support:**
   - 📧 **Email**: [support@rozo.ai](mailto:support@rozo.ai)

When reporting issues, please include:

- Code snippet showing the problem
- Error messages from browser console
- Steps to reproduce the issue
- Framework/version information

## 📖 Next Steps

- [View complete examples](examples.md) for working implementations
- [Check API reference](api-reference.md) for all available options
- [Use AI prompts](ai-prompts.md) for code generation
