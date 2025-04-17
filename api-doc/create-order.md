---
description: Create an order to Pay with Rozo
---

# Create Order

If you want to integrate with Rozo payment, please contact @shawnmuggle at discord.

For the API Token and the supported merchant lists.&#x20;



### Create an API Call

```shell
# Curl Command

curl -X POST https://api.rozo.ai/v1/orders \
  -H "Authorization: Bearer XXXXXXXXXXXXXXXXXXX" \
  -H "Content-Type: application/json" \
  -d '{
    "merchantId": "zen",
    "currency": "USD",
    "merchantOrderId": "000001",
    "amount": 0.01,
    "title": "Pizza x 1, Wine x 3, Membership"
  }'


```

### Response

```json
{
  status: 'success',
  message: 'Order created successfully',
  data: {
    order_id: '3ebae269-7f98-4d64-8416-f25de7a171e5',
    merchant_id: 'zen',
    merchant_order_id: 'ZEN-000001',
    amount: 0.01,
    amount_in_usd: 0.01,
    currency: 'USD',
    status: 'pending',
    payment_method: 'ROZO'
  },
  success_url: 'https://payment.link?order_id=123456'
}
```

### Redirect to the payment link

User can login and pay.

### &#x20;

<figure><img src="../.gitbook/assets/Screenshot 2025-04-17 at 9.33.07 AM.png" alt=""><figcaption></figcaption></figure>



