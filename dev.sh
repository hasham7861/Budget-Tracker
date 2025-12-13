#!/bin/bash
# Development script that builds frontend in watch mode and runs FastAPI

set -e

echo "🚀 Starting Budget Tracker Development Server"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    exit 1
fi

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Error: poetry is not installed"
    exit 1
fi

# Initial build
echo "📦 Building frontend (initial build)..."
cd src/budget_tracker_api/frontend
npm run build
cd "$SCRIPT_DIR"

echo ""
echo "✅ Initial build complete!"
echo ""
echo "🔄 Starting watch mode + FastAPI server..."
echo ""
echo "   Frontend: Auto-rebuilding on file changes"
echo "   Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $WATCH_PID 2>/dev/null || true
    kill $API_PID 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM

# Start frontend build in watch mode (background)
cd src/budget_tracker_api/frontend
npm run build:watch &> "$SCRIPT_DIR/.frontend-build.log" &
WATCH_PID=$!
cd "$SCRIPT_DIR"

# Give watch mode a moment to start
sleep 2

# Start FastAPI server (background)
poetry run api-start &
API_PID=$!

# Wait for both processes
wait $API_PID
