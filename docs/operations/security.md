# Piper Morgan - Security Guide

## Overview

This guide outlines security practices for the Piper Morgan system. While basic security measures are in place, comprehensive security hardening is required before production deployment.

## Current Security Implementation

### API Key Management

**Environment Variables**
```bash
# Required API keys stored in .env file
ANTHROPIC_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key
GITHUB_TOKEN=your_github_token

# Database credentials
POSTGRES_PASSWORD=dev_changeme  # ⚠️ MUST change for production
```

**Best Practices in Use**:
- ✅ API keys stored in environment variables
- ✅ `.env` file excluded from version control
- ✅ No hardcoded credentials in code
- ⚠️ No key rotation mechanism yet
- ⚠️ No audit logging for key usage

### Data Privacy

**Current Measures**:
- Documents processed locally only
- No unauthorized data transmission
- User consent required for GitHub operations
- Knowledge base stored locally in ChromaDB

**Gaps**:
- No data encryption at rest
- No user-level access controls
- No data retention policies
- No GDPR compliance measures

## Security Architecture

### Authentication & Authorization

**Current State**: 🚨 **MISSING**
- No user authentication system
- No role-based access control
- Anyone can access any functionality
- No session management

**Target State**:
```python
# Planned authentication flow
@app.post("/auth/login")
async def login(credentials: UserCredentials):
    # Validate credentials
    # Generate JWT token
    # Return secure session

@app.get("/api/protected")
@require_auth
async def protected_endpoint(user: AuthenticatedUser):
    # User-specific access only
```

### Network Security

**Docker Network Isolation**
```yaml
# Current: Basic network setup
networks:
  piper-net:
    driver: bridge

# Planned: Segmented networks
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

**Service Communication**:
- Internal services on private network
- Only API gateway exposed publicly
- Database not accessible externally

## Security Checklist

### Pre-Production Requirements

#### 🔴 Critical Security Items
- [ ] Change all default passwords
- [ ] Implement user authentication
- [ ] Enable HTTPS/TLS for all endpoints
- [ ] Set up API rate limiting
- [ ] Implement audit logging
- [ ] Configure firewall rules
- [ ] Enable database encryption

#### 🟡 Important Security Items
- [ ] Set up key rotation policies
- [ ] Implement CORS properly
- [ ] Add input validation/sanitization
- [ ] Configure security headers
- [ ] Set up intrusion detection
- [ ] Create incident response plan

#### 🟢 Good Practice Items
- [ ] Regular security audits
- [ ] Dependency vulnerability scanning
- [ ] Security training for team
- [ ] Penetration testing
- [ ] Compliance documentation

## Secure Configuration

### Environment Variables
```bash
# Production .env template
NODE_ENV=production

# Strong passwords (generate with: openssl rand -base64 32)
POSTGRES_PASSWORD=<strong-password>
REDIS_PASSWORD=<strong-password>
JWT_SECRET=<strong-secret>

# API Keys (from providers)
ANTHROPIC_API_KEY=<your-key>
OPENAI_API_KEY=<your-key>
GITHUB_TOKEN=<your-token>

# Security settings
ENABLE_HTTPS=true
ENABLE_RATE_LIMITING=true
MAX_REQUESTS_PER_MINUTE=60
SESSION_TIMEOUT_MINUTES=30
```

### Docker Security
```yaml
# docker-compose.prod.yml
services:
  api:
    # Run as non-root user
    user: "1000:1000"
    # Read-only root filesystem
    read_only: true
    # Limit resources
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    # Security options
    security_opt:
      - no-new-privileges:true
```

## Input Validation

### Current Implementation
- Basic validation in domain models
- Type checking via Pydantic

### Required Enhancements
```python
# Example secure input handling
from pydantic import BaseModel, validator
import re

class SecureIntentRequest(BaseModel):
    message: str
    project_id: Optional[str]
    
    @validator('message')
    def validate_message(cls, v):
        # Prevent injection attacks
        if len(v) > 1000:
            raise ValueError("Message too long")
        if re.search(r'[<>]', v):
            raise ValueError("Invalid characters")
        return v
    
    @validator('project_id')
    def validate_project_id(cls, v):
        if v and not re.match(r'^[a-zA-Z0-9-]+$', v):
            raise ValueError("Invalid project ID format")
        return v
```

## API Security

### Rate Limiting (Planned)
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/intent")
@limiter.limit("10/minute")
async def create_intent(request: Request):
    # Rate-limited endpoint
```

### Authentication (Planned)
```python
from fastapi_jwt_auth import AuthJWT

@app.post("/api/v1/intent")
async def create_intent(
    request: IntentRequest,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    # Process with user context
```

## Secrets Management

### Development
- Use `.env` files
- Never commit secrets
- Rotate keys regularly

### Production (Recommended)
- Use AWS Secrets Manager or similar
- Implement key rotation
- Audit access logs
- Encrypt secrets at rest

## Security Monitoring

### Audit Logging (Planned)
```python
# Log security events
async def log_security_event(
    event_type: str,
    user_id: str,
    details: dict
):
    await security_logger.log({
        "timestamp": datetime.utcnow(),
        "event_type": event_type,
        "user_id": user_id,
        "ip_address": request.client.host,
        "details": details
    })
```

### Security Alerts
- Failed authentication attempts
- Unusual API usage patterns
- Unauthorized access attempts
- Configuration changes

## Incident Response

### Response Plan (Template)
1. **Detect**: Monitor for security events
2. **Assess**: Determine severity and scope
3. **Contain**: Isolate affected systems
4. **Eradicate**: Remove threat
5. **Recover**: Restore normal operations
6. **Review**: Document lessons learned

### Emergency Contacts
- Security Lead: [TBD]
- System Admin: [TBD]
- Executive Sponsor: [TBD]

## Compliance Considerations

### Data Protection
- Implement GDPR compliance if handling EU data
- Define data retention policies
- Enable user data export/deletion
- Document data flows

### Industry Standards
- Follow OWASP Top 10 guidelines
- Implement CIS Docker benchmarks
- Consider SOC 2 compliance
- Regular security assessments

---
*Note: This security guide reflects current basic security measures and required enhancements. Full security implementation is tracked as PM-T002 in the technical backlog.*
---
*Last Updated: June 27, 2025*

## Revision Log
- **June 27, 2025**: Post-PM-011 consolidation: Updated deployment/user guides for web interface, fixed PostgreSQL port, added monitoring/security/config documentation
- **June 27, 2025**: Added systematic documentation dating and revision tracking
