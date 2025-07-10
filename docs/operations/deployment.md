# Piper Morgan 1.0 - Deployment Guide

## Infrastructure Requirements

### System Requirements
- **CPU**: 2+ cores
- **Memory**: 4GB+ RAM (8GB+ recommended)
- **Storage**: 20GB+ available space
- **Network**: Internet access for AI APIs

### Software Dependencies
- Docker 20.10+
- Docker Compose 2.0+
- Git
- Python 3.11+ (for running API server)

## Local Deployment

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd piper-morgan-product

# Configure environment
cp .env.example .env
# Edit .env with required API keys:
# - ANTHROPIC_API_KEY
# - OPENAI_API_KEY
# - GITHUB_TOKEN (optional for GitHub integration)

# Deploy infrastructure
docker-compose up -d

# Wait for services to be ready (especially postgres health check)
docker-compose logs -f postgres

# Start the API server (not yet containerized)
cd services
python -m uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload

# Start the web interface (PM-011 feature)
cd ../web
python app.py  # Streamlit interface on http://localhost:8501

# Verify deployment
curl http://localhost:8001/health
```

### Service Configuration

#### Environment Variables
```bash
# AI Services (REQUIRED)
ANTHROPIC_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key

# External Integrations (OPTIONAL)
GITHUB_TOKEN=your_github_token  # For GitHub issue creation

# Database Configuration (with current dev defaults)
POSTGRES_USER=piper
POSTGRES_PASSWORD=dev_changeme_in_production  # ⚠️ CHANGE FOR PRODUCTION!
POSTGRES_DB=piper_morgan
DATABASE_URL=postgresql://piper:dev_changeme_in_production@localhost:5433/piper_morgan

# Application Settings
LOG_LEVEL=INFO
DEBUG=false
APP_ENV=development
```

#### Docker Compose Services
- **postgres** (port 5433): Primary database with health checks
- **redis** (port 6379): Event queue and caching
- **chromadb** (port 8000): Vector database for knowledge base
- **temporal** (port 7233, UI on 8088): Workflow orchestration engine
- **traefik** (port 80, 8090): API gateway and load balancer

### Service Verification Steps
1. **Check all services**: `docker-compose ps` (all should show "running" and "healthy")
2. **Verify API health**: `curl http://localhost:8001/health`
3. **Test PostgreSQL**: `docker-compose exec postgres pg_isready -U piper`
4. **Test Redis**: `docker-compose exec redis redis-cli ping`
5. **Test ChromaDB**: `curl http://localhost:8000/api/v1/heartbeat`
6. **Test Temporal**: Access web UI at `http://localhost:8088`
7. **Access Web Interface**: Open browser to `http://localhost:8501`

### Application Startup (Current Development State)
**Note**: The application layer is in active development with these components:

1. **API Server** (manual start required):
   ```bash
   cd services
   python -m uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
   ```

2. **Web Interface** (PM-011 addition):
   ```bash
   cd web
   python app.py  # Starts Streamlit on port 8501
   ```

3. **Database Schema**: SQLAlchemy automatically creates tables on first run (no init script needed)

4. **Knowledge Base**: Upload documents through web interface or API

## Production Considerations

### Security (CRITICAL for production)
- **Change default passwords**: Especially `POSTGRES_PASSWORD`
- **Configure SSL/TLS**: Use proper certificates, not self-signed
- **API security**: Implement authentication and authorization
- **Network security**: Use private networks, firewall rules
- **Secret management**: Use proper secret management system

### Monitoring (Limited implementation)
- **Health checks**: Basic endpoints available at `/health`
- **Container monitoring**: Docker health checks implemented
- **Application logs**: Structured logging to stdout (development level)
- **Performance monitoring**: Not yet implemented

### Backup (Not yet implemented)
- **Database backup**: PostgreSQL backup procedures needed
- **Knowledge base backup**: ChromaDB persistence configured
- **Configuration backup**: Environment and Docker configurations
- **Disaster recovery**: Planning phase only

### Scaling (Architecture supports, implementation partial)
- **Horizontal scaling**: Stateless app design supports load balancing
- **Database scaling**: PostgreSQL connection pooling configured
- **Cache scaling**: Redis clustering support available
- **Resource limits**: Docker resource constraints not configured

## Troubleshooting

### Common Issues

1. **Services fail to start**
   ```bash
   # Check logs for specific service
   docker-compose logs <service-name>

   # Common causes:
   # - Port conflicts (5433, 6379, 8000, 7233, 8088, 80, 8001, 8501)
   # - Insufficient memory
   # - Missing environment variables
   ```

2. **Database connection failures**
   ```bash
   # Check postgres health
   docker-compose exec postgres pg_isready -U piper

   # Verify environment variables
   echo $POSTGRES_PASSWORD

   # Check database exists
   docker-compose exec postgres psql -U piper -d piper_morgan -c "\dt"

   # Note: PostgreSQL is on port 5433, not default 5432!
   ```

3. **API key errors**
   ```bash
   # Verify environment file
   cat .env | grep API_KEY

   # Check application logs
   # API server logs visible in terminal where uvicorn runs
   ```

4. **Web interface issues**
   ```bash
   # Check Streamlit is running
   ps aux | grep streamlit

   # Verify port 8501 is available
   lsof -i :8501

   # Check Streamlit logs in terminal
   ```

### Debug Commands
```bash
# Check service logs
docker-compose logs -f <service-name>

# Access database (note port 5433)
docker-compose exec postgres psql -U piper -d piper_morgan

# Check Redis
docker-compose exec redis redis-cli ping

# View ChromaDB collections
curl http://localhost:8000/api/v1/collections

# Test intent processing via API
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message":"test intent"}'

# Check Temporal workflows
# Visit http://localhost:8088 in browser
```

## Current System Status

**PM-011 Release Status**:
- ✅ Web chat interface implemented
- ✅ File upload functionality
- ✅ Basic workflow execution
- ✅ Intent classification working
- 🔄 GitHub integration 70% complete
- 📋 Authentication not implemented
- 📋 Multi-user support pending

For operational monitoring details, see [Monitoring Guide](monitoring.md).
For configuration options, see [Configuration Guide](configuration.md).

---
*Last Updated: June 27, 2025*

## Revision Log
- **June 27, 2025**: Updated for PM-011 web interface, corrected PostgreSQL port to 5433, added current system status
