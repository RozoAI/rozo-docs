#!/usr/bin/env bash
# Sample integration script: bridge USDC from Stellar testnet to Base Sepolia.
#
# API endpoint: https://intentapitestnet.rozo.ai
# All endpoints are public — no auth header required.
#
# What it does:
#   1. POST /payments  type=exactIn, source=Stellar testnet USDC, dest=Base Sepolia USDC
#   2. Print source.receiverAddress (= Stellar hub) AND source.receiverMemo (REQUIRED).
#   3. Send the USDC payment with the memo, or pass AUTO=1 to auto-send.
#   4. Poll GET /payments/{id} until status=payment_completed.
set -euo pipefail

cd "$(dirname "$0")/.."
set -a
source .env.dev
set +a

API_BASE_URL="${API_BASE_URL:-https://intentapitestnet.rozo.ai/functions/v1/payment-api}"

: "${TEST_EVM_RECEIVER_ADDRESS:?}"

AMOUNT="${1:-0.02}"
AUTO="${AUTO:-0}"

echo "=== Step 1: create payment ==="
RESP=$(curl -sS -X POST "$API_BASE_URL/payments" \
  -H "Content-Type: application/json" \
  -d "{
    \"appId\": \"testnet-stellar-to-base\",
    \"orderId\": \"order-$(date +%s)\",
    \"type\": \"exactIn\",
    \"display\": { \"title\": \"Testnet Stellar->Base\", \"currency\": \"USD\" },
    \"source\": { \"chainId\": \"1500\", \"tokenSymbol\": \"USDC\", \"amount\": \"$AMOUNT\" },
    \"destination\": {
      \"chainId\": \"84532\",
      \"receiverAddress\": \"$TEST_EVM_RECEIVER_ADDRESS\",
      \"tokenSymbol\": \"USDC\"
    }
  }")
echo "$RESP" | jq .

PAY_ID=$(echo "$RESP" | jq -r .id)
HUB_ADDR=$(echo "$RESP" | jq -r .source.receiverAddress)
HUB_MEMO=$(echo "$RESP" | jq -r .source.receiverMemo)
SRC_AMOUNT=$(echo "$RESP" | jq -r .source.amount)
echo ""
echo "Payment id : $PAY_ID"
echo "Send TO    : $HUB_ADDR"
echo "Send MEMO  : $HUB_MEMO  (memo_text — REQUIRED for matching)"
echo "Send AMOUNT: $SRC_AMOUNT USDC (Stellar testnet)"
echo ""

if [ "$AUTO" = "1" ]; then
  echo "=== Step 2: auto-send (uses TEST_STELLAR_PAYER_SECRET) ==="
  npx tsx scripts/_send-stellar-usdc.ts "$HUB_ADDR" "$SRC_AMOUNT" "$HUB_MEMO"
else
  echo "=== Step 2: send manually ==="
  echo "From wallet: $TEST_STELLAR_PAYER_ADDRESS"
  echo "Or set AUTO=1 to auto-send."
  read -p "Press ENTER once you've sent..."
fi

echo "=== Step 3: poll status (lazy GET hits Horizon directly; fallback cron runs every 1m) ==="
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
