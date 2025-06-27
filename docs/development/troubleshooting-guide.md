# Piper Morgan 1.0 - Troubleshooting Guide

## Overview

This guide addresses common issues encountered during Piper Morgan development and deployment. Issues are organized by category with step-by-step resolution procedures.

## Environment Setup Issues

### Docker Services Won't Start

**Symptoms:**
- `docker-compose up -d` fails
- Port conflicts (5432, 6379, 8000)
- Service health checks failing

**Resolution:**
```bash
# Check for port conflicts
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :8000  # ChromaDB

# Stop conflicting services
brew services stop postgresql  # If Homebrew PostgreSQL running
sudo systemctl stop redis     # If system Redis running

# Clean up Docker state
docker-compose down --volumes
docker system prune -f
docker-compose up -d

# Verify services
docker-compose ps
```

**Common Causes:**
- Homebrew PostgreSQL claiming port 5432
- Previous Docker containers not cleaned up
- Insufficient Docker resources allocated

### Python Environment Issues

**Symptoms:**
- Import errors despite installed packages
- `ModuleNotFoundError` for local services
- Type checking failures

**Resolution:**
```bash
# Ensure virtual environment activated
source venv/bin/activate

# Verify Python path includes project root
python -c "import sys; print('\n'.join(sys.path))"

# Reinstall dependencies
pip install -r requirements.txt

# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify imports work
python -c "from services.domain.models import Project; print('OK')"
```

### Environment Variables Not Loading

**Symptoms:**
- `None` values for API keys
- Services failing with authentication errors
- "API key not found" messages

**Resolution:**
```bash
# Check .env file exists and is readable
ls -la .env
cat .env | grep -v "^#" | head -5  # Don't expose keys

# Verify load_dotenv() calls
grep -r "load_dotenv" services/

# Test environment loading
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('ANTHROPIC_API_KEY set:', bool(os.getenv('ANTHROPIC_API_KEY')))
"
```

**Critical Fix Pattern:**
```python
# Always add at top of modules using os.getenv()
from dotenv import load_dotenv
load_dotenv()  # BEFORE any os.getenv() calls

import os
api_key = os.getenv('ANTHROPIC_API_KEY')
```

## Runtime Issues

### Intent Classification Failures

**Symptoms:**
- Low confidence scores (<0.5)
- Incorrect intent categories
- "UNKNOWN" classifications for valid requests

**Diagnosis:**
```bash
# Check LLM service status
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "test classification"}'

# Enable debug logging
export LOG_LEVEL=DEBUG
```

**Resolution:**
- **Knowledge Base Issues**: Upload more relevant PM documents
- **Prompt Problems**: Check intent classification prompts for clarity
- **API Failures**: Verify Claude/OpenAI API keys and quotas
- **Context Missing**: Ensure knowledge search returns relevant results

### Database Connection Errors

**Symptoms:**
- `sqlalchemy.exc.OperationalError`
- "Connection refused" to PostgreSQL
- Workflow state not persisting

**Resolution:**
```bash
# Check PostgreSQL container
docker logs piper-postgres

# Test database connection
python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test():
    engine = create_async_engine('postgresql+asyncpg://piper:dev_changeme@localhost/piper_morgan')
    async with engine.begin() as conn:
        result = await conn.execute('SELECT 1')
        print('DB connection OK:', result.scalar())
    await engine.dispose()

asyncio.run(test())
"

# Initialize database schema
python -c "
import asyncio
from services.database.session import init_database
asyncio.run(init_database())
"
```

### Knowledge Base Search Issues

**Symptoms:**
- Poor search relevance
- Empty search results
- ChromaDB connection errors

**Diagnosis:**
```bash
# Check ChromaDB status
curl http://localhost:8000/api/v1/version

# Verify document ingestion
python -c "
import chromadb
client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_collection('pm_knowledge')
print('Document count:', collection.count())
"
```

**Resolution:**
- **Empty Collection**: Re-run document ingestion
- **Poor Relevance**: Tune chunking strategy and embedding parameters
- **Connection Issues**: Restart ChromaDB container

## API Issues

### 404 Not Found Errors

**Symptoms:**
- API endpoints return 404
- FastAPI not starting correctly
- Route registration failures

**Diagnosis:**
```bash
# Check FastAPI startup logs
docker logs piper-api  # If containerized
# OR
python main.py  # Direct startup

# Verify routes registered
curl http://localhost:8001/docs  # OpenAPI docs
```

**Common Causes:**
- Missing route registration in main.py
- Import errors in route modules
- Port conflicts or service not starting

### 422 Validation Errors

**Symptoms:**
- Request validation failures
- Pydantic model errors
- Missing required fields

**Resolution:**
```bash
# Test with valid request format
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a ticket for login bug",
    "session_id": "test-123"
  }'

# Check API documentation
open http://localhost:8001/docs
```

### 500 Internal Server Errors

**Symptoms:**
- Unhandled exceptions
- Service crashes
- Database transaction failures

**Diagnosis:**
```bash
# Check application logs
tail -f logs/app.log

# Enable detailed error tracking
export LOG_LEVEL=DEBUG
export SHOW_ERROR_DETAILS=true
```

**Common Causes:**
- Uninitialized database schemas
- Missing environment variables
- Service dependency failures

