#!/usr/bin/env bash
# Sample integration script: bridge USDC from Base Sepolia to Stellar testnet
# (classic G-account destination).
#
# API endpoint: https://intentapitestnet.rozo.ai
# All endpoints are public — no auth header required.
#
# What it does:
#   1. POST /payments  type=exactIn, source=Base Sepolia USDC, dest=Stellar USDC
#   2. Print returned payment, including source.receiverAddress and source.amount
#      (the user must send exactly that amount to that address)
#   3. Send the USDC tx manually, or pass AUTO=1 to auto-send via TEST_EVM_PAYER_*
#   4. Poll GET /payments/{id} until status=payment_completed
set -euo pipefail

cd "$(dirname "$0")/.."
set -a
source .env.dev
set +a

API_BASE_URL="${API_BASE_URL:-https://intentapitestnet.rozo.ai/functions/v1/payment-api}"

: "${TEST_STELLAR_RECEIVER_ADDRESS:?TEST_STELLAR_RECEIVER_ADDRESS not set}"

AMOUNT="${1:-0.01}"
AUTO="${AUTO:-0}"

echo "=== Step 1: create payment ==="
RESP=$(curl -sS -X POST "$API_BASE_URL/payments" \
  -H "Content-Type: application/json" \
  -d "{
    \"appId\": \"testnet-base-to-stellar\",
    \"orderId\": \"order-$(date +%s)\",
    \"type\": \"exactIn\",
    \"display\": { \"title\": \"Testnet Base->Stellar\", \"currency\": \"USD\" },
    \"source\": { \"chainId\": \"84532\", \"tokenSymbol\": \"USDC\", \"amount\": \"$AMOUNT\" },
    \"destination\": {
      \"chainId\": \"1500\",
      \"receiverAddress\": \"$TEST_STELLAR_RECEIVER_ADDRESS\",
      \"tokenSymbol\": \"USDC\"
    }
  }")
echo "$RESP" | jq .

PAY_ID=$(echo "$RESP" | jq -r .id)
HUB_ADDR=$(echo "$RESP" | jq -r .source.receiverAddress)
SRC_AMOUNT=$(echo "$RESP" | jq -r .source.amount)
echo ""
echo "Payment id : $PAY_ID"
echo "Send TO    : $HUB_ADDR"
echo "Send AMOUNT: $SRC_AMOUNT USDC (Base Sepolia)"
echo ""

if [ "$AUTO" = "1" ]; then
  echo "=== Step 2: auto-send (uses TEST_EVM_PAYER_PRIVATE_KEY) ==="
  npx tsx scripts/_send-evm-usdc.ts "$HUB_ADDR" "$SRC_AMOUNT"
else
  echo "=== Step 2: send manually ==="
  echo "From wallet: $TEST_EVM_PAYER_ADDRESS"
  echo "Or set AUTO=1 to auto-send."
  echo ""
  read -p "Press ENTER once you've sent the USDC tx..."
fi

echo "=== Step 3: poll status ==="
for i in {1..60}; do
  STATUS=$(curl -sS "$API_BASE_URL/payments/$PAY_ID" | jq -r .status)
  echo "  [$i] status = $STATUS"
  if [ "$STATUS" = "payment_completed" ] || [ "$STATUS" = "payment_bounced" ] || [ "$STATUS" = "payment_expired" ]; then
    break
  fi
  sleep 5
done

echo ""
echo "=== Final ==="
curl -sS "$API_BASE_URL/payments/$PAY_ID" | jq .
