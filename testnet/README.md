# Base Sepolia to Stellar Testnet

Use this guide to try a Base Sepolia USDC payment to a Stellar testnet recipient. It covers classic Stellar accounts (`G` addresses) and compatible Soroban contract accounts (`C` addresses). These are test networks: do not send mainnet funds.

## Before you start

- Use a wallet you control on Base Sepolia, with test USDC and test ETH for transaction fees. Test tokens are available from the [Circle USDC faucet](https://faucet.circle.com/) and [Alchemy Base Sepolia faucet](https://www.alchemy.com/faucets/base-sepolia).
- Choose your own Stellar **testnet** recipient. Confirm that it can receive the test USDC asset. A `C` address must identify the intended compatible contract on testnet.
- The documented source amount range is 0.01 to 1.00 test USDC. The order response supplies the actual payment instructions and expiry.
- `display.title` and `display.currency` (`USD`) are required in every create request.
- This endpoint does not require an authentication header. Its test app ID is not a production app registration.

API base URL:

```text
https://intentapitestnet.rozo.ai/functions/v1/payment-api
```

## 1. Create a test order

Replace `YOUR_STELLAR_TESTNET_RECEIVER` with your recipient and choose a unique `orderId` for this test. The placeholder is deliberately not a payable address.

```bash
curl -sS -X POST 'https://intentapitestnet.rozo.ai/functions/v1/payment-api/payments' \
  -H 'Content-Type: application/json' \
  -d '{
    "appId": "testnet-base-to-stellar",
    "orderId": "YOUR_UNIQUE_TEST_ORDER_ID",
    "type": "exactIn",
    "display": {
      "title": "Testnet order",
      "currency": "USD"
    },
    "source": {
      "chainId": "84532",
      "tokenSymbol": "USDC",
      "amount": "0.01"
    },
    "destination": {
      "chainId": "1500",
      "receiverAddress": "YOUR_STELLAR_TESTNET_RECEIVER",
      "tokenSymbol": "USDC"
    }
  }'
```

Save the returned payment `id`. Read `source.receiverAddress`, `source.amount` and `expiresAt` from that response. The required source amount can differ from the amount requested; follow the returned instructions instead of calculating a deposit amount yourself.

## 2. Pay with your test wallet

In your Base Sepolia wallet, send the returned amount of test USDC to the returned source address before the order expires. Check the network and asset before approving the transfer.

Use your wallet's normal signing flow. No private key needs to be pasted into these API requests or shared with Rozo. Do not reuse a deposit address copied from an old order or documentation example.

## 3. Read the result

Replace `YOUR_PAYMENT_ID` with the ID from step 1:

```bash
curl -sS 'https://intentapitestnet.rozo.ai/functions/v1/payment-api/payments/YOUR_PAYMENT_ID'
```

| Testnet `status` | What to do |
| --- | --- |
| `payment_unpaid` | Waiting for the source payment |
| `payment_payin_completed` | Source payment confirmed; keep checking the destination result |
| `payment_completed` | Check the destination amount and transaction against your test order |
| `payment_expired` | If unpaid, create a new order; if you already paid, contact support before sending again |
| `payment_bounced` | Stop and contact support with the payment ID and error details |

A created order or source transaction is not proof of destination delivery. Confirm the resulting transaction on Stellar testnet and the amount credited to your chosen recipient. If an error or interruption leaves the outcome unclear, resume checking the existing order rather than paying again.

## G and C recipient differences

- A classic `G` account receives a Stellar payment operation; its account and asset trustline must be ready to receive the asset.
- A compatible `C` account receives through the Stellar Asset Contract token transfer. Do not use this path for an exchange deposit that requires a classic payment memo.
- If your integration decodes Soroban transaction results itself, use an SDK that supports the transaction metadata returned by the network. A server-side payout error requires Rozo support; your application does not deploy the payout service.

The request selects the recipient through `destination.receiverAddress`. Do not infer support for a particular passkey wallet or contract solely from the address prefix.

## Next steps

See the [Wallet guide](../start/wallets.md) for production integrations and access requirements. Testnet coverage here does not imply testnet support for every Funding, Checkout or MPP feature. For a failed or unclear test, [contact Rozo](../contact/contact-us/README.md) with the payment ID and relevant transaction hashes; never include a private key.