## Testing Issues

### Async Test Failures

**Symptoms:**
- `RuntimeError: This event loop is already running`
- Test timeouts
- Fixture dependency errors

**Resolution:**
```python
# Ensure proper async test setup
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None

# Configure pytest.ini
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Test Database Issues

**Symptoms:**
- Tests interfering with each other
- Database state not cleaned
- Connection pool exhaustion

**Resolution:**
```python
# Use isolated test database
@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
```

### Mock Configuration Problems

**Symptoms:**
- Mocks not applying correctly
- Real API calls during tests
- Inconsistent test results

**Resolution:**
```python
# Proper mock setup
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_llm_client():
    client = Mock()
    client.complete = AsyncMock(return_value="test response")
    return client

# Verify mock calls
def test_with_mock(mock_llm_client):
    # ... test code ...
    mock_llm_client.complete.assert_called_once()
```

## Performance Issues

### Slow Response Times

**Symptoms:**
- API responses >5 seconds
- Knowledge search timeouts
- Workflow execution delays

**Diagnosis:**
```bash
# Profile API performance
time curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "list projects"}'

# Check database query performance
export LOG_LEVEL=DEBUG  # Shows SQL queries
```

**Optimization Steps:**
1. **Database**: Add indexes, optimize queries
2. **Knowledge Search**: Reduce search scope, tune parameters
3. **Caching**: Implement Redis caching for frequent queries
4. **Concurrency**: Use async operations properly

### Memory Usage Issues

**Symptoms:**
- Increasing memory consumption
- Out of memory errors
- Container restarts

**Monitoring:**
```bash
# Monitor container memory
docker stats

# Python memory profiling
pip install memory-profiler
python -m memory_profiler your_script.py
```

## Development Workflow Issues

### Git Workflow Problems

**Symptoms:**
- Merge conflicts in generated files
- Branch synchronization issues
- Lost work due to force pushes

**Best Practices:**
```bash
# Create feature branch
git checkout -b feature/pm-XXX-description

# Regular commits with clear messages
git commit -m "PM-009: Add project context resolution

- Implement ProjectContext class
- Add session memory for project tracking
- Update workflow factory integration"

# Sync with main regularly
git fetch origin
git rebase origin/main
```

### Code Review Issues

**Symptoms:**
- Architectural drift
- Pattern violations
- Missing tests

**Prevention:**
```bash
# Pre-commit checks
grep -r "create.*workflow" services/  # Check patterns
mypy services/  # Type checking
pytest  # All tests pass
```

## Debugging Techniques

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Add context to all log entries
logger.info(
    "processing_intent",
    intent_id=intent.id,
    category=intent.category.value,
    confidence=intent.confidence,
    user_id=session_id
)
```

### Interactive Debugging

```python
# Drop into debugger on errors
import pdb; pdb.set_trace()

# Or use ipdb for better interface
import ipdb; ipdb.set_trace()

# VS Code debugging
# Set breakpoints in IDE and run with debugger
```

### Health Check Endpoints

```bash
# System health
curl http://localhost:8001/api/v1/health

# Individual service checks
curl http://localhost:8000/api/v1/version  # ChromaDB
curl http://localhost:8088/  # Temporal UI
```

## Emergency Procedures

### Complete System Reset

```bash
# Nuclear option - reset everything
docker-compose down --volumes
docker system prune -a -f
rm -rf data/  # Clears all persistent data
docker-compose up -d

# Reinitialize
python -c "
import asyncio
from services.database.session import init_database
asyncio.run(init_database())
"

# Re-upload knowledge base
python scripts/upload_docs.py  # If exists
```

### Data Recovery

```bash
# Backup before major changes
docker exec piper-postgres pg_dump -U piper piper_morgan > backup.sql

# Restore from backup
docker exec -i piper-postgres psql -U piper piper_morgan < backup.sql
```

## Getting Help

### Log Analysis

**Check these locations:**
- Application logs: `logs/app.log`
- Docker logs: `docker-compose logs [service]`
- System logs: `/var/log/` (production)

### Useful Commands

```bash
# Service status overview
docker-compose ps

# Resource usage
docker stats --no-stream

# Network connectivity
docker-compose exec api ping postgres

# Database inspection
docker-compose exec postgres psql -U piper -d piper_morgan -c "\dt"
```

### External Resources

- **FastAPI Issues**: [FastAPI GitHub Issues](https://github.com/tiangolo/fastapi/issues)
- **SQLAlchemy Async**: [Official Async Guide](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
- **Docker Compose**: [Compose Troubleshooting](https://docs.docker.com/compose/troubleshooting/)
- **ChromaDB**: [ChromaDB Documentation](https://docs.trychroma.com/)

## Prevention Strategies

### Regular Maintenance

```bash
# Weekly cleanup
docker system prune -f
docker-compose pull  # Update images

# Monthly tasks
pip list --outdated  # Check for updates
brew update && brew upgrade  # Update system tools
```

### Monitoring Setup

```python
# Add health checks to critical services
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "database": await check_database(),
            "chromadb": await check_chromadb(),
            "redis": await check_redis()
        }
    }
```

---
*Last Updated: June 21, 2025*

## Revision Log
- **June 21, 2025**: Initial troubleshooting guide creation with common Piper Morgan issues