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





### 3. API Response

payment\_status is the enum \[SUCCESS, EXPIRED, OUT\_OF\_CREDIT]



```
{
    "payment_status": "SUCCESS"
}


SUCCESS: the amount_usd_cents are added to the to_address, which can be withdrawn.
NOT_VALID_SIGN: The signature is not valid
EXPIRED: The signature is expired. The signature is valid for 5 minutes. 
OUT_OF_CREDIT:  the credit is not enough for the payment
```

### 3. API Call

```
Body
API Host: https://api.rozo.ai/v1/sign

Body: 
 {
    from_address
    to_address
    amount_usd_cents
    timestamp
    signature
    order_id
    about
}

Request Body Example:
{
  "from_address": "0xBbCa2269b1EBbB859DD4E5F0b024a5b574151B57",
  "to_address": "0xab47828c07eeea1ecff55baa729da0eb3790f6fb",
  "amount_usd_cents": 100,
  "timestamp": 1741597464229,
  "signature": "0x75cedff072993e4ee929c1077b4334663cce768c43982b95edf0aeed7455c63957ca223dd9ebc6e07e0846af342bf72064b73ae09b55be6702ce1f807c87704e1b",
  "order_id": "ORDER123",
  "about": "Monitor rental for 1 day"
}

```

#### Curl Command

```markup
curl -X POST https://api.rozo.ai/v1/sign \
  -H "Content-Type: application/json" \
  -d '{"from_address":"0xBbCa2269b1EBbB859DD4E5F0b024a5b574151B57","to_address":"0xab47828c07eeea1ecff55baa729da0eb3790f6fb","amount_usd_cents":100,"timestamp":1741597464229,"signature":"0x75cedff072993e4ee929c1077b4334663cce768c43982b95edf0aeed7455c63957ca223dd9ebc6e07e0846af342bf72064b73ae09b55be6702ce1f807c87704e1b","order_id":"ORDER123","about":"Monitor rental for 1 day"}'

```



### 4.  Type Scripts Example

```typescript

import { ethers } from 'ethers';
import dotenv from 'dotenv';

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

async function testSignEndpoint(): Promise<void> {
    try {
        if (!process.env.PRIVATE_KEY_TEST) {
            throw new Error('PRIVATE_KEY_TEST not found in environment variables');
        }
        
        const provider = new ethers.providers.JsonRpcProvider(process.env.PROVIDER_URL || 'http://localhost:8545');
        const wallet = new ethers.Wallet(process.env.PRIVATE_KEY_TEST, provider);
        
        // Test parameters
        let fromAddress = await wallet.getAddress();
        const toAddress = "0xab47828c07eeea1ecff55baa729da0eb3790f6fb";
        const amountUsdCents = 100; // $1.00
        const timestamp = Date.now();
        const orderId = "ORDER123";  // Add order ID
        const about = "Monitor rental for 1 day";  // Add about text

        // Get the message to sign
        const message = getSignMessage(fromAddress, toAddress, amountUsdCents, timestamp, orderId, about);
        console.log('\nMessage to sign:');
        console.log(message);

        // Sign the message - ethers.js will add the prefix internally
        const signature = await wallet.signMessage(message);
        console.log('\nSignature:', signature);

        // Prepare the request body
        const requestBody = {
            from_address: fromAddress,
            to_address: toAddress,
            amount_usd_cents: amountUsdCents,
            timestamp,
            signature,
            order_id: orderId,  // Add to request body
            about: about  // Add to request body
        };

        console.log('\nRequest body:');
        console.log(JSON.stringify(requestBody, null, 2));


        // Make the actual request using fetch
        const response = await fetch('http://localhost:3000/v1/sign', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        const result = await response.json();
        console.log('\nAPI Response:');
        console.log(JSON.stringify(result, null, 2));

    } catch (error) {
        console.error('Error:', error);
    }
}

// Run if called directly
if (require.main === module) {
    dotenv.config();
    testSignEndpoint();
}

export default testSignEndpoint; 

```



