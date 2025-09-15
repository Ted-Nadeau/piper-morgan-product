# Port Reference - Quick Guide

## Development Ports (Fixed)
- **8001**: API Backend (all endpoints)
- **8081**: Web UI (chat, standup, preferences)

## Common URLs

### Web Interface
- **Main Chat**: http://localhost:8081/
- **Personality Preferences**: http://localhost:8081/personality-preferences
- **Standup Generator**: http://localhost:8081/standup

### API Endpoints
- **API Base**: http://localhost:8001/api/
- **Health Check**: http://localhost:8001/health
- **Personality Profile**: http://localhost:8001/api/personality/profile/default
- **Enhanced Standup**: http://localhost:8001/api/standup?personality=true

## Testing Commands

### Quick API Tests
```bash
# Test API health
curl http://localhost:8001/health

# Get personality profile
curl http://localhost:8001/api/personality/profile/default | jq '.'

# Test enhanced standup
curl "http://localhost:8001/api/standup?personality=true" | jq '.'

# Test basic standup
curl http://localhost:8001/api/standup | jq '.'
```

### Open Web Interfaces
```bash
# Open personality preferences
open http://localhost:8081/personality-preferences

# Open main chat interface
open http://localhost:8081/

# Open standup generator
open http://localhost:8081/standup
```

## Port History (For Reference)
- **Legacy ports** (no longer used): 8000, 8080, 3000
- **Current stable ports**: 8001 (API), 8081 (Web)
- **Port assignment**: Fixed in infrastructure, not configurable

## Troubleshooting

### Connection Issues
1. **Cannot reach 8081**: Web server not running
   ```bash
   # Check if web server is running
   lsof -i :8081
   ```

2. **Cannot reach 8001**: API server not running
   ```bash
   # Check if API server is running
   lsof -i :8001
   ```

3. **Wrong port in browser**: Always use 8081 for web interface

### Common Mistakes
- ❌ Using http://localhost:8000 (old port)
- ❌ Using http://localhost:8080 (old port)
- ❌ Using http://localhost:3000 (old port)
- ✅ Using http://localhost:8081 (correct web UI)
- ✅ Using http://localhost:8001 (correct API)

---

**Last Updated**: September 11, 2025
**Status**: Production Infrastructure
**Note**: These ports are fixed and should not be changed without updating all documentation
