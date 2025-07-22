# Dockerfile for Piper Morgan Main Application
# PM-055 Step 2: Docker configuration for Python 3.11 consistency
# Created: 2025-07-22

# Use Python 3.11-slim base image for PM-055 compliance
FROM python:3.11-slim-bullseye

# Set Python version environment variable for verification
ENV PYTHON_VERSION=3.11

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Add Python version verification during build
RUN python --version && \
    python -c "import sys; assert sys.version_info >= (3, 11), f'Python {sys.version} < 3.11 (PM-055 requirement)'"

# Copy application code
COPY . .

# Copy and setup version verification script
COPY scripts/verify-python-version.sh /usr/local/bin/verify-python-version.sh
RUN chmod +x /usr/local/bin/verify-python-version.sh

# Set PYTHONPATH for proper module imports
ENV PYTHONPATH=/app:$PYTHONPATH

# Create non-root user for security
RUN groupadd -r piper && useradd -r -g piper piper
RUN chown -R piper:piper /app
USER piper

# Expose port for main application
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8001/health', timeout=5)" || exit 1

# Run version verification on startup, then start application
CMD ["/bin/bash", "-c", "/usr/local/bin/verify-python-version.sh && python main.py"]
