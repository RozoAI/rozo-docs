# Supported Tokens and Chains

### Live supported matrix

The tables on this page are a snapshot. The always-current, machine-readable list is served by the API itself. Use it to populate chain/token pickers instead of hardcoding:

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/supported'
# optional filter: ?provider=rozo | ?provider=near
```

Each entry describes one (chain, token) leg in Rozo's own naming:

```json
{
  "chainId": "42161",
  "chainName": "Arbitrum",
  "chainAliases": ["arb", "arbitrum"],
  "addressFormat": "evm",
  "tokenSymbol": "USDC",
  "providers": ["rozo", "near"],
  "destinationProviders": ["rozo"]
}
```

* `providers`: rails that accept this leg as a **pay-in source**.
* `destinationProviders`: rails that can **pay out to** it. They differ for `near`: it accepts pay-ins from many chains but only settles on Base, Solana and Stellar.
* `destinationMinimumFee`: present only when a per-destination minimum fee applies.
* The top-level `fees` object is the rate card per rail (see [Get Fees](api-for-advanced-used/get-fees.md)).

New chains and tokens appear here automatically as they are enabled. Optimism (`10`) and World Chain (`480`) are not offered: no payout rail exists for them, so orders to them are rejected at creation. See [Routing provider](api-quick-start.md#routing-provider-optional) for how to select a rail.

> **Note on Chain IDs for Solana and Stellar:** For non-EVM chains, the API accepts **either** the numeric chain ID **or** the lowercase chain name string:
> - **Solana**: `900` or `"solana"`
> - **Stellar**: `1500` or `"stellar"`
>
> Both formats are equivalent and interchangeable in all API requests.

### Native coins (beta, invite only)

{% hint style="info" %}
**Beta feature.** Stablecoins (USDC, USDT, EURC) are enabled for every merchant. Native coins are available only to merchants invited by Rozo. Other merchants can request an invitation in partners.rozo.ai.
{% endhint %}

Invited merchants can accept these native coins. The buyer pays in the native coin and the merchant still settles in USDC.

| Coin | Chain | Chain ID |
| --- | --- | --- |
| ETH | Ethereum | `1` |
| ETH | Base | `8453` |
| ETH | Arbitrum | `42161` |
| BNB | BNB Chain | `56` |
| SOL | Solana | `900` |

* Native coins are **off by default** and **invite only**. To ask for an invitation, open [partners.rozo.ai](https://partners.rozo.ai) → Settings → Supported tokens and click Request access. Once Rozo invites the account, the merchant switches each coin on or off on the same page.
* Pay-in only. The quoted amount is locked for 60 minutes and includes a conversion spread.
* During the beta, per-order and daily limits apply. An order above the limit returns `amountTooHigh`; once the daily limit is reached new native orders return `nativePayinPaused`. Stablecoin orders are not affected.
* An order with a native source for a merchant that has not enabled that coin is rejected with `invalidRequest` (`Native <COIN> payin on chain <id> is not enabled for this app`), including dryruns.
* In `GET /payments/supported`, native entries carry `"optIn": true`. Pass your `X-API-Key` or `?appId=<your appId>` to list only the native coins your account can use:

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/supported?appId=<your appId>'
```

