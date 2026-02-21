#!/usr/bin/env bash
# Start uvicorn (API) and open demo.html in the browser.
# Run from project root: ./start_demo.sh

set -e
cd "$(dirname "$0")"

echo "Starting API on http://localhost:8000 ..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

echo "Starting file server for demo on http://localhost:8080 ..."
python3 -m http.server 8080 &
HTTP_PID=$!

sleep 2
DEMO_URL="http://localhost:8080/demo.html"
API_URL="http://localhost:8000"
echo "Opening demo in browser..."
if command -v explorer.exe >/dev/null 2>&1; then
  explorer.exe "$DEMO_URL"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$DEMO_URL" 2>/dev/null || true
elif command -v open >/dev/null 2>&1; then
  open "$DEMO_URL"
else
  echo "Open in your browser: $DEMO_URL"
fi

echo ""
echo "  API (use this in the browser): $API_URL  -> landing page, $API_URL/docs -> Swagger"
echo "  Demo: $DEMO_URL"
echo "  (0.0.0.0 means 'listen on all interfaces'; always open http://localhost:8000 or http://127.0.0.1:8000)"
echo ""
echo "Press Ctrl+C to stop both servers."
cleanup() { kill $UVICORN_PID $HTTP_PID 2>/dev/null; exit 0; }
trap cleanup INT TERM
wait $UVICORN_PID $HTTP_PID
