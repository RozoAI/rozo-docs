#!/usr/bin/env bash
# Fee preview via dryrun: POST /payments?dryrun=true returns the same shape as
# a real create call, but does NOT persist anything and does NOT allocate an
# amount slot. Use this to show users a fee + receive amount before they commit.
#
# Mirrors https://docs.rozo.ai/integration/api-doc/api-for-advanced-used/get-fees
# but for testnet. fee is always "0" on testnet.
#
# API endpoint: https://intentapitestnet.rozo.ai (public, no auth header).
#
# Usage:
#   bash scripts/testnet-get-fee.sh                          # default 0.10 base->stellar
#   bash scripts/testnet-get-fee.sh 0.50 base-to-stellar
#   bash scripts/testnet-get-fee.sh 0.50 stellar-to-base
set -euo pipefail

cd "$(dirname "$0")/.."
set -a
source .env.dev
set +a

API_BASE_URL="${API_BASE_URL:-https://intentapitestnet.rozo.ai/functions/v1/payment-api}"

AMOUNT="${1:-0.10}"
DIRECTION="${2:-base-to-stellar}"

case "$DIRECTION" in
  base-to-stellar)
    SRC_CHAIN="84532"
    DST_CHAIN="1500"
    DST_ADDR="${TEST_STELLAR_RECEIVER_ADDRESS:?TEST_STELLAR_RECEIVER_ADDRESS not set}"
    ;;
  stellar-to-base)
    SRC_CHAIN="1500"
    DST_CHAIN="84532"
    DST_ADDR="${TEST_EVM_RECEIVER_ADDRESS:?TEST_EVM_RECEIVER_ADDRESS not set}"
    ;;
  *)
    echo "ERROR: direction must be 'base-to-stellar' or 'stellar-to-base'" >&2
    exit 1
    ;;
esac

echo "Fee preview: $AMOUNT USDC, $DIRECTION"
echo ""

curl -sS -X POST "$API_BASE_URL/payments?dryrun=true" \
  -H "Content-Type: application/json" \
  -d "{
    \"appId\": \"testnet-fee-preview\",
    \"type\": \"exactIn\",
    \"display\": { \"title\": \"Fee preview\", \"currency\": \"USD\" },
    \"source\": { \"chainId\": \"$SRC_CHAIN\", \"tokenSymbol\": \"USDC\", \"amount\": \"$AMOUNT\" },
    \"destination\": {
      \"chainId\": \"$DST_CHAIN\",
      \"receiverAddress\": \"$DST_ADDR\",
      \"tokenSymbol\": \"USDC\"
    }
  }" | jq .

echo ""
echo "(testnet always returns fee=\"0\"; same shape as docs.rozo.ai/api-for-advanced-used/get-fees)"
