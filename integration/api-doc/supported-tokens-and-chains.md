# Supported Tokens and Chains

> **Note on Chain IDs for Solana and Stellar:** For non-EVM chains, the API accepts **either** the numeric chain ID **or** the lowercase chain name string:
> - **Solana** — `900` or `"solana"`
> - **Stellar** — `1500` or `"stellar"`
>
> Both formats are equivalent and interchangeable in all API requests.

### CCTP V2 Domain Aliases

If you're routing via Circle's CCTP V2, you can pass the CCTP domain using the **`cctp:<N>` prefix** and the API will resolve it to the canonical Rozo chain ID before validation.

<table><thead><tr><th width="140">Alias</th><th width="180">Resolves to chainId</th><th>Chain</th></tr></thead><tbody><tr><td><code>cctp:0</code></td><td><code>1</code></td><td>Ethereum</td></tr><tr><td><code>cctp:3</code></td><td><code>42161</code></td><td>Arbitrum</td></tr><tr><td><code>cctp:5</code></td><td><code>900</code></td><td>Solana</td></tr><tr><td><code>cctp:6</code></td><td><code>8453</code></td><td>Base</td></tr><tr><td><code>cctp:7</code></td><td><code>137</code></td><td>Polygon</td></tr><tr><td><code>cctp:27</code></td><td><code>1500</code></td><td>Stellar</td></tr></tbody></table>

**Rules:**
- The `cctp:` prefix is **required**. A bare integer (e.g. `27`) is treated as a literal `chainId` and will return `invalidChainId`.
- Matching is case-insensitive and whitespace-trimmed (`cctp:27`, `CCTP:27`, ` Cctp:27 ` are all equivalent).
- `cctp:25` is **not** aliased — domain `25` belongs to Codex, which is not currently supported.
- `cctp:2` (Optimism) is not currently aliased and will be enabled separately once Optimism payout support is reviewed.

### Pay In Tokens and Chains

**USDC Support (More chains coming soon)**

<table><thead><tr><th width="118.76953125">Chain ID</th><th width="119.1953125">Chain Name</th><th width="407.73828125">USDC Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>1</code></td><td>Ethereum</td><td><code>0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48</code></td><td>6</td></tr><tr><td><code>42161</code></td><td>Arbitrum</td><td><code>0xaf88d065e77c8cc2239327c5edb3a432268e5831</code></td><td>6</td></tr><tr><td><code>8453</code></td><td>Base</td><td><code>0x833589fcd6edb6e08f4c7c32d4f71b54bda02913</code></td><td>6</td></tr><tr><td><code>56</code></td><td>BSC</td><td><code>0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d</code></td><td>18</td></tr><tr><td><code>137</code></td><td>Polygon</td><td><code>0x3c499c542cef5e3811e1192ce70d8cc03d5c3359</code></td><td>6</td></tr><tr><td><code>999</code></td><td>HyperEVM</td><td><code>0xb88339cb7199b77e23db6e890353e22632ba630f</code></td><td>6</td></tr><tr><td><code>900</code> or <code>solana</code></td><td>Solana</td><td><code>EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v</code></td><td>6</td></tr><tr><td><code>1500</code> or <code>stellar</code></td><td>Stellar</td><td><code>USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN</code></td><td>7</td></tr></tbody></table>

**USDT Support**

<table><thead><tr><th width="103.88671875">Chain ID</th><th width="149.35546875">Chain Name</th><th width="408.99609375">USDT Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>1</code></td><td>Ethereum</td><td><code>0xdac17f958d2ee523a2206206994597c13d831ec7</code></td><td>6</td></tr><tr><td><code>42161</code></td><td>Arbitrum</td><td><code>0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9</code></td><td>6</td></tr><tr><td><code>56</code></td><td>BSC</td><td><code>0x55d398326f99059ff775485246999027b3197955</code></td><td>18</td></tr><tr><td><code>137</code></td><td>Polygon</td><td><code>0xc2132d05d31c914a87c6611c10748aeb04b58e8f</code></td><td>6</td></tr><tr><td><code>900</code> or <code>solana</code></td><td>Solana</td><td><code>Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB</code></td><td>6</td></tr></tbody></table>

### Pay Out Tokens and Chains

**USDC Support (More chains coming soon)**

<table><thead><tr><th width="118.76953125">Chain ID</th><th width="119.1953125">Chain Name</th><th width="407.73828125">USDC Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>1</code></td><td>Ethereum</td><td><code>0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48</code></td><td>6</td></tr><tr><td><code>42161</code></td><td>Arbitrum</td><td><code>0xaf88d065e77c8cc2239327c5edb3a432268e5831</code></td><td>6</td></tr><tr><td><code>8453</code></td><td>Base</td><td><code>0x833589fcd6edb6e08f4c7c32d4f71b54bda02913</code></td><td>6</td></tr><tr><td><code>56</code></td><td>BSC</td><td><code>0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d</code></td><td>18</td></tr><tr><td><code>137</code></td><td>Polygon</td><td><code>0x3c499c542cef5e3811e1192ce70d8cc03d5c3359</code></td><td>6</td></tr><tr><td><code>999</code></td><td>HyperEVM</td><td><code>0xb88339cb7199b77e23db6e890353e22632ba630f</code></td><td>6</td></tr><tr><td><code>900</code> or <code>solana</code></td><td>Solana</td><td><code>EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v</code></td><td>6</td></tr><tr><td><code>1500</code> or <code>stellar</code></td><td>Stellar</td><td><code>USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN</code></td><td>7</td></tr></tbody></table>

**USDT Support**

<table><thead><tr><th width="103.88671875">Chain ID</th><th width="149.35546875">Chain Name</th><th width="408.99609375">USDT Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>1</code></td><td>Ethereum</td><td><code>0xdac17f958d2ee523a2206206994597c13d831ec7</code></td><td>6</td></tr><tr><td><code>42161</code></td><td>Arbitrum</td><td><code>0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9</code></td><td>6</td></tr><tr><td><code>56</code></td><td>BSC</td><td><code>0x55d398326f99059ff775485246999027b3197955</code></td><td>18</td></tr><tr><td><code>137</code></td><td>Polygon</td><td><code>0xc2132d05d31c914a87c6611c10748aeb04b58e8f</code></td><td>6</td></tr></tbody></table>

### EURC PayIn  & PayOut

(Base and Stellar network)

<table><thead><tr><th width="109.328125">Chain ID</th><th width="119.1953125">Chain Name</th><th width="455.8515625">EURC Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>8453</code></td><td>Base</td><td>0x60a3e35cc302bfa44cb288bc5a4f316fdb1adb42</td><td>6</td></tr><tr><td><code>1500</code> or <code>stellar</code></td><td>Stellar</td><td>EURC:GDHU6WRG4IEQXM5NZ4BMPKOXHW76MZM4Y2IEMFDVXBSDP6SJY4ITNPP2</td><td>7</td></tr></tbody></table>

