# Data Types & Schemas

## Core Interfaces

### PaymentDisplay

Display information for user interfaces.

```typescript
interface PaymentDisplay {
  intent: string; // Payment description/purpose
  paymentValue: string; // Human-readable amount (e.g., "29.99")
  currency: string; // Currency code (USD, EUR, etc.)
}
```

### PaymentDestination

Where the payment should be sent.

```typescript
interface PaymentDestination {
  destinationAddress?: string; // Recipient wallet address
  chainId: string; // Blockchain network ID
  amountUnits: string; // Amount in smallest token units
  tokenSymbol: string; // Token symbol (USDC, ETH, etc.)
  tokenAddress?: string; // Token contract address
  txHash?: string | null; // Transaction hash (set after payment)
}
```

### PaymentSource

Payment source information.

```typescript
interface PaymentSource {
  sourceAddress?: string; // Sender wallet address
  [key: string]: unknown; // Additional metadata
}
```

### PaymentRequestData

Data required to create a payment.

```typescript
interface PaymentRequestData {
  appId: string; // Your application ID
  display: PaymentDisplay; // Display information
  destination: PaymentDestination; // Payment destination
  externalId?: string; // Your internal reference ID
  metadata?: Record<string, unknown>; // Additional metadata
  preferredChain?: string; // Preferred blockchain
  preferredToken?: string; // Preferred token symbol
  preferredTokenAddress?: string; // Preferred token address
  [key: string]: unknown; // Extensible for future fields
}
```

### PaymentResponseData

Complete payment information from API.

```typescript
interface PaymentResponseData {
  id: string; // Unique payment ID
  status: string; // Payment status (e.g., "payment_unpaid")
  createdAt: string; // ISO timestamp
  display: {
    intent: string; // Payment intent
    currency: string; // Currency (e.g., "USDC")
  };
  source: PaymentSource | null; // Source information (null initially)
  destination: {
    destinationAddress: string; // Recipient address
    txHash: string | null; // Transaction hash (null initially)
    chainId: string; // Chain ID (e.g., "1500" for Stellar)
    amountUnits: string; // Amount in token units
    tokenSymbol: string; // Token symbol
    tokenAddress: string; // Token contract/asset address
  };
  metadata: {
    receivingAddress?: string; // IMPORTANT: Final receiving address
    payinchainid?: string; // Pay-in chain ID
    payintokenaddress?: string; // Pay-in token address
    memo?: string | null; // REQUIRED memo for Stellar and Solana payments
    webhookUrl?: string; // Webhook URL for notifications
    [key: string]: unknown; // Additional metadata
  };
  url: string; // Checkout URL for payment
}
```

### ApiResponse

Standard API response wrapper.

```typescript
interface ApiResponse<T> {
  data: T | null; // Response data
  error: Error | null; // Error information
  status: number | null; // HTTP status code
}
```

### RequestState

Hook state for React components.

```typescript
interface RequestState<T> {
  data: T | null; // Response data
  error: Error | null; // Error information
  status: number | null; // HTTP status
  isLoading: boolean; // Loading state
  isError: boolean; // Error state
  isSuccess: boolean; // Success state
}
```

## Payment Status Values

| Status           | Description                    |
| ---------------- | ------------------------------ |
| `payment_unpaid` | Payment created, awaiting user |
| `processing`     | Payment being processed        |
| `completed`      | Payment successful             |
| `failed`         | Payment failed                 |
| `cancelled`      | Payment cancelled              |
| `expired`        | Payment expired                |

## Chain IDs

Common blockchain network identifiers:

| Chain   | ID     | Name                |
| ------- | ------ | ------------------- |
| Base    | `8453` | Mainnet             |
| Polygon | `137`  | Polygon             |
| BSC     | `56`   | Binance Smart Chain |
| Stellar | `1500` | Stellar Mainnet     |
| Solana  | `900`  | Solana Mainnet      |

## Token Addresses

### USDC Addresses

- Base: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Polygon: `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- Stellar: `USDC:GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN`
- Solana: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

### USDT Address

- BSC: `0x55d398326f99059fF775485246999027B3197955`
