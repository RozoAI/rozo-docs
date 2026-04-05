---
icon: code
---

# dApp Integration

Integrate **Pay with Rozo Wallet** into your dApp using the `window.rozo` provider for gasless USDC transfers on Stellar.

When your dApp is opened inside the Rozo Wallet mobile app, the `window.rozo` provider is automatically injected into the WebView, giving users:

- **Gasless USDC payments** — fees sponsored by OpenZeppelin Relayer
- **Biometric authentication** — Face ID / Touch ID
- **No wallet setup** — the user's Rozo Wallet is ready to go

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Your dApp (WebView)                      │
│                                                              │
│  1. Detect window.rozo                                       │
│  2. Build USDC transfer transaction                          │
│  3. Call window.rozo.signAuthEntry()                         │
└──────────────────────────┬──────────────────────────────────┘
                           │ postMessage
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Rozo Wallet App (Native)                    │
│                                                              │
│  4. Show confirmation modal → User approves                  │
│  5. Biometric authentication → Face ID / Touch ID            │
│  6. Sign with Passkey → Submit to Relayer (gasless!)        │
│  7. Return { hash, status, signedAuthEntry }                 │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Detect Rozo Wallet

```javascript
// Check if window.rozo exists
if (!window.rozo) {
  // Wait for rozo:ready event
  await new Promise((resolve) => {
    window.addEventListener('rozo:ready', resolve, { once: true });
    setTimeout(resolve, 3000);
  });
}

if (!window.rozo) {
  console.log('Not in Rozo Wallet');
  return;
}

// Check connection
const { isConnected } = await window.rozo.isConnected();
if (!isConnected) {
  console.log('Wallet not connected');
  return;
}
```

### 2. Get Wallet Info

```javascript
// Get wallet address
const { address } = await window.rozo.getAddress();
console.log('Wallet:', address); // "CXXX...XXX"

// Get network details
const { network, sorobanRpcUrl, networkPassphrase } =
  await window.rozo.getNetworkDetails();
console.log('Network:', network); // "PUBLIC" or "TESTNET"

// Get balance
const { balance } = await window.rozo.getBalance();
console.log('Balance:', balance); // "10000000" (1.0 USDC in stroops)
```

### 3. Build USDC Transfer Transaction

```javascript
import {
  Account,
  Address,
  Contract,
  nativeToScVal,
  TransactionBuilder,
} from '@stellar/stellar-sdk';
import { Server } from '@stellar/stellar-sdk/rpc';

// USDC contract addresses
const USDC_CONTRACTS = {
  PUBLIC: 'CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75',
  TESTNET: 'CBIELTK6YBZJU5UP2WWQEUCYKLPU6AUNZ2BQ4WWFEIE3USCIHMXQDAMA',
};

// Setup
const server = new Server(sorobanRpcUrl);
const usdcContractId = network === 'PUBLIC'
  ? USDC_CONTRACTS.PUBLIC
  : USDC_CONTRACTS.TESTNET;
const usdcContract = new Contract(usdcContractId);

// Convert amount to stroops (7 decimals)
// "10.50" → 105000000n
function toStroops(amount) {
  const [whole, decimal = ''] = amount.split('.');
  const paddedDecimal = decimal.padEnd(7, '0').slice(0, 7);
  return BigInt(whole + paddedDecimal);
}

const amountStroops = toStroops('10.50');

// Build transfer operation
const hostFunction = usdcContract.call(
  'transfer',
  new Address(fromAddress).toScVal(),
  new Address(toAddress).toScVal(),
  nativeToScVal(amountStroops, { type: 'i128' })
);

// Create dummy source (Relayer will replace this)
const dummySource = new Account(
  'GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF',
  '0'
);

// Build transaction
const tx = new TransactionBuilder(dummySource, {
  fee: '100',
  networkPassphrase,
})
  .addOperation(hostFunction)
  .setTimeout(30)
  .build();
```

### 4. Simulate to Get Auth Entries

```javascript
const simulation = await server.simulateTransaction(tx);

if ('error' in simulation) {
  throw new Error(`Simulation failed: ${simulation.error}`);
}

// Extract auth entries
const authEntries = simulation.result?.auth || [];
if (authEntries.length === 0) {
  throw new Error('No auth entries found');
}

// Convert to XDR (base64)
const authEntryXdr =
  typeof authEntries[0] === 'string'
    ? authEntries[0]
    : authEntries[0].toXDR('base64');
```

