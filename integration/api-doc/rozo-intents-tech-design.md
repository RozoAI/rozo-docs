# Intent Payment Flow

A Rozo intent describes a requested payment outcome. Your application creates the request, the payer authorizes the source payment, and your application checks the destination result.

```text
Choose the task and supported route
                 ↓
Preview the amount and fees
                 ↓
Create the order and save its reference
                 ↓
Payer checks and authorizes payment
                 ↓
Read status or receive a verified notification
                 ↓
Reconcile the destination result
```

## What your application supplies

- The payment amount and asset according to the chosen API.
- The source and destination networks supported by that flow.
- The destination address when using a wallet transfer API. Merchant integrations instead use the receiving configuration associated with the merchant app.
- Any required recipient memo, app identity and application order reference.

Follow [Choose Your Integration](../../start/choose-your-integration.md) before constructing a request. Do not combine fields from different APIs solely because they serve similar payment use cases.

## What your application receives

The selected API returns its order reference, payment instructions and status fields. Use those instructions for this order only. The returned amount and payment deadline take precedence over illustrative values in a guide.

Track the order until the requested destination result is confirmed. Source-payment detection is an intermediate result, not a general settlement guarantee. See the [payment lifecycle](../../rozo-intentpay-techdoc.md) for completion checks across merchant, Funding, Checkout and paid-API flows.

## Responsibilities at the integration boundary

The payer or authorized wallet signer approves the payment. Your application validates the recipient and amount, keeps request references, verifies notifications and handles retries according to the API's idempotency rules.

Rozo executes the selected payment flow and exposes its result through the documented interface. Applications do not need to operate Rozo infrastructure to integrate. If an outcome remains unclear, query the existing order and [contact support](../../contact/contact-us/README.md) before sending again.

## References

- [Bridge & Wallet API](bridge-api.md)
- [Merchant API](merchant-api.md)
- [Funding API](funding/README.md)
- [Webhook verification](api-for-advanced-used/webhook.md)
- [Contracts & Audits](../../contact/contracts-and-audits.md)
