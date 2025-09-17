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

### ❌ Wrong Solana/Stellar Configuration

**Problem:**

```tsx
// ❌ DON'T DO THIS - Wrong chain/token for Solana/Stellar
<RozoPayButton
  appId="rozoDemo"
  toChain={1} // ❌ Wrong chain
  toToken={getAddress("0xA0b86a33...")} // ❌ Wrong token
  toSolanaAddress="DYw8jCTf..."
/>
```

**Solution:**

```tsx
// ✅ DO THIS - Correct Base chain config
<RozoPayButton
  appId="rozoDemo"
  toChain={8453} // ✅ Base chain
  toToken={getAddress(baseUSDC.token)} // ✅ Base USDC
  toAddress={getAddress("0x742d35Cc6634C0532925a3b8D454A3fE1C11C4e2")}
  toSolanaAddress="DYw8jCTf..."
/>
```

**Why it happens:** Solana/Stellar payments require Base chain as settlement layer.

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

| Error                    | Cause                   | Solution                            |
| ------------------------ | ----------------------- | ----------------------------------- |
| `Provider not found`     | Missing RozoPayProvider | Wrap app with providers             |
| `Invalid address format` | Raw string address      | Use `getAddress()` wrapper          |
| `Chain not supported`    | Wrong chain ID          | Use supported chain (8453, 137, 56) |
| `Token not found`        | Wrong token address     | Verify token address for chain      |
| `Wallet not connected`   | No wallet connection    | User needs to connect wallet        |

## 📞 Getting Help

If you're still experiencing issues:

1. **Check Documentation:**

   - [Examples](examples.md) - Working code examples
   - [API Reference](api-reference.md) - Complete prop reference

2. **Community Support:**

   - 💬 **Discord**: [discord.gg/rozoai](https://discord.com/invite/EfWejgTbuU)
   - 🐛 **GitHub Issues**: [GitHub Issues](https://github.com/rozoai/intent-pay/issues)

3. **Direct Support:**
   - 📧 **Email**: support@rozo.ai

When reporting issues, please include:

- Code snippet showing the problem
- Error messages from browser console
- Steps to reproduce the issue
- Framework/version information

## 📖 Next Steps

- [View complete examples](examples.md) for working implementations
- [Check API reference](api-reference.md) for all available options
- [Use AI prompts](ai-prompts.md) for code generation
