# Rozo Smart Contract

Rozo Smart Address:  [0x00ec30cbFdbA236b66bF86D485561318eB03F6C1](https://basescan.org/address/0x00ec30cbFdbA236b66bF86D485561318eB03F6C1)

```
interface IRozo {
    struct User {
        uint256 totalCreditUsdCents;      // Total credit limit
        uint256 availableCreditUsdCents;  // Available credit for purchases
        uint256 usedCreditUsdCents;       // Currently used credit
        uint256 score;                    // Cashback points earned
        uint256 balanceUsdCents;          // Current balance
    }


    function withdraw() external;
    function makePurchase(uint256 amountUsdCents, address seller) external;
    function repayCredit(uint256 amountUsdCents) external;

    function users(address user) external view returns (User memory);
} 
```

If user address 0x123456789 is NS members with $20 credit, users\[0x123456789].totalCreditUsdCents = 2000 .&#x20;