### 5. Extract Host Function XDR

```javascript
const txXdr = tx.toEnvelope().v1().tx();
const opXdr = txXdr.operations()[0].body().invokeHostFunctionOp();
const funcXdr = opXdr.hostFunction().toXDR('base64');
```

### 6. Sign and Submit via `window.rozo`

```javascript
const result = await window.rozo.signAuthEntry(authEntryXdr, {
  func: funcXdr,           // Host function XDR (required for submit: true)
  submit: true,            // Submit via Relayer (gasless!)
  message: 'Transfer 10.50 USDC',  // User-facing description
});

console.log('Transaction hash:', result.hash);
console.log('Status:', result.status);
console.log('Signed auth entry:', result.signedAuthEntry);
```

## What Happens in the Wallet

When you call `window.rozo.signAuthEntry()`:

1. **Confirmation Modal** appears showing the description, recipient, amount, and network
2. **User clicks "Confirm"** — or cancels (throws `"User rejected the signing request"`)
3. **Biometric Authentication** — Face ID / Touch ID (cannot be bypassed)
4. **Sign with Passkey** — signs in secure enclave, private key never exposed
5. **Submit to Relayer** (when `submit: true`) — OpenZeppelin Relayer sponsors gas fees
6. **Return Result**:

```javascript
{
  signedAuthEntry: "AAAABg...",  // Signed XDR
  hash: "a1b2c3...",             // Transaction hash
  status: "PENDING"              // Status
}
```

