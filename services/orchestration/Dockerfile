# Dockerfile for the Orchestration Service (Temporal Worker)
# 2025-06-03: Initial Dockerfile for orchestration service.
# 2025-07-22: Updated for PM-055 Python 3.11 consistency

# Use Python 3.11-slim base image for PM-055 compliance
FROM python:3.11-slim-bullseye

# Set Python version environment variable for verification
ENV PYTHON_VERSION=3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the top-level requirements.txt into the container
# This assumes requirements.txt is at the project root
COPY requirements.txt .

# Install Python dependencies with version verification
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Add Python version verification during build
RUN python --version && \
    python -c "import sys; assert sys.version_info >= (3, 11), f'Python {sys.version} < 3.11 (PM-055 requirement)'"

# Copy the entire 'services' directory into the container
# This allows imports like 'from services.shared_types import ...'
# This path should match the volume mount in docker-compose.yml: ./services:/app/services
COPY services /app/services

# Copy version verification script
COPY scripts/verify-python-version.sh /usr/local/bin/verify-python-version.sh
RUN chmod +x /usr/local/bin/verify-python-version.sh

# Set PYTHONPATH to include the /app directory, so Python can find 'services' package
ENV PYTHONPATH=/app:$PYTHONPATH

# If your worker script is directly in services/orchestration,
# you'll run it from the root of /app/services/orchestration
# assuming the worker script is named worker.py
# If your worker script is in a different location or needs specific commands, adjust CMD.
# For now, let's assume a worker.py will be created in services/orchestration
# CMD ["/bin/bash", "-c", "/usr/local/bin/verify-python-version.sh && python -m services.orchestration.worker"]
# We'll leave this commented for now, as we haven't defined the entrypoint yet.

# If you have specific scripts to run on startup for this service,
# you would define them here. For a Temporal worker, it typically runs continuously.
# ENTRYPOINT ["/usr/local/bin/python"]
# CMD ["-m", "services.orchestration.worker"]
