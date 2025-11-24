#!/bin/bash

# Piper Morgan Stop Script
# Version: 1.1.0 (Cross-platform)
# Purpose: Clean shutdown of Piper Morgan services
# Supports: macOS, Linux, Windows (Git Bash/WSL)

# Source OS detection library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/os-detect.sh
source "$SCRIPT_DIR/lib/os-detect.sh"

echo "🛑 Stopping Piper Morgan..."
echo "================================"

# Stop backend (cross-platform)
if [ -f ".piper-backend.pid" ]; then
    BACKEND_PID=$(cat .piper-backend.pid)
    if kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "🛑 Stopping backend (PID: $BACKEND_PID)..."
        if terminate_process "$BACKEND_PID" "TERM"; then
            echo "✅ Backend stopped"
        else
            echo "⚠️  Failed to stop backend gracefully, forcing shutdown..."
            terminate_process "$BACKEND_PID" "KILL" || true
            echo "✅ Backend forced to stop"
        fi
    else
        echo "ℹ️  Backend already stopped"
    fi
    rm -f .piper-backend.pid
else
    echo "ℹ️  No backend PID file found"
fi

# Stop frontend (cross-platform)
if [ -f ".piper-frontend.pid" ]; then
    FRONTEND_PID=$(cat .piper-frontend.pid)
    if kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo "🛑 Stopping frontend (PID: $FRONTEND_PID)..."
        if terminate_process "$FRONTEND_PID" "TERM"; then
            echo "✅ Frontend stopped"
        else
            echo "⚠️  Failed to stop frontend gracefully, forcing shutdown..."
            terminate_process "$FRONTEND_PID" "KILL" || true
            echo "✅ Frontend forced to stop"
        fi
    else
        echo "ℹ️  Frontend already stopped"
    fi
    rm -f .piper-frontend.pid
else
    echo "ℹ️  No frontend PID file found"
fi

# Clean up any remaining processes (cross-platform)
echo "🧹 Cleaning up..."
if is_windows; then
    # Windows: Use taskkill
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq*Piper*" 2>/dev/null || true
else
    # Unix: Use pkill
    pkill -f "python main.py" 2>/dev/null || true
    pkill -f "python web/app.py" 2>/dev/null || true
fi

echo "✅ Piper Morgan stopped successfully"
echo "================================"
