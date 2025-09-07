# Morning Standup Web Interface

## Implementation

- FastAPI backend with /api/standup endpoint
- Dark mode UI at /assets/standup.html
- Integrates with CLI orchestrator for consistency
- Performance: 4.6-5.1s generation time

## Configuration

- Port: 8001 (documented to avoid Docker conflicts)
- Server: uvicorn with 127.0.0.1 binding
- Static assets: served via FastAPI StaticFiles

## Usage

Daily 6 AM standup with prominent performance metrics,
project context, and GitHub activity display.

## Quick Start

```bash
# Start FastAPI server
PYTHONPATH=. python web/app.py
# or
PYTHONPATH=. python -m uvicorn web.app:app --host 127.0.0.1 --port 8001
```

## Access Points

- **Web UI**: http://localhost:8001/assets/standup.html
- **API Endpoint**: http://localhost:8001/api/standup
- **API Documentation**: http://localhost:8001/docs

## Performance

- Generation Time: 4.6-5.1 seconds
- Response: JSON with comprehensive standup data
- Features: Dark mode, mobile responsive, error handling
