#!/bin/bash

# Piper Morgan One-Click Startup Script
# Version: 1.0.0
# Purpose: Launch Piper Morgan with health checks

set -e  # Exit on any error

echo "🚀 Starting Piper Morgan..."
echo "================================"

# Check if Docker Desktop is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker Desktop is not running"
    echo "Please start Docker Desktop and try again"
    echo "You can find Docker Desktop in your Applications folder"
    exit 1
fi

echo "✅ Docker Desktop is running"

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "web/app.py" ]; then
    echo "❌ Not in Piper Morgan directory"
    echo "Please navigate to your piper-morgan directory and try again"
    exit 1
fi

echo "✅ Piper Morgan directory confirmed"

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found"
    echo "Please run: python -m venv venv && source venv/bin/activate"
    exit 1
fi

# Check Python dependencies
echo "🔍 Checking Python dependencies..."
if ! python -c "import services" > /dev/null 2>&1; then
    echo "❌ Python dependencies not installed"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Python dependencies verified"

# Create logs directory if it doesn't exist
mkdir -p logs

# Start backend services
echo "🚀 Starting backend services..."
echo "Starting main.py in background..."
nohup python main.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check backend health
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    echo "Check logs/backend.log for details"
    exit 1
fi

# Start frontend
echo "🌐 Starting frontend..."
echo "Starting web/app.py..."
nohup python web/app.py > logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 3

# Check frontend health
if curl -s http://localhost:8081/health > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    echo "Check logs/frontend.log for details"
    exit 1
fi

# Create PID file for management
echo "$BACKEND_PID" > .piper-backend.pid
echo "$FRONTEND_PID" > .piper-frontend.pid

echo "🎉 Piper Morgan is ready!"
echo "================================"

# Branch management reminder
echo ""
echo "🌿 Branch Management Reminder:"
echo "================================"
CURRENT_BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "📍 Current Branch: $CURRENT_BRANCH"
    if [ "$CURRENT_BRANCH" = "main" ]; then
        echo "⚠️  Working on main branch - consider feature branch for development"
        echo "📚 See: docs/development/BRANCH-MANAGEMENT.md"
    elif [[ "$CURRENT_BRANCH" == feature/* ]]; then
        echo "✅ Good! Working on feature branch"
    elif [[ "$CURRENT_BRANCH" == dev/* ]]; then
        echo "🔬 Development branch - experiments and research"
    fi
    echo "📋 Quick guidance: ./scripts/branch-guidance.sh"
fi
echo "🌐 Frontend: http://localhost:8081/"
echo "🔧 Backend: http://localhost:8000/"
echo "📊 Health: http://localhost:8081/health"
echo ""
echo "💡 Tip: Bookmark http://localhost:8081/ for quick access"
echo "🔄 To stop: ./stop-piper.sh"
echo ""
echo "🚀 Ready for your 6:00 AM PT standup!"

# Open browser
open http://localhost:8081/
