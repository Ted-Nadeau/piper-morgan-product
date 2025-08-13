#!/bin/bash

# Piper Morgan Stop Script
# Version: 1.0.0
# Purpose: Clean shutdown of Piper Morgan services

echo "🛑 Stopping Piper Morgan..."
echo "================================"

# Stop backend
if [ -f ".piper-backend.pid" ]; then
    BACKEND_PID=$(cat .piper-backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "🛑 Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        echo "✅ Backend stopped"
    else
        echo "ℹ️  Backend already stopped"
    fi
    rm -f .piper-backend.pid
else
    echo "ℹ️  No backend PID file found"
fi

# Stop frontend
if [ -f ".piper-frontend.pid" ]; then
    FRONTEND_PID=$(cat .piper-frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "🛑 Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        echo "✅ Frontend stopped"
    else
        echo "ℹ️  Frontend already stopped"
    fi
    rm -f .piper-frontend.pid
else
    echo "ℹ️  No frontend PID file found"
fi

# Clean up any remaining processes
echo "🧹 Cleaning up..."
pkill -f "python main.py" 2>/dev/null || true
pkill -f "python web/app.py" 2>/dev/null || true

echo "✅ Piper Morgan stopped successfully"
echo "================================"
