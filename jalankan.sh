#!/usr/bin/env bash
# Jalankan frontend (React) + backend (FastAPI) secara bersamaan.
# Tekan Ctrl+C di sini untuk matiin dua-duanya.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR/backend"
.venv/bin/uvicorn app.main:app --reload --port 8000 &
BACK_PID=$!

cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONT_PID=$!

echo ""
echo "=========================================="
echo "  Frontend : http://localhost:5173"
echo "  Backend  : http://localhost:8000"
echo "  API Docs : http://localhost:8000/docs"
echo "  (Ctrl+C untuk stop semuanya)"
echo "=========================================="
echo ""

trap "kill $BACK_PID $FRONT_PID 2>/dev/null" EXIT INT TERM
wait