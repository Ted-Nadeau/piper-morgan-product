#!/bin/bash
# Setup Python environment for Piper Morgan 1.0

echo "Setting up Python environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies from existing requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Python environment ready"
echo "💡 Activate with: source venv/bin/activate"