* Order responses also include `supportedTokens`; see [API Quick Start (Merchant)](api-quick-start-merchant.md#merchant-info-and-supported-tokens).

### CCTP V2 Domain Aliases

If you're routing via Circle's CCTP V2, you can pass the CCTP domain using the **`cctp:<N>` prefix** and the API will resolve it to the canonical Rozo chain ID before validation.

<table><thead><tr><th width="140">Alias</th><th width="180">Resolves to chainId</th><th>Chain</th></tr></thead><tbody><tr><td><code>cctp:0</code></td><td><code>1</code></td><td>Ethereum</td></tr><tr><td><code>cctp:3</code></td><td><code>42161</code></td><td>Arbitrum</td></tr><tr><td><code>cctp:5</code></td><td><code>900</code></td><td>Solana</td></tr><tr><td><code>cctp:6</code></td><td><code>8453</code></td><td>Base</td></tr><tr><td><code>cctp:7</code></td><td><code>137</code></td><td>Polygon</td></tr><tr><td><code>cctp:27</code></td><td><code>1500</code></td><td>Stellar</td></tr></tbody></table>

**Rules:**
- The `cctp:` prefix is **required**. A bare integer (e.g. `27`) is treated as a literal `chainId` and will return `invalidChainId`.
- Matching is case-insensitive and whitespace-trimmed (`cctp:27`, `CCTP:27`, ` Cctp:27 ` are all equivalent).
- `cctp:25` is **not** aliased: domain `25` belongs to Codex, which is not currently supported.
- `cctp:2` (Optimism) is not aliased: Optimism is not offered.

### Pay In Tokens and Chains

**USDC Support**

<table><thead><tr><th width="118.76953125">Chain ID</th><th width="119.1953125">Chain Name</th><th width="407.73828125">USDC Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>1</code></td><td>Ethereum</td><td><code>0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48</code></td><td>6</td></tr><tr><td><code>42161</code></td><td>Arbitrum</td><td><code>0xaf88d065e77c8cc2239327c5edb3a432268e5831</code></td><td>6</td></tr><tr><td><code>8453</code></td><td>Base</td><td><code>0x833589fcd6edb6e08f4c7c32d4f71b54bda02913</code></td><td>6</td></tr><tr><td><code>56</code></td><td>BSC</td><td><code>0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d</code></td><td>18</td></tr><tr><td><code>137</code></td><td>Polygon</td><td><code>0x3c499c542cef5e3811e1192ce70d8cc03d5c3359</code></td><td>6</td></tr><tr><td><code>999</code></td><td>HyperEVM</td><td><code>0xb88339cb7199b77e23db6e890353e22632ba630f</code></td><td>6</td></tr><tr><td><code>900</code> or <code>solana</code></td><td>Solana</td><td><code>EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v</code></td><td>6</td></tr><tr><td><code>1500</code> or <code>stellar</code></td><td>Stellar</td><td><code>USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN</code></td><td>7</td></tr></tbody></table>

**USDT Support**

<table><thead><tr><th width="103.88671875">Chain ID</th><th width="149.35546875">Chain Name</th><th width="408.99609375">USDT Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>1</code></td><td>Ethereum</td><td><code>0xdac17f958d2ee523a2206206994597c13d831ec7</code></td><td>6</td></tr><tr><td><code>42161</code></td><td>Arbitrum</td><td><code>0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9</code></td><td>6</td></tr><tr><td><code>56</code></td><td>BSC</td><td><code>0x55d398326f99059ff775485246999027b3197955</code></td><td>18</td></tr><tr><td><code>137</code></td><td>Polygon</td><td><code>0xc2132d05d31c914a87c6611c10748aeb04b58e8f</code></td><td>6</td></tr><tr><td><code>900</code> or <code>solana</code></td><td>Solana</td><td><code>Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB</code></td><td>6</td></tr></tbody></table>

USDT on Stellar (asset code `USDT0`) is also accepted as a pay in, in beta. See [USDT on Stellar (beta)](#usdt-on-stellar-beta).

### Pay Out Tokens and Chains

**USDC Support**

<table><thead><tr><th width="118.76953125">Chain ID</th><th width="119.1953125">Chain Name</th><th width="407.73828125">USDC Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>1</code></td><td>Ethereum</td><td><code>0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48</code></td><td>6</td></tr><tr><td><code>42161</code></td><td>Arbitrum</td><td><code>0xaf88d065e77c8cc2239327c5edb3a432268e5831</code></td><td>6</td></tr><tr><td><code>8453</code></td><td>Base</td><td><code>0x833589fcd6edb6e08f4c7c32d4f71b54bda02913</code></td><td>6</td></tr><tr><td><code>56</code></td><td>BSC</td><td><code>0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d</code></td><td>18</td></tr><tr><td><code>137</code></td><td>Polygon</td><td><code>0x3c499c542cef5e3811e1192ce70d8cc03d5c3359</code></td><td>6</td></tr><tr><td><code>999</code></td><td>HyperEVM</td><td><code>0xb88339cb7199b77e23db6e890353e22632ba630f</code></td><td>6</td></tr><tr><td><code>900</code> or <code>solana</code></td><td>Solana</td><td><code>EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v</code></td><td>6</td></tr><tr><td><code>1500</code> or <code>stellar</code></td><td>Stellar</td><td><code>USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN</code></td><td>7</td></tr></tbody></table>

USDT payouts to the chains above are in private beta and are not offered through the public API yet. They are available only inside Rozo's own apps. Orders with a USDT destination from other accounts are rejected at creation. To request access for your integration, see [Contact us](../../contact/contact-us/README.md).

USDT on Stellar (`USDT0`) is the exception: any integration can receive it, in beta. See [USDT on Stellar (beta)](#usdt-on-stellar-beta) below.

### USDT on Stellar (beta)

**Beta feature.** USDT routes are live in beta. Supported pairs, fees and limits may change while the beta runs, and USDT payouts to other chains are private beta (see above).

Rozo bridges Tether's USDT on Stellar to and from USDC and USDT on other chains, so a Stellar wallet can receive USDT that was paid in USDC on Base, or turn its USDT into USDC on Base, Solana or Stellar.

| Chain ID | Chain Name | USDT Asset | Decimals |
| --- | --- | --- | --- |
| `1500` or `stellar` | Stellar | `USDT0:GATISXX6BZ6NC7IKQBY37CJD4SOZL3CYZJWXEDG6JVIY4WBS6KXJHN6Q` | 7 |

On Stellar this asset uses the asset code `USDT0`, so the API token symbol is `"tokenSymbol": "USDT0"` with chain `1500`, on either side of the order. On every other chain use `USDT`. A Stellar receiver must hold a trustline to the asset above.

**Pay in, receive USDT on Stellar**

| Pay in chain | Chain ID | Pay in tokens |
| --- | --- | --- |
| Stellar | `1500` | USDC |
| Base | `8453` | USDC |
| Solana | `900` | USDC, USDT |
| Ethereum | `1` | USDC, USDT |
| BSC | `56` | USDC, USDT |
| Polygon | `137` | USDC, USDT |
| Arbitrum | `42161` | USDC, USDT |

**Pay in USDT on Stellar, receive**

| Payout chain | Chain ID | Payout token |
| --- | --- | --- |
| Stellar | `1500` | USDC |
| Base | `8453` | USDC |
| Solana | `900` | USDC |

USDT on Stellar to USDT on another chain is part of the USDT payout beta above. Any other pair with Stellar USDT on one side, for example Stellar USDT to USDC on Ethereum or BSC, is rejected with `unsupportedRoute`.

**Fees and limits**

* Fee: **0.2%** of the pay in amount, with a **minimum of 0.10 USD** per order. The fee is charged on the source side, so paying 100 USDC returns 99.80 USDT, and paying 10 USDC returns 9.90 USDT. Check the exact amount with a dryrun quote before you create the order.
* Limit: up to **1,000 USD per order** during the beta. Larger orders are rejected with `amountTooHigh`. Split larger amounts into several orders.
* Availability depends on Rozo's liquidity for the payout leg. If a route is temporarily short, the order is rejected at creation with `INSUFFICIENT_LIQUIDITY` and no funds are taken.
* Fees and limits may change during the beta. A quote keeps the fee it was issued with.

### EURC PayIn  & PayOut

(Base and Stellar network)

<table><thead><tr><th width="109.328125">Chain ID</th><th width="119.1953125">Chain Name</th><th width="455.8515625">EURC Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>8453</code></td><td>Base</td><td>0x60a3e35cc302bfa44cb288bc5a4f316fdb1adb42</td><td>6</td></tr><tr><td><code>1500</code> or <code>stellar</code></td><td>Stellar</td><td>EURC:GDHU6WRG4IEQXM5NZ4BMPKOXHW76MZM4Y2IEMFDVXBSDP6SJY4ITNPP2</td><td>7</td></tr></tbody></table>

