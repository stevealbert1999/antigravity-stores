#!/bin/bash
set -e

echo "LedgerGuard AI — Sales Demo Launcher"
echo "-----------------------------------"

cd "$(dirname "$0")/backend"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is not installed."
  exit 1
fi

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "WARNING: cloudflared is not installed."
  echo "Install it from: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
  echo "Then rerun this script."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing backend dependencies..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null

export LEDGERGUARD_API_KEY=demo-ledgerguard-key

echo "Starting backend on http://localhost:8000 ..."
uvicorn main:app --host 0.0.0.0 --port 8000 > ledgerguard-demo.log 2>&1 &
BACKEND_PID=$!

sleep 3

echo "Opening Cloudflare tunnel..."
echo "Copy the generated https://*.trycloudflare.com URL into the dashboard Backend URL field."
echo "Dashboard: https://stevealbert1999.github.io/antigravity-stores/accounts-payable-ai/app/"
echo "Login: ap.manager@ledgerguard.local / demo-password"
echo "CSV: accounts-payable-ai/demo-data/sample_invoices.csv"
echo ""

cloudflared tunnel --url http://localhost:8000

trap "kill $BACKEND_PID" EXIT
