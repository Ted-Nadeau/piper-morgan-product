# Piper Morgan - Configuration Guide

## Overview

This guide covers all configuration options for the Piper Morgan system, including environment variables, service configurations, and runtime settings.

## Environment Configuration

### Required Environment Variables

Create a `.env` file in the project root with these required settings:

```bash
# AI Service API Keys (REQUIRED)
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# External Integration Keys (OPTIONAL)
GITHUB_TOKEN=your_github_personal_access_token

# Database Configuration
POSTGRES_USER=piper
POSTGRES_PASSWORD=dev_changeme_in_production  # ⚠️ CHANGE IN PRODUCTION
POSTGRES_DB=piper_morgan
DATABASE_URL=postgresql://piper:dev_changeme_in_production@localhost:5433/piper_morgan

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=  # Set for production

# Application Settings
APP_ENV=development  # development, staging, production
LOG_LEVEL=INFO      # DEBUG, INFO, WARNING, ERROR
DEBUG=false         # Enable debug mode
```

### Optional Configuration

```bash
# Performance Tuning
MAX_WORKERS=4
REQUEST_TIMEOUT=30
MAX_RETRIES=3

# Feature Flags
ENABLE_CLARIFYING_QUESTIONS=false
ENABLE_MULTI_REPO=false
ENABLE_LEARNING=false

# LLM Configuration
CLAUDE_MODEL=claude-3-opus-20240229
OPENAI_MODEL=gpt-4
EMBEDDING_MODEL=text-embedding-3-small

# Knowledge Base
CHROMA_PERSIST_DIR=./chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Session Management
SESSION_TIMEOUT_MINUTES=30
MAX_SESSIONS_PER_USER=5
```

## Service Configuration

### Docker Compose Configuration

**Development** (`docker-compose.yml`):
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    environment:
      CHROMA_SERVER_HOST: 0.0.0.0
      CHROMA_SERVER_PORT: 8000
    volumes:
      - chroma_data:/chroma/data

volumes:
  postgres_data:
  redis_data:
  chroma_data:
```

**Production** (`docker-compose.prod.yml`):
```yaml
# Override file for production
version: '3.8'

services:
  postgres:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD_PROD}
    restart: always
    deploy:
      resources:
        limits:
          memory: 2G

  redis:
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    restart: always

  api:
    environment:
      APP_ENV: production
      LOG_LEVEL: WARNING
    restart: always
```

### API Configuration

**API Server Settings** (`services/api/config.py`):
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Settings
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Piper Morgan API"
    version: str = "1.0.0-PM-011"

    # CORS Settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]

    # Rate Limiting
    rate_limit_enabled: bool = False
    rate_limit_per_minute: int = 60

    # File Upload
    max_upload_size: int = 50 * 1024 * 1024  # 50MB
    allowed_file_types: list = [".pdf", ".txt", ".md", ".docx"]

    class Config:
        env_file = ".env"
```

### Database Configuration

**SQLAlchemy Settings**:
```python
# Database connection pool
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 10
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = 1800
```

**Alembic Migration Config** (`alembic.ini`):
```ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql://piper:dev_changeme_in_production@localhost:5433/piper_morgan

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic
```

## LLM Provider Configuration

### Claude Configuration
```python
# Claude API settings
CLAUDE_CONFIG = {
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "model": os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229"),
    "max_tokens": 1000,
    "temperature": 0.7,
    "timeout": 30,
}
```

### OpenAI Configuration
```python
# OpenAI API settings
OPENAI_CONFIG = {
    "api_key": os.getenv("OPENAI_API_KEY"),
    "model": os.getenv("OPENAI_MODEL", "gpt-4"),
    "embedding_model": os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
    "max_tokens": 1000,
    "temperature": 0.7,
    "timeout": 30,
}
```

## Knowledge Base Configuration

### ChromaDB Settings
```python
# Vector database configuration
CHROMA_CONFIG = {
    "persist_directory": os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"),
    "collection_name": "piper_morgan_knowledge",
    "distance_function": "cosine",
}

# Document processing
DOCUMENT_CONFIG = {
    "chunk_size": int(os.getenv("CHUNK_SIZE", 1000)),
    "chunk_overlap": int(os.getenv("CHUNK_OVERLAP", 200)),
    "separators": ["\n\n", "\n", " ", ""],
}
```

## Logging Configuration

### Python Logging
```python
import logging
from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "logs/piper_morgan.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "root": {
        "level": os.getenv("LOG_LEVEL", "INFO"),
        "handlers": ["console", "file"]
    }
}

# Apply configuration
dictConfig(LOGGING_CONFIG)
```

## Configuration Management

### Loading Configuration
```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration class
class Config:
    """Centralized configuration management"""

    def __init__(self):
        self.validate_required_vars()

    def validate_required_vars(self):
        """Ensure required environment variables are set"""
        required = [
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "DATABASE_URL"
        ]

        missing = [var for var in required if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")

    @property
    def is_production(self):
        return os.getenv("APP_ENV") == "production"

    @property
    def is_debug(self):
        return os.getenv("DEBUG", "false").lower() == "true"

# Singleton instance
config = Config()
```

