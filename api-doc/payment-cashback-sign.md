# Payment (Cashback Sign)

## Prepare the message

Buyers (from\_address) need to sign a messge to confirm the payments. The message includes the order details.





### 1. API Call

```
Body
API Host: https://api.rozo.ai/v1/cashbacksign



```

#### Curl Command

```shellscript
curl -X POST https://api.rozo.ai/v1/cashbacksign \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": "0x1234",
    "to_handle": "cafeshop",
    "amount_usd_cents": 23,
    "amount_local": 1,
    "currency_local": "MYR",
    "timestamp": 1742621218673,
    "order_id": "20250322001",
    "about": "Cafe Latte",
    "signature": "xxxxxxxxxxxx"
  }'
```

````markup
```
 {
  "from_address": "    ",
  "to_handle": "nscafe",
  "amount_usd_cents": 23,
  "amount_local": 1,
  "currency_local": "MYR",
  "timestamp": 1741597464229,
  "order_id": "20250322001",
  "about": "NS Cafe Latte",
  "signature": "XXXXXXXX"
}

{
  "status": "success",
  "message": "Cashback Sign processed successfully",
  "order_id": "20250322001"
}
```
````

### API Fields

Required fields: from\_address, to\_handle, amount\_usd\_cents, timestamp, signature

1. timestap should be within 5 minutes
2. signature should follow [https://docs.rozo.ai/api-doc/make-a-payment-sign](https://docs.rozo.ai/api-doc/make-a-payment-sign)



### API Response

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

###



