# Payment (NS Sign)

## 1. Prepare the message

Buyers (from\_handle) need to sign a messge to confirm the payments. The message includes the order details.



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

### 2. API Call

```
Body
API Host: https://api.rozo.ai/v1/nssign



```

#### Curl Command

```shellscript
curl -X POST https://api.rozo.ai/v1/nssign \
  -H "Content-Type: application/json" \
  -d '{
    "from_handle": "hello",
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
  "from_handle": "shawnmuggle",
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
  "message": "NS Sign processed successfully",
  "order_id": "20250322001"
}
```
````



###



