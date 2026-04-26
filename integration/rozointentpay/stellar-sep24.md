# Stellar SEP-24 Support

Use ROZO's Stellar anchor for standard SEP-24 deposit and withdraw flows alongside the ROZO Intent Pay SDK.

## Supported Anchor Hosts

| Environment | Host |
| ----------- | ---- |
| Mainnet     | `anchor.rozo.ai` |
| Testnet     | `testanchor.rozo.ai` |

## Supported Assets

| Network | Asset |
| ------- | ----- |
| Stellar | `USDC` |
| Stellar | `EURC` |

For token identifiers and chain-level details, see [Supported Tokens and Chains](../api-doc/supported-tokens-and-chains.md).

## Endpoint Discovery

ROZO follows the standard Stellar SEP-24 discovery flow. Start from the anchor host and read:

```text
https://anchor.rozo.ai/.well-known/stellar.toml
https://testanchor.rozo.ai/.well-known/stellar.toml
```

Your client should read `TRANSFER_SERVER_SEP0024` from `stellar.toml` instead of hardcoding a transfer server path.

## When To Use SEP-24

Use SEP-24 when your Stellar integration needs an anchor-managed deposit or withdraw flow for supported assets.

Typical cases:

- On-ramp or off-ramp style deposit and withdrawal experiences
- Wallet or app flows that already support the Stellar anchor ecosystem
- Redirect-based deposit and withdraw UX outside the main ROZO payment button flow

Use the main [Quick Start Guide](quick-start.md) when you only need the SDK payment button flow.

## Integration Notes

- Use `anchor.rozo.ai` for production.
- Use `testanchor.rozo.ai` for testing and sandbox environments.
- Supported Stellar assets are currently `USDC` and `EURC`.
- Keep asset code handling explicit in your integration so users cannot accidentally switch between `USDC` and `EURC`.
- If you support both EVM and Stellar destinations in one app, keep your SDK payout config and your SEP-24 anchor config separate.

## Example Discovery Flow

1. Fetch the anchor's `stellar.toml`.
2. Read `TRANSFER_SERVER_SEP0024`.
3. Start the SEP-24 `deposit` or `withdraw` flow for `USDC` or `EURC`.
4. Redirect the user through the anchor flow in your wallet or app UI.
5. Track the transaction state using the anchor response and your app session state.

## Asset Selection Guidance

If your app already uses ROZO Intent Pay for payouts:

- Use the SDK payout config for checkout and direct payment collection.
- Use SEP-24 only for anchor-style deposit and withdraw steps.
- Keep `USDC` and `EURC` as separate user choices in the UI.

## Related Docs

- [Quick Start Guide](quick-start.md)
- [Complete Examples](examples.md)
- [API Reference](api-reference.md)
- [Supported Tokens and Chains](../api-doc/supported-tokens-and-chains.md)
