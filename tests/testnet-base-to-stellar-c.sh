#!/usr/bin/env bash
# Bridge USDC from Base Sepolia to a Stellar testnet C-address (Soroban contract).
#
# Same flow as testnet-base-to-stellar.sh, but the destination is a C-address
# (e.g. a smart wallet or contract account) instead of a classic G-account.
# On the payout side this triggers the Stellar Asset Contract (SAC) `transfer`
# path via Soroban RPC — no `memo_text` is supported on this path.
#
# Usage:
#   ./scripts/testnet-base-to-stellar-c.sh [AMOUNT] [C_ADDRESS]
#   AUTO=1 ./scripts/testnet-base-to-stellar-c.sh 0.02
#
# Defaults to TEST_STELLAR_C_RECEIVER_ADDRESS from .env.dev if no C-address is
# passed on the CLI.
set -euo pipefail

cd "$(dirname "$0")/.."
set -a
source .env.dev
set +a

API_BASE_URL="${API_BASE_URL:-https://intentapitestnet.rozo.ai/functions/v1/payment-api}"

AMOUNT="${1:-0.02}"
C_ADDR="${2:-${TEST_STELLAR_C_RECEIVER_ADDRESS:-}}"
AUTO="${AUTO:-0}"

if [ -z "$C_ADDR" ]; then
  echo "ERROR: pass a C-address as 2nd arg, or set TEST_STELLAR_C_RECEIVER_ADDRESS in .env.dev" >&2
  exit 1
fi

if [[ ! "$C_ADDR" =~ ^C[A-Z2-7]{55}$ ]]; then
  echo "ERROR: destination is not a Stellar C-address: $C_ADDR" >&2
  exit 1
fi

echo "=== Step 1: create payment (dest = C-address) ==="
RESP=$(curl -sS -X POST "$API_BASE_URL/payments" \
  -H "Content-Type: application/json" \
  -d "{
    \"appId\": \"testnet-base-to-stellar-c\",
    \"orderId\": \"order-c-$(date +%s)\",
    \"type\": \"exactIn\",
    \"display\": { \"title\": \"Testnet Base->Stellar C-addr\", \"currency\": \"USD\" },
    \"source\": { \"chainId\": \"84532\", \"tokenSymbol\": \"USDC\", \"amount\": \"$AMOUNT\" },
    \"destination\": {
      \"chainId\": \"1500\",
      \"receiverAddress\": \"$C_ADDR\",
      \"tokenSymbol\": \"USDC\"
    }
  }")
echo "$RESP" | jq .

PAY_ID=$(echo "$RESP" | jq -r .id)
HUB_ADDR=$(echo "$RESP" | jq -r .source.receiverAddress)
SRC_AMOUNT=$(echo "$RESP" | jq -r .source.amount)

if [ "$PAY_ID" = "null" ] || [ -z "$PAY_ID" ]; then
  echo "ERROR: payment creation failed" >&2
  exit 1
fi

echo ""
echo "Payment id : $PAY_ID"
echo "Send TO    : $HUB_ADDR"
echo "Send AMOUNT: $SRC_AMOUNT USDC (Base Sepolia)"
echo "Dest C-addr: $C_ADDR"
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
