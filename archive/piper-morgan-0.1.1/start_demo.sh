#!/bin/bash
echo "🚀 Starting Piper Morgan 0.1.1 Demo..."

# Activate virtual environment
source venv/bin/activate

# Check required files exist
if [ ! -f ".env" ]; then
    echo "❌ .env file missing! Please configure API keys."
    exit 1
fi

# Start the demo
echo "✅ Starting Streamlit on http://localhost:8501"
python -m streamlit run chat_interface.py --server.headless true
