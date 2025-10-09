# Make a Payment (Sign)

## 1. Prepare the message

Buyers (from\_address) need to sign a messge to confirm the payments. The message includes the order details.

#### &#x20;Message Contents

```javascript
/*
Amount: 1.00 USD
From: 0xbbca2269b1ebbb859dd4e5f0b024a5b574151b57
To: 0xab47828c07eeea1ecff55baa729da0eb3790f6fb
Time: 2025-03-10T09:04:24.229Z
Order ID: ORDER123
About: Monitor rental for 1 day
*/


// Function to generate the message
function getSignMessage(
    fromAddress: string, 
    toAddress: string, 
    amountUsdCents: number, 
    timestamp: number,
    orderId: string = '',
    about: string = ''
): string {
    const dollars = Math.floor(amountUsdCents / 100);
    const cents = amountUsdCents % 100;
    const amountStr = `${dollars}.${cents.toString().padStart(2, '0')}`;

    return `Amount: ${amountStr} USD
From: ${fromAddress.toLowerCase()}
To: ${toAddress.toLowerCase()}
Time: ${new Date(timestamp).toISOString()}
Order ID: ${orderId}
About: ${about}
`;
}


```



### 2. Sign the Message

```typescript
import { ethers } from 'ethers';
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY_TEST, provider);

// Sign the message - ethers.js will add the prefix internally
const signature = await wallet.signMessage(message);
console.log('\nSignature:', signature);
```

