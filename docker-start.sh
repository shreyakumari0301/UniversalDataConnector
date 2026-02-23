#!/usr/bin/env bash
# Start the API with Docker and open the app + demo in the browser (like start_demo.sh).
# Run after at least one 'docker-compose up --build'.
cd "$(dirname "$0")"

echo "Starting containers..."
docker-compose up -d

echo "Waiting for API to be ready..."
for i in 1 2 3 4 5 6 7 8 9 10; do
  if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null | grep -q 200; then
    break
  fi
  sleep 1
done
sleep 1

DEMO_URL="http://localhost:8000/demo"
API_URL="http://localhost:8000"
echo "Opening app and demo in browser..."
if command -v explorer.exe >/dev/null 2>&1; then
  explorer.exe "$DEMO_URL"
  explorer.exe "$API_URL"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$DEMO_URL" 2>/dev/null || true
  xdg-open "$API_URL" 2>/dev/null || true
elif command -v open >/dev/null 2>&1; then
  open "$DEMO_URL"
  open "$API_URL"
else
  echo "Open: $API_URL and $DEMO_URL"
fi

echo ""
echo "  API: $API_URL  |  Demo: $DEMO_URL"
echo "  To view logs: docker-compose logs -f"
echo "  To stop: docker-compose down"
echo ""
docker-compose logs -f