### Feature Flags
```python
class FeatureFlags:
    """Manage feature toggles"""

    @staticmethod
    def is_enabled(feature: str) -> bool:
        """Check if feature is enabled"""
        env_var = f"ENABLE_{feature.upper()}"
        return os.getenv(env_var, "false").lower() == "true"

# Usage
if FeatureFlags.is_enabled("clarifying_questions"):
    # Feature-specific code
    pass
```

## Deployment Configuration

### Production Checklist
- [ ] Set strong passwords for all services
- [ ] Configure SSL/TLS certificates
- [ ] Set appropriate resource limits
- [ ] Enable production logging
- [ ] Configure backup schedules
- [ ] Set up monitoring alerts
- [ ] Review firewall rules
- [ ] Enable rate limiting
- [ ] Configure session timeouts
- [ ] Set appropriate CORS origins

### Environment-Specific Files
```
.env                 # Local development
.env.staging         # Staging environment
.env.production      # Production environment
.env.example         # Template with all variables
```

### Configuration Validation Script
```bash
#!/bin/bash
# validate_config.sh

echo "Validating configuration..."

# Check required variables
required_vars=(
    "ANTHROPIC_API_KEY"
    "OPENAI_API_KEY"
    "DATABASE_URL"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "ERROR: $var is not set"
        exit 1
    fi
done

echo "Configuration valid!"
```

## Credential Recovery Procedures

### Lost PostgreSQL Password

**Option 1: Docker Volume Reset (Development Only)**
```bash
# ⚠️ WARNING: This destroys all database data!
docker-compose down
docker volume rm piper-morgan-product_postgres_data
docker-compose up -d postgres

# Database will recreate with password from .env
```

**Option 2: Password Reset via Docker**
```bash
# Connect as postgres superuser
docker-compose exec postgres psql -U postgres

# Reset the piper user password
ALTER USER piper WITH PASSWORD 'new_password_here';

# Update .env and DATABASE_URL with new password
```

**Option 3: Trust Authentication (Emergency)**
```bash
# Edit postgresql.conf in container
docker-compose exec postgres bash
echo "local all all trust" >> /var/lib/postgresql/data/pg_hba.conf

# Restart postgres
docker-compose restart postgres

# Connect without password and reset
docker-compose exec postgres psql -U piper -d piper_morgan
ALTER USER piper WITH PASSWORD 'new_password';

# ⚠️ Remove trust auth immediately after!
```

### Lost Redis Password

```bash
# If Redis has no password set (dev default)
docker-compose exec redis redis-cli

# If password was set and lost
docker-compose down redis
docker volume rm piper-morgan-product_redis_data
docker-compose up -d redis
# Redis will start fresh without password
```

### Lost API Keys

**Anthropic Claude API Key**
1. Log into https://console.anthropic.com
2. Navigate to API Keys section
3. Revoke old key if compromised
4. Generate new key
5. Update `.env` file

**OpenAI API Key**
1. Log into https://platform.openai.com
2. Go to API keys page
3. Delete old key if needed
4. Create new secret key
5. Update `.env` file

**GitHub Personal Access Token**
1. Go to GitHub Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Delete old token
4. Generate new token with 'repo' scope
5. Update `.env` file

### Lost ChromaDB Data

```bash
# ChromaDB persists to disk
# If data corrupted, rebuild knowledge base:
docker-compose down chromadb
docker volume rm piper-morgan-product_chroma_data
docker-compose up -d chromadb

# Re-upload documents through API
curl -X POST http://localhost:8001/api/v1/knowledge/upload \
  -F "file=@/path/to/document.pdf"
```

### Emergency Recovery Checklist

1. **Backup Current State**
   ```bash
   # Before any recovery attempts
   docker-compose exec postgres pg_dump -U piper piper_morgan > backup.sql
   cp .env .env.backup
   ```

2. **Document What's Lost**
   - Which service/credential?
   - When last known working?
   - Any error messages?

3. **Recovery Priority**
   - Database access (most critical)
   - API keys (can regenerate)
   - Cache data (can rebuild)

4. **Post-Recovery**
   - Update all `.env` files
   - Test all service connections
   - Document new credentials securely
   - Update team password manager

### Preventing Credential Loss

**Development Best Practices**
```bash
# Keep encrypted backup of .env
gpg -c .env  # Creates .env.gpg
# Decrypt when needed: gpg -d .env.gpg > .env

# Use password manager for team
# Store in 1Password, Bitwarden, etc.

# Regular backups
./scripts/backup_config.sh  # Create this script
```

**Production Recommendations**
- Use secrets management service (AWS Secrets Manager, HashiCorp Vault)
- Implement key rotation policies
- Set up automated backups
- Document recovery procedures
- Test recovery quarterly

---
*Note: Always use environment variables for sensitive configuration. Never commit secrets to version control. This guide covers both current configuration options and planned enhancements.*
---
*Last Updated: June 27, 2025*

## Revision Log
- **June 27, 2025**: Added systematic documentation dating and revision tracking
