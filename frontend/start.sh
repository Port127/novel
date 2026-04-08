#!/bin/bash
# Start both frontend dev server and Python backend

FRONTEND_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$FRONTEND_DIR")"

echo "=== 小说工作台 ==="
echo ""

# Check Python deps
if ! python -c "import fastapi" 2>/dev/null; then
  echo "📦 Installing Python dependencies..."
  pip install -r "$PROJECT_ROOT/backend/requirements.txt" -q
fi

# Start backend (from project root so 'backend' package is importable)
echo "🚀 Starting backend on http://localhost:8000 ..."
cd "$PROJECT_ROOT"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir backend &
BACKEND_PID=$!

# Start frontend
echo "🚀 Starting frontend on http://localhost:5173 ..."
cd "$FRONTEND_DIR"
npx vite --host &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers running. Press Ctrl+C to stop."
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