## Complete Example: Vanilla JavaScript

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pay with Rozo Wallet</title>
</head>
<body>
  <div id="app">
    <h1>Coffee Shop</h1>
    <p id="status">Loading...</p>
    <div id="payment-form" style="display: none;">
      <p>Balance: <span id="balance">-</span> USDC</p>
      <input type="number" id="amount" value="5.00" step="0.01" />
      <button id="pay-btn">Pay with Rozo Wallet</button>
    </div>
  </div>

  <script type="module">
    import {
      Account,
      Address,
      Contract,
      nativeToScVal,
      TransactionBuilder,
    } from 'https://cdn.jsdelivr.net/npm/@stellar/stellar-sdk/+esm';
    import { Server } from 'https://cdn.jsdelivr.net/npm/@stellar/stellar-sdk/rpc/+esm';

    const MERCHANT_ADDRESS = 'GDQP2KPQGKIHYJGXNUIYOMHARUARCA7DJT5FO2FFOOUJ3UBSIB3GN5QA';

    const USDC_CONTRACTS = {
      PUBLIC: 'CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75',
      TESTNET: 'CBIELTK6YBZJU5UP2WWQEUCYKLPU6AUNZ2BQ4WWFEIE3USCIHMXQDAMA',
    };

    const statusEl = document.getElementById('status');
    const paymentFormEl = document.getElementById('payment-form');
    const balanceEl = document.getElementById('balance');
    const amountInput = document.getElementById('amount');
    const payBtn = document.getElementById('pay-btn');

    function showStatus(message) {
      statusEl.textContent = message;
    }

    function fromStroops(stroops) {
      const amount = BigInt(stroops);
      const whole = amount / BigInt(10_000_000);
      const decimal = amount % BigInt(10_000_000);
      const decimalStr = decimal.toString().padStart(7, '0');
      return `${whole}.${decimalStr}`.replace(/\.?0+$/, '');
    }

    function toStroops(amount) {
      const [whole, decimal = ''] = amount.split('.');
      const paddedDecimal = decimal.padEnd(7, '0').slice(0, 7);
      return BigInt(whole + paddedDecimal);
    }

    async function transferUSDC(toAddress, amount) {
      showStatus('Preparing transaction...');

      try {
        const { address: fromAddress } = await window.rozo.getAddress();
        const { sorobanRpcUrl, networkPassphrase, network } =
          await window.rozo.getNetworkDetails();

        const server = new Server(sorobanRpcUrl);
        const usdcContractId =
          network === 'PUBLIC' ? USDC_CONTRACTS.PUBLIC : USDC_CONTRACTS.TESTNET;
        const usdcContract = new Contract(usdcContractId);

        const amountStroops = toStroops(amount);

        const hostFunction = usdcContract.call(
          'transfer',
          new Address(fromAddress).toScVal(),
          new Address(toAddress).toScVal(),
          nativeToScVal(amountStroops, { type: 'i128' })
        );

        const dummySource = new Account(
          'GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF',
          '0'
        );

        const tx = new TransactionBuilder(dummySource, {
          fee: '100',
          networkPassphrase,
        })
          .addOperation(hostFunction)
          .setTimeout(30)
          .build();

        showStatus('Simulating transaction...');
        const simulation = await server.simulateTransaction(tx);

        if ('error' in simulation) {
          throw new Error(`Simulation failed: ${simulation.error}`);
        }

        const authEntries = simulation.result?.auth || [];
        if (authEntries.length === 0) {
          throw new Error('No auth entries found');
        }

        const authEntryXdr =
          typeof authEntries[0] === 'string'
            ? authEntries[0]
            : authEntries[0].toXDR('base64');

        const txXdr = tx.toEnvelope().v1().tx();
        const opXdr = txXdr.operations()[0].body().invokeHostFunctionOp();
        const funcXdr = opXdr.hostFunction().toXDR('base64');

        showStatus('Waiting for confirmation...');
        const result = await window.rozo.signAuthEntry(authEntryXdr, {
          func: funcXdr,
          submit: true,
          message: `Transfer ${amount} USDC`,
        });

        if (!result.hash) {
          throw new Error('Transaction submission failed');
        }

        showStatus(`Payment successful! Tx: ${result.hash.slice(0, 8)}...`);
        await refreshBalance();
        return result;
      } catch (error) {
        if (error.message.includes('User rejected')) {
          showStatus('Payment cancelled by user');
        } else {
          showStatus(`Error: ${error.message}`);
        }
        throw error;
      }
    }

    async function refreshBalance() {
      if (!window.rozo) return;
      try {
        const { balance } = await window.rozo.getBalance();
        balanceEl.textContent = fromStroops(balance);
      } catch (error) {
        console.error('Failed to get balance:', error);
      }
    }

    async function init() {
      if (!window.rozo) {
        await new Promise((resolve) => {
          window.addEventListener('rozo:ready', resolve, { once: true });
          setTimeout(resolve, 3000);
        });
      }

      if (!window.rozo) {
        showStatus('Please open this page in the Rozo Wallet app');
        return;
      }

      const { isConnected } = await window.rozo.isConnected();
      if (!isConnected) {
        showStatus('Wallet not connected');
        return;
      }

      const { address } = await window.rozo.getAddress();
      await refreshBalance();

      showStatus('Ready to accept payments');
      paymentFormEl.style.display = 'block';

      payBtn.onclick = async () => {
        const amount = amountInput.value;
        if (!amount || parseFloat(amount) <= 0) {
          alert('Please enter a valid amount');
          return;
        }

        const balance = parseFloat(balanceEl.textContent);
        if (balance < parseFloat(amount)) {
          alert(`Insufficient balance. You have ${balance} USDC.`);
          return;
        }

        payBtn.disabled = true;
        try {
          await transferUSDC(MERCHANT_ADDRESS, amount);
        } finally {
          payBtn.disabled = false;
        }
      };
    }

    init().catch(console.error);
  </script>
</body>
</html>
```

## React Example

```tsx
import { useEffect, useState } from 'react';
import {
  Account,
  Address,
  Contract,
  nativeToScVal,
  TransactionBuilder,
} from '@stellar/stellar-sdk';
import { Server } from '@stellar/stellar-sdk/rpc';

const USDC_CONTRACTS = {
  PUBLIC: 'CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75',
  TESTNET: 'CBIELTK6YBZJU5UP2WWQEUCYKLPU6AUNZ2BQ4WWFEIE3USCIHMXQDAMA',
};

function toStroops(amount: string): bigint {
  const [whole, decimal = ''] = amount.split('.');
  const paddedDecimal = decimal.padEnd(7, '0').slice(0, 7);
  return BigInt(whole + paddedDecimal);
}

