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

| Coin | Chain | Chain ID | Minimum pay-in | Status |
| --- | --- | --- | --- | --- |
| ETH | Ethereum | `1` | 1.00 USD | Beta |
| ETH | Base | `8453` | 0.10 USD | Beta |
| ETH | Arbitrum | `42161` | 0.10 USD | Beta |
| BNB | BNB Chain | `56` | 0.10 USD | Beta |
| SOL | Solana | `900` | 1.00 USD | Beta |
| POL | Polygon | `137` | 0.10 USD | Beta |

* The minimum is the USD value of the order, priced from the coin at quote time. An order below it is rejected with `amountTooLow` (`Minimum for <COIN> payins on chain <id> is $<min>`). Ethereum and Solana have a higher minimum because each pay-in costs more in network fees on those chains.

* Native coins are **off by default** and **invite only**. To ask for an invitation, open [partners.rozo.ai](https://partners.rozo.ai) → Settings → Supported tokens and click Request access. Once Rozo invites the account, the merchant switches each coin on or off on the same page.
* Pay-in only. The quoted amount is locked for 60 minutes and includes a conversion spread.
* During the beta, per-order and daily limits apply. An order above the limit returns `amountTooHigh`; once the daily limit is reached new native orders return `nativePayinPaused`. Stablecoin orders are not affected.
* An order with a native source for a merchant that has not enabled that coin is rejected with `invalidRequest` (`Native <COIN> payin on chain <id> is not enabled for this app`), including dryruns.
* In `GET /payments/supported`, native entries carry `"optIn": true`. Pass your `X-API-Key` or `?appId=<your appId>` to list only the native coins your account can use:

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/supported?appId=<your appId>'
```

* Order responses also include `supportedTokens`; see [API Quick Start (Merchant)](api-quick-start-merchant.md#merchant-info-and-supported-tokens).

#### How native-coin conversion works

Nothing changes on the partner side. The flow for a native-coin order:

1. The buyer sends the native coin to the order's deposit address. It arrives at the Rozo hub on the same chain.
2. Rozo converts it to USDC on that chain. ETH and SOL are converted through NEAR Intents. BNB on BNB Chain and POL on Polygon are converted through Rozo's own bridge and a DEX.
3. The partner is settled in USDC exactly as for a stablecoin order: same payout, same webhooks, same settlement time.

The partner never holds the volatile coin, and no extra integration work or action is needed. The conversion spread is already in the quoted amount the buyer pays.

### Gas drop add-on (beta)

{% hint style="info" %}
**Beta feature.** Gas drop is enabled per account on request. Other accounts get `"available": false` with `"reason": "app_not_allowed"` and an otherwise unchanged response. To request it, see [Contact us](../../contact/contact-us/README.md).
{% endhint %}

The payer can add a small amount of the destination chain's gas coin to an order that pays out USDC, so the receiving wallet can move its USDC right away. For example, an order paying out USDC on Arbitrum can also deliver a little ETH on Arbitrum.

Gas drop is separate from native-coin pay-ins. It is offered only when all of these hold:

* The order pays in USDC or USDT and pays out USDC.
* The order type is `exactIn` or `exactOut`.
* The order is routed by Rozo (`provider` is `rozo`).

It is not available on native-coin pay-ins (ETH, BNB, SOL, POL) or on orders routed through NEAR Intents. Those return `"available": false` with `"reason": "token"` or `"reason": "route"`.

Request it with `options.gasDrop` on a dryrun or a create:

```json
"options": {
  "gasDrop": { "enabled": true, "amountUsd": "1" }
}
```

| Setting | Value |
| --- | --- |
| Minimum | 0.10 USD (Ethereum: 1.00 USD) |
| Maximum | 10.00 USD |
| Step | 0.10 USD |
| Spread | 5% of the gas drop amount |
| Gas coin by destination chain | ETH on Ethereum, Base and Arbitrum; BNB on BNB Chain; POL on Polygon; SOL on Solana; XLM on Stellar; HYPE on HyperEVM |

* `amountUsd` is what the payer gives up for the gas coin. On `exactIn` it comes out of the USDC payout; on `exactOut` it is added to the pay-in.
* An amount outside the range or off the 0.10 USD step returns `"available": false` with `"reason": "amount_out_of_range"`.
* At quote time a refused gas drop only removes the add-on: the quote is returned without it and the rest is unchanged.
* At order creation the gas coin is reserved for the order. If that reservation fails, for example because the gas inventory ran out after the quote, the API returns HTTP `409` with `gasDropUnavailable` and **the order is not created**. Request a new quote; it will show whether the gas drop is still available.
* The response `gasDrop` block shows `amountNative`, `chargedUsd`, `feeUsd` (the spread) and `principalUsd`. Example for 1 USD to Arbitrum: `chargedUsd` 1.00, `feeUsd` 0.05, `principalUsd` 0.95, delivered as ETH at the quoted price.
* The gas coin is sent after the USDC payout completes.

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

#### USDT on BNB Chain to USDC on Stellar

USDT on BNB Chain (BSC, chain `56`) can be paid in and settled as USDC on Stellar (`1500`). This is a standard route, available to every integration.

| | Value |
| --- | --- |
| Pay in | USDT on BSC, `0x55d398326f99059ff775485246999027b3197955`, **18 decimals** |
| Pay out | USDC on Stellar, `USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN`, 7 decimals |
| Fee on Rozo's rail | **0.2%** of the amount (any order with USDT on either side), minimum per your app tier (public default $0.01). Your partner fee, if any, is added on top |
| Fee on NEAR Intents | flat 0.3%, minimum $0.01 (see [Get Fees](api-for-advanced-used/get-fees.md)) |
| Example | 100 USDT on BSC pays out 99.80 USDC on Stellar on Rozo's rail (fee $0.20) |
| Ways to integrate | [Payment API](api-quick-start.md) order, [Wallet Top-up](api-for-advanced-used/wallet-topup.md) (`anyAmount`), or a fixed [Wallet Deposit](deposit-api.md) address |
| Limits | Wallet Top-up: minimum $0.02, maximum **TBD before publish**. Wallet Deposit: no fixed minimum; a deposit not larger than its fee is not paid out |

The Stellar receiving account must hold a USDC trustline. The Wallet Deposit API does not send a memo, so do not use it for an exchange deposit account that needs one. Always read the exact fee from the dry-run or created order.

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
* Limit: up to **10,000 USD per order** during the beta. Larger orders are rejected with `amountTooHigh`. Split larger amounts into several orders.
* Availability depends on Rozo's liquidity for the payout leg. If a route is temporarily short, the order is rejected at creation with `INSUFFICIENT_LIQUIDITY` and no funds are taken.
* Fees and limits may change during the beta. A quote keeps the fee it was issued with.

### TRON USDT to Stellar USDC (invited beta)

{% hint style="info" %}
**Beta feature, invite only.** This route is available only to apps that Rozo has invited and approved. Other apps get HTTP `403`. Fees, limits and the minimum may change while the beta runs. To request access, see [Contact us](../../contact/contact-us/README.md).
{% endhint %}

The payer sends USDT on TRON to a payment address issued for one order. Rozo confirms the transfer on chain and pays USDC on Stellar to the receiving account approved for your app.

| Side | Chain | Chain ID | Token | Asset | Decimals |
| --- | --- | --- | --- | --- | --- |
| Pay in | TRON | `728126428` or `tron` | USDT (TRC20) | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | 6 |
| Pay out | Stellar | `1500` or `stellar` | USDC | `USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN` | 7 |

This route is not listed in `GET /payments/supported`. TRON is not a pay-out chain, and Stellar to TRON is not offered.

#### Who can use it

* Apps with an `X-API-Key` that Rozo has invited to this beta.
* Each invited app pays out to **one fixed Stellar receiving account and one fixed memo** (or no memo), approved by Rozo before access is switched on. A request with any other receiving account or memo is refused with `403` `destination_not_approved` or `memo_mismatch` (after release). Per-user memos on a shared account are not supported in this beta.
* The receiving account must already exist and hold an authorized USDC trustline to the issuer above. Otherwise the payment option is refused with `422` `trustline_missing` and no payment address is issued (after release).

To request access, contact us with your `appId`, the Stellar receiving account, the memo (or "no memo") and your expected order size and daily volume.

#### Fees and limits

* Minimum order: **TBD before publish**.
* Maximum per order and per day for your app: **TBD before publish**. An order above your app's per-order or daily limit returns `422` `beta_limit` (after release). Rozo's overall limits for TRON also apply: an order above them returns `422` `order_cap_exceeded`, and once the overall daily limit is reached new orders return `422` `daily_budget_exhausted` until the next UTC day.
* Fee: a Rozo service fee of a dynamic rate with a 0.20% floor and a $0.50 minimum, plus your partner fee if configured (see [Partner Fee](api-for-advanced-used/partner-fee.md)). Rozo calculates the fee on the server (after release). The payer sends the USDC amount to be received plus these fees, rounded up to the cent. The response shows the exact amount to send.
* Each order reserves USDC on Stellar for the payout when the payment option is created. If Rozo cannot reserve it, the API returns `422` `inventory_unavailable` and no payment address is issued (after release). Try again later or offer another payment method.

#### How to integrate

The flow has two calls. First create the order on the Payment API. Then ask for the TRON payment option for that order.

**1. Create the order**

Create an `exactOut` order that pays USDC on Stellar (`1500`), with `"provider": "rozo"` set explicitly. `orderId` is your own unique reference. `destination.amount` is the USDC amount the receiving account gets, with at most 6 decimals. `receiverAddress` and `receiverMemo` must be the receiving account and memo approved for your app; omit `receiverMemo` if your app was approved with no memo. Do not send `metadata.original` (if you send it, it must equal `destination.amount`).

The Payment API does not accept TRON as a source, so set the source to USDC on Base (`8453`). The order gets its own Base deposit address as usual. Do not show that address to the payer: the payer pays only the TRON option from step 2.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "<your appId>",
    "orderId": "<your order reference>",
    "type": "exactOut",
    "provider": "rozo",
    "display": { "title": "TRON USDT to Stellar USDC", "currency": "USD" },
    "source": { "chainId": "8453", "tokenSymbol": "USDC" },
    "destination": {
        "chainId": "1500",
        "tokenSymbol": "USDC",
        "receiverAddress": "<your approved Stellar account>",
        "receiverMemo": "<your approved memo, omit if none>",
        "amount": "100.00"
    }
}'
```

An order that does not exist, is not `exactOut`, has an amount with more than 6 decimals, is routed to a provider other than Rozo, or carries a native coin, `USDT0` or exchange quote lock is refused at the next step with `409` `beta_unsupported_order` (after release). An order that is already paid or closed is refused with `409` `order_not_open`. If your app has a partner fee, it must be in USDC or USDT and equal the configured rate on the net amount, rounded up to 4 decimals; otherwise the request is refused with `409` `pilot_partner_fee_invalid` or `pilot_partner_fee_mismatch` (after release).

**2. Get the TRON payment option**

Send the same `orderId` as `merchantOrderId`. `baseServiceUsd` must equal the USDC amount of the order (`destination.amount`), not the amount including fees. `existingAppFeeUsd` is optional for invited beta apps and is ignored if sent, because Rozo calculates the fee on the server (after release).

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/tron-ton-alpha' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "merchantOrderId": "<your order reference>",
    "baseServiceUsd": 100,
    "network": "tron",
    "token": "USDT"
}'
```

Example response (values are illustrative, for an app with no partner fee):

```json
{
  "orderId": "<your order reference>",
  "reused": false,
  "chainId": "728126428",
  "network": "tron",
  "tokenSymbol": "USDT",
  "tokenIdentity": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
  "tokenDecimals": 6,
  "receivingAddress": "T...",
  "expectedAmount": "100.50",
  "expectedAmountAtomic": "100500000",
  "grossUsd": "100.50",
  "expiresAt": "2026-01-01T01:00:00Z",
  "poolAddress": true,
  "notice": "Alpha: the payment is verified on chain and the top-up is delivered automatically. Each order has its own address. Do not copy an address from your wallet history."
}
```

Show the payer `receivingAddress` and `expectedAmount`. Calling the same request again for the same order returns the same option with `"reused": true`; it does not issue a new address or amount. Sending the same `merchantOrderId` with different values returns `409` `order_conflict`.

#### Settlement conditions

* Send **exactly** `expectedAmount` of USDT on TRON to `receivingAddress` before `expiresAt`. The payment window is 60 minutes. When paying from an exchange, add the exchange's withdrawal fee on top so that the exact amount arrives.
* Use the address from this order's response only. Do not copy an address from wallet history.
* After the transfer is confirmed on chain, the order moves to `payment_payin_completed` and the USDC payout to Stellar starts.
* If the order's Base deposit address is also paid, the order settles as a normal Base to Stellar order and the TRON payment is held as a duplicate for manual review.
* A transfer outside a small tolerance of `expectedAmount`, a transfer after the window has closed, or a second payment for an order that is already paid is not paid out automatically. The funds are held and reviewed by Rozo. Contact us with the TRON transaction hash.
* After expiry the same request returns `410` `order_expired`. Create a new order.

#### Check the status

```bash
curl 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/order/<your appId>/<your order reference>' \
--header 'X-API-Key: <your api key>'
```

Or by payment id: `GET /payment-api/payments/{id}`. Treat the order as settled only at raw `status` `payment_payout_completed`, and reconcile the Stellar transaction. See [status and reconciliation](merchant-api-keys.md#reading-order-status).

#### Errors

| HTTP | `error` | Meaning |
| --- | --- | --- |
| `401` | `unauthorized` | Missing, unknown or expired API key |
| `403` | `alpha_disabled`, `app_not_allowed` | The route is off, or your app is not invited |
| `403` | `destination_not_approved`, `memo_mismatch` | The order does not pay the approved account or memo (after release) |
| `400` | `bad_request`, `unsupported_asset` | Missing fields, or a network/token other than TRON USDT |
| `409` | `order_conflict` | Same order reference sent with different values |
| `409` | `beta_unsupported_order` | The order does not exist, is not a Rozo `exactOut` order to Stellar USDC, carries a native, `USDT0` or exchange quote lock, or its amount does not match `baseServiceUsd` (after release) |
| `409` | `order_not_open` | The order is already paid or closed (after release) |
| `409` | `pilot_partner_fee_invalid`, `pilot_partner_fee_mismatch` | The partner fee is not in USDC or USDT, or does not match the configured rate on the net amount (after release) |
| `410` | `order_expired` | The payment window closed |
| `422` | `beta_limit` | Above your app's per-order or daily limit (after release) |
| `422` | `order_cap_exceeded`, `daily_budget_exhausted` | Above Rozo's overall TRON limits |
| `422` | `inventory_unavailable` | No USDC can be reserved on Stellar now (after release) |
| `422` | `trustline_missing` | The receiving account does not exist or has no authorized USDC trustline (after release) |
| `503` | `stellar_check_unavailable` | The Stellar account check could not run. Try again later (after release) |
| `503` | `pool_exhausted` (with `"hideOption": true`) | No TRON payment address is free right now. Hide the TRON option and offer another method |

### EURC PayIn  & PayOut

(Base and Stellar network)

<table><thead><tr><th width="109.328125">Chain ID</th><th width="119.1953125">Chain Name</th><th width="455.8515625">EURC Token Address</th><th>Decimals</th></tr></thead><tbody><tr><td><code>8453</code></td><td>Base</td><td>0x60a3e35cc302bfa44cb288bc5a4f316fdb1adb42</td><td>6</td></tr><tr><td><code>1500</code> or <code>stellar</code></td><td>Stellar</td><td>EURC:GDHU6WRG4IEQXM5NZ4BMPKOXHW76MZM4Y2IEMFDVXBSDP6SJY4ITNPP2</td><td>7</td></tr></tbody></table>

