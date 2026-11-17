---
icon: code
---

# dApp Integration

Integrate **Pay with Rozo Wallet** into your dApp using the `window.rozo` provider for gasless USDC transfers on Stellar.

When a page is opened in the in-app browser of the Rozo Wallet mobile app, the app injects the `window.rozo` provider into the WebView, giving users:

- **Gasless USDC payments**: fees sponsored by OpenZeppelin Relayer
- **Passkey verification**: Face ID / Touch ID
- **No wallet setup**: the user's Rozo Wallet is ready to go

## Availability

- The provider is available only to pages served from `rozo.ai` or a subdomain of `rozo.ai` (for example `https://<name>.rozo.ai`). Pages on any other domain do not receive `window.rozo`, and requests from them are rejected with the error code `UNTRUSTED_ORIGIN`.
- The provider exists only inside the mobile app's in-app browser. It is not available in the web version of Rozo Wallet or in a regular mobile browser.
- The network (`PUBLIC` or `TESTNET`) is fixed by the app build. Read it with `getNetwork()` or `getNetworkDetails()`; a dApp cannot switch it.

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
│  4. Passkey verification → Face ID / Touch ID                │
│  5. Sign with Passkey → Submit to Relayer (gasless!)         │
│  6. Return { signedAuthEntry, signerAddress, hash, status }  │
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

// Get balances (strings, in stroops: 7 decimals)
const { usdc, eurc } = await window.rozo.getBalance();
console.log('USDC:', usdc); // "10000000" (1.0 USDC)
console.log('EURC:', eurc); // "0"
```

`getBalance()` also returns `balance`, which equals `usdc` and is kept for backward compatibility. Use `usdc` in new code.

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
});

if (result.status !== 'SUCCESS') {
  throw new Error(result.error || 'Transaction submission failed');
}

console.log('Transaction hash:', result.hash);
console.log('Signed auth entry:', result.signedAuthEntry);
```

## What Happens in the Wallet

When you call `window.rozo.signAuthEntry()`:

1. **Passkey verification**: the user verifies with Face ID / Touch ID. Cancelling rejects the call with a `PASSKEY_CANCELLED` or `USER_CANCELLED` error code.
2. **Sign with Passkey**: the passkey signs the auth entry; the private key is never exposed.
3. **Submit to Relayer** (when `submit: true` and `func` is provided): OpenZeppelin Relayer sponsors the fees.
4. **Return Result**:

```javascript
{
  signedAuthEntry: "AAAABg...",  // Signed auth entry XDR
  signerAddress: "CXXX...XXX",   // The wallet's contract address
  hash: "a1b2c3...",             // Transaction hash (only when status is "SUCCESS")
  status: "SUCCESS",             // "SUCCESS" or "FAILED"; absent when submit was not requested
  error: undefined               // Relayer error message (only when status is "FAILED")
}
```

If the relayer rejects the submission, the call still resolves with the signed entry, `status: "FAILED"` and `error`. If `submit: true` is passed without `func`, the entry is signed but not submitted, and `hash` and `status` are absent.

## Provider API Reference

All methods except `on()` and `off()` return Promises; `on()` and `off()` return nothing. Read methods time out after 10 seconds and signing methods after 120 seconds (error code `TIMEOUT`).

| Method | Returns | User prompt |
|--------|---------|-------------|
| `isConnected()` | `{ isConnected }` | None |
| `getAddress()` | `{ address }`, the wallet's contract (`C...`) address | None |
| `getPublicKey()` | `{ publicKey }` | None |
| `getNetwork()` | `{ network, networkPassphrase }`; `network` is `"PUBLIC"` or `"TESTNET"` | None |
| `getNetworkDetails()` | `{ network, networkUrl, networkPassphrase, sorobanRpcUrl }` | None |
| `getBalance()` | `{ usdc, eurc, balance }`, strings in stroops; `balance` equals `usdc` (legacy) | None |
| `getActiveCurrency()` | `{ currency }`, `"USDC"` or `"EURC"`, the user's display currency | None |
| `signAuthEntry(authEntryXdr, opts)` | `{ signedAuthEntry, signerAddress, hash?, status?, error? }` | Requires passkey verification |
| `signTransaction(xdr, opts)` | `{ signedTxXdr, signerAddress, operationXDR?, hash?, status? }` | Requires passkey verification |
| `signMessage(message, opts)` | `{ signedMessage, signerAddress }` | Confirmation dialog, then passkey verification |
| `on(event, callback)` / `off(event, callback)` | Registers or removes a listener for `connect`, `disconnect`, `accountChanged` or `networkChanged` | None |

### `signAuthEntry` options

| Option | Description |
|--------|-------------|
| `func` | Host function XDR (base64). Required for submission. |
| `submit` | `true` to submit through the relayer after signing. |
| `address` | Optional. The wallet signs with its own address. |
| `paymentId`, `fromAddress`, other fields | Optional. Fields other than `authEntryXdr`, `func`, `submit`, `address` and `message` are forwarded to the relayer request body. `message` is ignored. |

### `signTransaction` options

