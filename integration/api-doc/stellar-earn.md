# Stellar Earn

The Stellar Earn API enables integration with DeFindex vault for yield-earning functionality. Users can deposit funds to receive yield-bearing dTokens, or withdraw dTokens to receive USDC on any supported chain.

## Overview

Two intents are available:

| Intent | Description | Source | Destination |
|--------|-------------|--------|-------------|
| `stellar_earn_deposit` | Deposit from any chain, receive dTokens on Stellar | Any chain, any token | Stellar, DTOKEN |
| `stellar_earn_withdraw` | Pay with dTokens on Stellar, receive USDC on any chain | Stellar, DTOKEN | Any chain, USDC |

## DeFindex Vault

- **Vault Address**: `CBNKCU3HGFKHFOF7JTGXQCNKE3G3DXS5RDBQUKQMIIECYKXPIOUGB2S3`
- **dToken**: Vault share token (7 decimals)
- **Underlying Asset**: USDC

---

## stellar_earn_deposit

Deposit from any chain and receive dTokens on Stellar.

### Flow

```
1. User creates payment with intent: "stellar_earn_deposit"
2. User sends USDC/USDT from any chain (Base, Solana, Stellar, etc.)
3. System detects payin
4. System deposits USDC to DeFindex vault
5. System transfers dTokens to user's Stellar address
```

### Request

```bash
curl -X POST https://aozudqtlykbhzbuzalzz.supabase.co/functions/v1/payment-api/payments \
  -H "Content-Type: application/json" \
  -d '{
    "appId": "your-app-id",
    "orderId": "order-123",
    "type": "exactIn",
    "intent": "stellar_earn_deposit",
    "display": {
      "title": "Deposit to Earn",
      "currency": "USD"
    },
    "source": {
      "chainId": "8453",
      "tokenSymbol": "USDC",
      "amount": "100.00"
    },
    "destination": {
      "chainId": "1500",
      "receiverAddress": "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "tokenSymbol": "DTOKEN"
    }
  }'
```

### Parameters

| Field | Required | Description |
|-------|----------|-------------|
| `intent` | Yes | Must be `"stellar_earn_deposit"` |
| `source.chainId` | Yes | Any supported chain |
| `source.tokenSymbol` | Yes | Any supported token (USDC, USDT, etc.) |
| `source.amount` | Yes | Amount to deposit |
| `destination.chainId` | Yes | Must be `"1500"` (Stellar) |
| `destination.receiverAddress` | Yes | Stellar address (G or C) |
| `destination.tokenSymbol` | Yes | Must be `"DTOKEN"` |

### Fee Structure

- Standard fee applies (0.1% or minimum fee)
- Fee is deducted before vault deposit
- Example: 100 USDC in → 0.10 fee → 99.90 USDC deposited → ~99.90 dTokens out

---

## stellar_earn_withdraw

Pay with dTokens on Stellar and receive USDC on any chain.

### Flow

```
1. User creates payment with intent: "stellar_earn_withdraw"
2. User sends dTokens to the provided Stellar address
3. System detects dToken balance
4. System converts dToken to USDC equivalent
5. System applies fee and pays out USDC to destination
```

### Request

```bash
curl -X POST https://aozudqtlykbhzbuzalzz.supabase.co/functions/v1/payment-api/payments \
  -H "Content-Type: application/json" \
  -d '{
    "appId": "your-app-id",
    "orderId": "order-456",
    "type": "anyAmount",
    "intent": "stellar_earn_withdraw",
    "display": {
      "title": "Withdraw from Earn",
      "currency": "USD"
    },
    "source": {
      "chainId": "1500",
      "tokenSymbol": "DTOKEN"
    },
    "destination": {
      "chainId": "8453",
      "receiverAddress": "0x1234567890abcdef1234567890abcdef12345678",
      "tokenSymbol": "USDC"
    }
  }'
```

### Parameters

| Field | Required | Description |
|-------|----------|-------------|
| `intent` | Yes | Must be `"stellar_earn_withdraw"` |
| `type` | Yes | Must be `"anyAmount"` |
| `source.chainId` | Yes | Must be `"1500"` (Stellar) |
| `source.tokenSymbol` | Yes | Must be `"DTOKEN"` |
| `destination.chainId` | Yes | Any supported chain |
| `destination.receiverAddress` | Yes | Address to receive USDC |
| `destination.tokenSymbol` | Yes | Typically `"USDC"` |

### Response

The response includes a Stellar contract address (C...) to send dTokens to:

```json
{
  "success": true,
  "data": {
    "id": "payment-uuid",
    "status": "payment_unpaid",
    "source": {
      "chainId": "1500",
      "tokenSymbol": "DTOKEN",
      "receiverAddress": "CXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    },
    "destination": {
      "chainId": "8453",
      "tokenSymbol": "USDC",
      "receiverAddress": "0x1234..."
    }
  }
}
```

### Fee Structure

- dToken balance is converted to USDC value via DeFindex API
- Standard fee (0.1%) applied to USDC equivalent
- Payout = USDC value - fee
- Example: 100 dTokens (~100 USDC) → 0.10 fee → 99.90 USDC payout

### dToken → USDC Conversion

The conversion rate is determined by the vault's current share price:

```
USDC value = dToken amount × (vault underlying balance / total dToken supply)
```

The rate at payout time is used for conversion.

---

## Supported Chains

### Source Chains (stellar_earn_deposit)

| Chain | Chain ID |
|-------|----------|
| Stellar | 1500 |
| Base | 8453 |
| Polygon | 137 |
| Solana | 900 |
| Ethereum | 1 |
| BNB Chain | 56 |
| Arbitrum | 42161 |

### Destination Chains (stellar_earn_withdraw)

Same as source chains above.

---

## Error Codes

| Code | Description |
|------|-------------|
| `invalidRequest` | Invalid intent or chain/token combination |
| `insufficientLiquidity` | Not enough liquidity for payout |
| `amountTooLow` | Amount below minimum threshold |
| `amountTooHigh` | Amount above maximum threshold |

---

## Notes

1. **dToken Detection**: For `stellar_earn_withdraw`, the system monitors dToken balances on Stellar addresses using the DeFindex vault contract.

2. **Contract Address**: `stellar_earn_withdraw` uses Stellar contract addresses (C...) for receiving dTokens, similar to `stellar_payin_contracts`.

3. **Exchange Rate**: The dToken → USDC rate fluctuates based on vault performance and yield accrual.
