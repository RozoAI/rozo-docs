---
description: >-
  ROZO Intent based bridge. One click to bridge from Base to Stellar within few
  seconds.
icon: bridge
---

# Intent Based Bridge

### Fast

It confirms within few seconds.

versus traditional bridges require waiting for 10 minutes bridging.

### One Click&#x20;

It's Intent based with one click.

versus Traditional bridges require users  to perform two separate actions: authorization and execution .



### **Web UI:**&#x20;

{% embed url="https://intents.rozo.ai/" %}

**API Integration** : [https://docs.rozo.ai/api-doc](https://docs.rozo.ai/api-doc)



<figure><img src="../.gitbook/assets/Screenshot 2025-11-29 at 1.43.05 PM.png" alt="" width="375"><figcaption><p>ROZO Intents</p></figcaption></figure>

# Bridge URL Query Parameters

Pre-fill the bridge form by passing query parameters to `/bridge`.

---

## Parameters

| Parameter | Description | Example |
|---|---|---|
| `sourceChain` | Chain to send from | `base`, `stellar`, `arbitrum` |
| `sourceToken` | Token to send | `USDC`, `EURC` |
| `destinationChain` | Chain to receive on | `stellar`, `base`, `polygon` |
| `destinationToken` | Token to receive | `USDC`, `EURC` |
| `amount` | Amount to send (ExactIn) | `10`, `0.5` |
| `destinationAddress` | Pre-fill destination address | EVM or Stellar address |

---

## Supported Chain Values

| Chain | Accepted values |
|---|---|
| Base | `base`, `8453` |
| Stellar | `stellar`, `rozo-stellar` |
| Ethereum | `ethereum`, `eth`, `1` |
| Arbitrum | `arbitrum`, `arb`, `42161` |
| BNB Chain | `bnb`, `bsc`, `56` |
| Polygon | `polygon`, `matic`, `137` |
| Solana | `solana`, `sol` |

Chain values are **case-insensitive**. Numeric chainIds also work.

---

## Examples

**Base USDC -> Stellar USDC, amount 10**
```
/bridge?sourceChain=base&sourceToken=USDC&destinationChain=stellar&destinationToken=USDC&amount=10
```

**Base EURC -> Stellar EURC**
```
/bridge?sourceChain=base&sourceToken=EURC&destinationChain=stellar&destinationToken=EURC&amount=25
```

**Stellar -> Base with destination address pre-filled**
```
/bridge?sourceChain=stellar&destinationChain=base&destinationAddress=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&amount=10
```

**Stellar -> Base, amount only**
```
/bridge?sourceChain=stellar&destinationChain=base&amount=50
```

**Just pre-fill amount (keep default chains)**
```
/bridge?amount=100
```

---

## Rules

- All parameters are **optional** - omitted params keep their default values.
- Unsupported chain names, unknown token symbols, zero/negative/non-numeric amounts, and addresses invalid for the destination chain are **silently ignored**.
- Only `USDC` and `EURC` are supported tokens.
- `USDC -> EURC` and `EURC -> USDC` cross-token routes are **not allowed** - the destination token will be ignored if it conflicts.
- URL params take precedence over the `?currency=EURC` shortcut.
