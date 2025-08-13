# Daily Startup Guide - One-Click Piper Morgan

**Created**: 2025-08-13
**Purpose**: Documentation for the one-click startup script for daily standup routine

## Overview

The `start-piper.sh` script provides a one-click solution to start all Piper Morgan services for your daily standup routine. It includes comprehensive health checks, platform-specific browser opening, and user-friendly status reporting.

## Quick Start

```bash
# From the project root directory
./start-piper.sh
```

That's it! The script will:
- ✅ Check Docker daemon status
- ✅ Start infrastructure services (PostgreSQL, Redis, ChromaDB, Temporal)
- ✅ Start the API server on port 8001
- ✅ Start the Web UI on port 8081
- ✅ Open your browser to the chat interface
- ✅ Display startup summary with health status

## What Gets Started

### Infrastructure Services (Docker)
- **PostgreSQL**: Database on port 5433
- **Redis**: Cache and session store on port 6379
- **ChromaDB**: Vector database for document embeddings
- **Temporal**: Workflow orchestration engine
- **Traefik**: Load balancer and reverse proxy

### Application Services
- **API Server**: Main backend on `http://localhost:8001`
- **Web UI**: Chat interface on `http://localhost:8081`

## Service Health Checks

The script performs comprehensive health checks:
- Docker daemon connectivity
- Individual service health endpoints
- Port availability verification
- Response time monitoring (max 2 minutes)

## Platform Support

**Browser Opening**:
- **macOS**: Uses `open` command
- **Linux**: Uses `xdg-open` (with fallback message)
- **Windows**: Uses `start` command
- **Unknown OS**: Provides manual URL

## Stopping Services

```bash
# Stop all services cleanly
./stop-piper.sh
```

The stop script will:
- Stop Python processes using PID files
- Clean up background processes on ports 8001/8081
- Stop Docker infrastructure services
- Clean up logs and temporary files

## Troubleshooting

### Common Issues

**Docker not running**:
```
❌ Docker daemon is not running. Please start Docker Desktop and try again.
```
**Solution**: Start Docker Desktop and wait for it to fully initialize.

**Port conflicts**:
```
❌ API server failed to start on port 8001 after 60 seconds
```
**Solution**: Check if another service is using the port:
```bash
lsof -i :8001
kill <PID>  # if needed
```

**Services already running**:
```
⚠️ API server already running on port 8001
```
**Solution**: This is normal - the script detects existing services and continues.

### Log Files

Service logs are stored in the `logs/` directory:
- `logs/api_server.log` - API server output
- `logs/web_ui.log` - Web UI output
- `logs/api_server.pid` - API server process ID
- `logs/web_ui.pid` - Web UI process ID

### Manual Commands

If the script fails, you can start services manually:

```bash
# Start Docker services
docker-compose up -d

# Start API server
python main.py &

# Start Web UI
cd web && python -m uvicorn app:app --reload --port 8081 &
```

## Configuration

### Script Variables
Edit the script to modify:
- `MAIN_UI_PORT=8081` - Web UI port
- `API_PORT=8001` - API server port
- `MAX_WAIT_TIME=120` - Maximum health check wait time

### Environment Variables
Ensure your `.env` file contains:
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://piper:dev_changeme_in_production@localhost:5433/piper_morgan
REDIS_URL=redis://localhost:6379
```

## Daily Workflow Integration

### Morning Standup Routine
1. Run `./start-piper.sh`
2. Browser opens to chat interface automatically
3. PIPER.md context is loaded (VA/Kind priorities, project allocation)
4. Ask questions like:
   - "What's my top priority today?"
   - "What am I working on?"
   - "What should I focus on?"

### End of Day
1. Use the chat interface for session wrap-up
2. Run `./stop-piper.sh` when done
3. Services shut down cleanly

## Integration with PIPER.md

The startup script automatically loads context from `config/PIPER.md`:
- **VA/Decision Reviews**: 70% allocation, Q4 onramp priority
- **Piper Morgan AI**: 25% allocation, production-ready status
- **OneJob/Other**: 5% allocation, maintenance mode
- **Daily schedule**: 6 AM standup, 9 AM dev focus, 2 PM UX work

## Performance Expectations

**Startup Time**:
- Cold start: ~60-90 seconds (includes Docker service initialization)
- Warm start: ~15-30 seconds (Docker already running)
- Health checks: <60 seconds for all services

**Resource Usage**:
- RAM: ~2-3 GB total for all services
- CPU: Minimal during idle, moderate during AI processing
- Disk: Persistent data in Docker volumes

## Customization

### Adding Services
To add new services to the startup sequence:
1. Add health check function
2. Add service start function
3. Update startup summary
4. Add to stop script

### Changing Ports
1. Update script variables
2. Update Docker Compose configuration
3. Update health check URLs

### Browser Customization
Modify the `open_browser()` function to:
- Open specific browser
- Open multiple tabs
- Set browser preferences

## Mac Dock Integration

**Add to Dock**:
1. Create alias: `alias piper='cd /path/to/piper-morgan && ./start-piper.sh'`
2. Add to `.zshrc` or `.bash_profile`
3. Or create macOS app wrapper

**Desktop Shortcut**:
1. Create Automator application
2. Add shell script action
3. Save to Applications folder

## Success Indicators

When everything is working correctly, you'll see:
```
🎉 Piper Morgan Startup Complete!
2025-08-13 05:02:30 PT - All services are running

📋 Service Status:
  🌐 Web UI:     http://localhost:8081
  🔌 API:       http://localhost:8001
  🐳 Docker:    Infrastructure services running

📝 Daily Standup Ready:
  • Chat interface is available for morning standup
  • All backend services are healthy and responsive
  • VA/Kind context loaded from PIPER.md

📊 Quick Health Check:
  ✅ API Health: OK
  ✅ Web UI: OK

Ready for your daily standup with Piper Morgan! 🚀
```

---

## Version History

- **v1.0** (2025-08-13): Initial release with full health checks and browser opening
- **v1.1** (TBD): Planned improvements based on usage feedback
