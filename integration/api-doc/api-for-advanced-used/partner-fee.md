# Partner Fee

Wallet partners can add their own fee, in basis points, **on top of the Rozo fee**. The fee is deducted from each order created with your API key, recorded per order, and paid out to you in USDC.

Available to **wallet** API accounts (`app_id` starting with `wallet_`). Merchant accounts are the recipient themselves and cannot configure one.

## Set a default rate

In [partners.rozo.ai](https://partners.rozo.ai) → **Settings → Fees**:

| | |
| --- | --- |
| Rate | 0 to 1000 bps (0% to 10%) |
| Payout address | A USDC address on **Base** or **Stellar** (G-account, self-custody only: no memo is sent, so do not use an exchange deposit address) |
| Confirmation | Every save needs a second factor (emailed code for portal accounts, a wallet signature for web3 accounts). Changing the payout address or chain starts a 24h settlement hold |

The rate is **frozen onto each order at creation**. Changing it later never affects existing orders.

## Override per order

Send `partnerFeeBps` (integer 0..1000) in the `POST /payment-api/payments` body to replace the dashboard default for that order only. Use it to tier your own customers, or send `0` when you already take your cut on-chain.

```bash
curl --location --request POST 'https://intentapiv4.rozo.ai/functions/v1/payment-api/payments' \
--header 'X-API-Key: <your api key>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "appId": "wallet_yourapp",
    "type": "anyAmount",
    "partnerFeeBps": 25,
    "source": { "chainId": "1500", "tokenSymbol": "USDC" },
    "destination": {
        "chainId": "1500",
        "tokenSymbol": "USDC",
        "receiverAddress": "G..."
    }
}'
```

A value outside 0..1000 is a `400`. A non-zero value on an account that has not saved a payout address in the dashboard yet is a `400` too. The field is ignored on keyless and merchant orders.

## What the payer sees

Dry-run and create responses carry `source.partnerFee` (in source-token units) and `source.partnerFeeBps` / `feeInfo.partnerFeeBps`, alongside the Rozo `fee`.

| Order type | Effect |
| --- | --- |
| `exactIn` / `anyAmount` | taken from what the recipient receives: `received − rozoFee − partnerFee` |
| `exactOut` | added to what the payer sends: `destination + rozoFee + partnerFee` |

## Scope

The fee applies to orders whose **source token is USDC or USDT** and that settle through the Rozo hub. Native-coin pay-ins (XLM / ETH / SOL / BNB / POL / Lightning), EURC destinations, Stellar USDT0 and Stellar Direct settlements charge `0` for now.

## Settlement

Accrued fees and per-order details are shown under **Settings → Fees**. Settlement is done in USDC to your configured address **on request or monthly**, not per payment; each settlement appears in the settlement history with its transaction hash. USDT-denominated fees accrue per token and are visible in the summary; the first phase settles USDC only.