`signTransaction(xdr, { submit: true })` expects a transaction with a single invoke host function operation that includes an auth entry for this wallet. The wallet signs its auth entries and submits that operation's host function through the relayer. On success it returns `hash` and `status: "SUCCESS"`; a relayer failure rejects the call. If no auth entry in the transaction belongs to the wallet, nothing is signed or submitted and the call returns `signedTxXdr` (the transaction as passed in) without `status`. Without `submit`, `signedTxXdr` is also the transaction as passed in. Always check `status === "SUCCESS"` before treating the payment as sent.

### `signMessage`

`signMessage(message)` shows a confirmation dialog with the message, then asks for passkey verification. `signedMessage` is the passkey signature as a hex string. Declining the dialog rejects with the error code `USER_REJECTED`.

### Events

`on()` and `off()` accept the provider event names above, but the current app version does not emit them. Use the DOM events below instead.

The wallet dispatches these DOM events on `window`:

| Event | When | `event.detail` |
|-------|------|----------------|
| `rozo:ready` | Once the provider is injected, and again after the page finishes loading | `{ provider }`; the second dispatch also includes the `rozo:state` fields |
| `rozo:state` | After the page finishes loading | `{ isConnected, isDeployed, address, usdc, eurc, balance }` |

Listening for `rozo:state` lets a page show the address and balances without calling `isConnected()`, `getAddress()` and `getBalance()` in sequence:

```javascript
window.addEventListener('rozo:state', (event) => {
  const { isConnected, isDeployed, address, usdc } = event.detail;
  // usdc is null when the wallet is not deployed yet
});
```

### Errors

Rejected calls throw an `Error` with a machine readable `code`, a user facing `message` and, for some errors, a `recoverySuggestion`. Branch on `code`, not on `message`. Common codes:

| Code | Meaning |
|------|---------|
| `USER_REJECTED`, `USER_CANCELLED`, `PASSKEY_CANCELLED` | The user declined or cancelled |
| `WALLET_NOT_CONNECTED` | No wallet is signed in to the app |
| `WALLET_NOT_DEPLOYED` | The wallet contract is not deployed yet (checked before any `submit: true` call) |
| `INSUFFICIENT_BALANCE` | Not enough balance |
| `SIMULATION_FAILED`, `SUBMISSION_FAILED`, `SIGNING_FAILED`, `AUTHORIZATION_FAILED` | The transaction could not be signed or submitted |
| `TIMEOUT` | No response within the method's timeout |
| `UNTRUSTED_ORIGIN` | The page is not on `rozo.ai` or a `rozo.ai` subdomain |
| `BRIDGE_NOT_AVAILABLE` | The page is not running inside the Rozo Wallet app |
| `UNKNOWN_ERROR` | Anything else |

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

    const MERCHANT_ADDRESS = 'YOUR_MERCHANT_STELLAR_ADDRESS'; // G... or C... address

    const USDC_CONTRACTS = {
      PUBLIC: 'CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75',
      TESTNET: 'CBIELTK6YBZJU5UP2WWQEUCYKLPU6AUNZ2BQ4WWFEIE3USCIHMXQDAMA',
    };

    const CANCEL_CODES = ['USER_REJECTED', 'USER_CANCELLED', 'PASSKEY_CANCELLED'];

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

        showStatus('Waiting for passkey verification...');
        const result = await window.rozo.signAuthEntry(authEntryXdr, {
          func: funcXdr,
          submit: true,
        });

        if (result.status !== 'SUCCESS') {
          throw new Error(result.error || 'Transaction submission failed');
        }

        showStatus(`Payment successful! Tx: ${result.hash.slice(0, 8)}...`);
        await refreshBalance();
        return result;
      } catch (error) {
        if (CANCEL_CODES.includes(error.code)) {
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
        const { usdc } = await window.rozo.getBalance();
        balanceEl.textContent = fromStroops(usdc);
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

const CANCEL_CODES = ['USER_REJECTED', 'USER_CANCELLED', 'PASSKEY_CANCELLED'];

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
      const { usdc } = await window.rozo.getBalance();

      setIsConnected(true);
      setAddress(address);
      setBalance(usdc);
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

      const toAddress = 'YOUR_MERCHANT_STELLAR_ADDRESS'; // G... or C... address
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
      });

      if (result.status !== 'SUCCESS') {
        throw new Error(result.error || 'Transaction submission failed');
      }

      alert(`Success! Transaction: ${result.hash}`);

      const { usdc: newBalance } = await window.rozo.getBalance();
      setBalance(newBalance);
    } catch (error) {
      if (!CANCEL_CODES.includes(error.code)) {
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
  if (['USER_REJECTED', 'USER_CANCELLED', 'PASSKEY_CANCELLED'].includes(error.code)) {
    // User cancelled: don't show an error
  } else if (error.code === 'INSUFFICIENT_BALANCE') {
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
2. **Serve your page over HTTPS from `rozo.ai` or a `rozo.ai` subdomain.** Pages on other domains, including local tunnels, do not receive `window.rozo` (see [Availability](#availability)).
3. **Open the page inside the app**, for example by scanning a QR code of its URL with the in-app scanner, or from a link in the Discover tab.
4. **Check the network** with `getNetwork()` before sending funds, and test with small amounts first.