function PaymentButton() {
  const [isConnected, setIsConnected] = useState(false);
  const [address, setAddress] = useState<string | null>(null);
  const [balance, setBalance] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function init() {
      if (!window.rozo) return;

      const { isConnected } = await window.rozo.isConnected();
      if (!isConnected) return;

      const { address } = await window.rozo.getAddress();
      const { balance } = await window.rozo.getBalance();

      setIsConnected(true);
      setAddress(address);
      setBalance(balance);
    }

    init();
  }, []);

  async function handlePay() {
    if (!window.rozo) return;

    setIsLoading(true);

    try {
      const { sorobanRpcUrl, networkPassphrase, network } =
        await window.rozo.getNetworkDetails();
      const { address: fromAddress } = await window.rozo.getAddress();

      const server = new Server(sorobanRpcUrl);
      const usdcContractId =
        network === 'PUBLIC' ? USDC_CONTRACTS.PUBLIC : USDC_CONTRACTS.TESTNET;
      const usdcContract = new Contract(usdcContractId);

      const toAddress = 'GDQP2KPQGKIHYJGXNUIYOMHARUARCA7DJT5FO2FFOOUJ3UBSIB3GN5QA';
      const amount = '10.00';
      const amountStroops = toStroops(amount);

      const hostFunction = usdcContract.call(
        'transfer',
        new Address(fromAddress).toScVal(),
        new Address(toAddress).toScVal(),
        nativeToScVal(amountStroops, { type: 'i128' })
      );

      const dummySource = new Account(
        'GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF',
        '0'
      );

      const tx = new TransactionBuilder(dummySource, {
        fee: '100',
        networkPassphrase,
      })
        .addOperation(hostFunction)
        .setTimeout(30)
        .build();

      const simulation = await server.simulateTransaction(tx);

      if ('error' in simulation) {
        throw new Error(`Simulation failed: ${simulation.error}`);
      }

      const authEntries = simulation.result?.auth || [];
      const authEntryXdr =
        typeof authEntries[0] === 'string'
          ? authEntries[0]
          : authEntries[0].toXDR('base64');

      const txXdr = tx.toEnvelope().v1().tx();
      const opXdr = txXdr.operations()[0].body().invokeHostFunctionOp();
      const funcXdr = opXdr.hostFunction().toXDR('base64');

      const result = await window.rozo.signAuthEntry(authEntryXdr, {
        func: funcXdr,
        submit: true,
        message: `Transfer ${amount} USDC`,
      });

      alert(`Success! Transaction: ${result.hash}`);

      const { balance: newBalance } = await window.rozo.getBalance();
      setBalance(newBalance);
    } catch (error) {
      if (!error.message.includes('User rejected')) {
        alert(`Error: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  }

  if (!isConnected) {
    return <div>Open in Rozo Wallet to pay</div>;
  }

  return (
    <div>
      <p>Wallet: {address}</p>
      <p>Balance: {balance ? (BigInt(balance) / 10_000_000n).toString() : '-'} USDC</p>
      <button onClick={handlePay} disabled={isLoading}>
        {isLoading ? 'Processing...' : 'Pay $10 USDC'}
      </button>
    </div>
  );
}

export default PaymentButton;
```

## Key Points

### Always Use `submit: true`

```javascript
await window.rozo.signAuthEntry(authEntryXdr, {
  func: funcXdr,
  submit: true,  // This makes it gasless!
});
```

This submits via OpenZeppelin Relayer, making transactions gasless for users.

### Amount Conversion

USDC on Stellar has **7 decimals**:

| Amount | Stroops |
|--------|---------|
| 1.00 USDC | 10,000,000 |
| 10.50 USDC | 105,000,000 |

```javascript
function toStroops(amount) {
  const [whole, decimal = ''] = amount.split('.');
  const paddedDecimal = decimal.padEnd(7, '0').slice(0, 7);
  return BigInt(whole + paddedDecimal);
}
```

### Error Handling

```javascript
try {
  await window.rozo.signAuthEntry(...);
} catch (error) {
  if (error.message.includes('User rejected')) {
    // User cancelled — don't show error
  } else if (error.message.includes('Insufficient balance')) {
    // Not enough USDC
  } else {
    console.error(error);
  }
}
```

### Network Detection

```javascript
const { network } = await window.rozo.getNetworkDetails();

const usdcAddress = network === 'PUBLIC'
  ? 'CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75'  // Mainnet
  : 'CBIELTK6YBZJU5UP2WWQEUCYKLPU6AUNZ2BQ4WWFEIE3USCIHMXQDAMA'; // Testnet
```

## Testing

1. **Install Rozo Wallet** mobile app (iOS/Android)
2. **Start your dev server** with HTTPS:
   ```bash
   npx ngrok http 3000
   ```
3. **Open your app** in Rozo Wallet's Explore tab
4. **Test on testnet** first before mainnet
