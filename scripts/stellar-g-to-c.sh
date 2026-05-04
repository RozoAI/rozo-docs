#!/usr/bin/env bash
# Mainnet: send USDC from a Stellar G-account to a Stellar C-address (Soroban contract).
#
# Same chain (Stellar -> Stellar), routed through Rozo so the destination C-address
# is paid via the Stellar Asset Contract (SAC) `transfer` path on Soroban RPC.
#
# Why route this through Rozo instead of calling SAC `transfer` directly?
#   - The user's funds live in a classic G-account that cannot natively `transfer`
#     to a Soroban contract; the hub bridges G (memo-based payin) -> C (SAC payout).
#   - Same auth-less public API as the cross-chain flows.
#
# Flow:
#   1. POST /payments  source = Stellar USDC (G-account payin via memo)
#                      destination = Stellar USDC, receiverAddress = C...
#   2. Print the Rozo Stellar hub address + memo + exact amount.
#   3. Send the Stellar payment with the memo, or pass AUTO=1 to auto-send
#      using TEST_STELLAR_PAYER_SECRET.
#   4. Poll GET /payments/{id} until payment_completed | payment_bounced | payment_expired.
#
# Usage:
#   bash scripts/stellar-g-to-c.sh [AMOUNT] [C_ADDRESS]
#   AUTO=1 bash scripts/stellar-g-to-c.sh 0.10
#
# Defaults to STELLAR_C_RECEIVER_ADDRESS from .env.dev when no C-address is given.
set -euo pipefail

cd "$(dirname "$0")/.."
set -a
source .env.dev
set +a

# Mainnet API. Override only if you've pointed a custom domain.
API_BASE_URL="${API_BASE_URL:-https://intentapiv4.rozo.ai/functions/v1/payment-api}"

AMOUNT="${1:-0.10}"
C_ADDR="${2:-${STELLAR_C_RECEIVER_ADDRESS:-}}"
AUTO="${AUTO:-0}"

if [ -z "$C_ADDR" ]; then
  echo "ERROR: pass a C-address as 2nd arg, or set STELLAR_C_RECEIVER_ADDRESS in .env.dev" >&2
  exit 1
fi

if [[ ! "$C_ADDR" =~ ^C[A-Z2-7]{55}$ ]]; then
  echo "ERROR: destination is not a Stellar C-address: $C_ADDR" >&2
  exit 1
fi

echo "=== Step 1: create payment (Stellar G -> Stellar C) ==="
RESP=$(curl -sS -X POST "$API_BASE_URL/payments" \
  -H "Content-Type: application/json" \
  -d "{
    \"appId\": \"stellar-g-to-c\",
    \"orderId\": \"order-g2c-$(date +%s)\",
    \"type\": \"exactIn\",
    \"display\": { \"title\": \"Stellar G->C\", \"currency\": \"USD\" },
    \"source\": { \"chainId\": \"1500\", \"tokenSymbol\": \"USDC\", \"amount\": \"$AMOUNT\" },
    \"destination\": {
      \"chainId\": \"1500\",
      \"receiverAddress\": \"$C_ADDR\",
      \"tokenSymbol\": \"USDC\"
    }
  }")
echo "$RESP" | jq .

PAY_ID=$(echo "$RESP" | jq -r .id)
HUB_ADDR=$(echo "$RESP" | jq -r .source.receiverAddress)
HUB_MEMO=$(echo "$RESP" | jq -r .source.receiverMemo)
SRC_AMOUNT=$(echo "$RESP" | jq -r .source.amount)

if [ "$PAY_ID" = "null" ] || [ -z "$PAY_ID" ]; then
  echo "ERROR: payment creation failed" >&2
  exit 1
fi

if [ "$HUB_MEMO" = "null" ] || [ -z "$HUB_MEMO" ]; then
  echo "ERROR: API did not return a receiverMemo for the Stellar G payin" >&2
  exit 1
fi

echo ""
echo "Payment id : $PAY_ID"
echo "Send TO    : $HUB_ADDR"
echo "Send MEMO  : $HUB_MEMO   (memo_text — REQUIRED for matching)"
echo "Send AMOUNT: $SRC_AMOUNT USDC (Stellar mainnet)"
echo "Dest C-addr: $C_ADDR"
echo ""

if [ "$AUTO" = "1" ]; then
  : "${TEST_STELLAR_PAYER_SECRET:?TEST_STELLAR_PAYER_SECRET not set in .env.dev}"
  echo "=== Step 2: auto-send (uses TEST_STELLAR_PAYER_SECRET) ==="
  npx tsx scripts/_send-stellar-usdc.ts "$HUB_ADDR" "$SRC_AMOUNT" "$HUB_MEMO"
else
  echo "=== Step 2: send manually ==="
  echo "From your Stellar G-wallet, send exactly $SRC_AMOUNT USDC to $HUB_ADDR"
  echo "with memo_text = $HUB_MEMO"
  echo ""
  echo "Or re-run with AUTO=1 to auto-send."
  read -p "Press ENTER once you've sent the Stellar payment..."
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
