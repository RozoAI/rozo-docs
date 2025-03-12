# API Doc

We are a contracts built on Base chain. The value are defined in USD in cents. To support users who don't have a EVM wallets, or don't have ETH token on Base, we support a PayMaster mode for user to sign without interaction on Base blockchain.

### Eligible?

Before start integration, please visit [https://rozo.ai/](https://rozo.ai/) and connect with your web3 wallets. You are eligible for BNPL if you have available credit.

<figure><img src="../.gitbook/assets/Screenshot 2025-03-09 at 10.01.11 PM.png" alt=""><figcaption></figcaption></figure>



### Contracts

Rozo Smart Address:  [0x00ec30cbFdbA236b66bF86D485561318eB03F6C1](https://basescan.org/address/0x00ec30cbFdbA236b66bF86D485561318eB03F6C1)

```
interface IRozo {
    struct User 
    function withdraw() external;
    function makePurchase(uint256 amountUsdCents, address seller) external;
    function repayCredit(uint256 amountUsdCents) external;
} 
```



## API Calls and Features

For Buyer: Make a Payment (Sign)

{% embed url="https://docs.rozo.ai/api-doc/make-a-payment-sign" %}

For Seller: Withdraw&#x20;

{% embed url="https://docs.rozo.ai/api-doc/withdraw" %}



