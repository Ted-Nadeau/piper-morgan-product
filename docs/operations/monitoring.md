# Piper Morgan - Monitoring Guide

## Overview

This guide covers monitoring strategies for the Piper Morgan system. While comprehensive monitoring is planned, current implementation provides basic health checks and logging.

## Current Monitoring Capabilities

### Health Checks

**API Health Endpoint**
```bash
# Basic health check
curl http://localhost:8001/health

# Expected response
{
  "status": "healthy",
  "version": "1.0.0-PM-011",
  "services": {
    "database": "connected",
    "redis": "connected",
    "chromadb": "connected"
  }
}
```

### Docker Service Monitoring

**Service Status Checks**
```bash
# View all service status
docker-compose ps

# Check specific service health
docker-compose exec postgres pg_isready -U piper
docker-compose exec redis redis-cli ping
curl http://localhost:8000/api/v1/heartbeat  # ChromaDB
```

**Service Logs**
```bash
# View all logs
docker-compose logs -f

# Service-specific logs
docker-compose logs -f postgres
docker-compose logs -f api
docker-compose logs -f temporal
```

### Application Logging

**Current Implementation**
- Structured logging to stdout (development level)
- No correlation IDs yet implemented
- Basic error logging in place

**Log Locations**
```bash
# Application logs (when containerized)
docker-compose logs app

# Manual API server logs
# Visible in terminal where uvicorn is running
```

## Planned Monitoring Enhancements

### Application Performance Monitoring (APM)
**Target State**: Comprehensive metrics dashboard
- Request/response times
- Error rates by endpoint
- Workflow completion metrics
- LLM API call performance

### Business Metrics
**Target State**: PM-specific metrics tracking
- Workflows completed per day
- Intent classification accuracy
- Knowledge base query relevance
- User satisfaction scores

### Infrastructure Monitoring
**Target State**: Full observability stack
- CPU/Memory/Disk usage per service
- Network latency between services
- Database query performance
- Cache hit rates

## Monitoring Architecture (Planned)

```
┌─────────────────┐
│   Prometheus    │ ← Metrics collection
└────────┬────────┘
         │
┌────────▼────────┐
│    Grafana      │ ← Visualization
└────────┬────────┘
         │
┌────────▼────────┐
│   Alert Manager │ ← Alerting
└─────────────────┘
```

## Key Metrics to Monitor

### System Health
- **Uptime**: Service availability percentage
- **Response Time**: P50, P95, P99 latencies
- **Error Rate**: 4xx and 5xx responses
- **Resource Usage**: CPU, memory, disk

### Application Metrics
- **Intent Classification**: Success rate, confidence scores
- **Workflow Execution**: Completion rate, duration
- **Knowledge Queries**: Relevance scores, response times
- **External APIs**: Call rates, failures, costs

### Business Metrics
- **User Engagement**: Daily active users, session length
- **Feature Usage**: Most used intents, workflow types
- **Quality Metrics**: Issue revision rates, user feedback
- **Cost Tracking**: LLM API usage, infrastructure costs

## Troubleshooting Guide

### Common Issues

**High Memory Usage**
```bash
# Check container memory
docker stats

# Identify memory-heavy processes
docker-compose exec <service> top
```

**Slow Response Times**
```bash
# Check database performance
docker-compose exec postgres psql -U piper -c "SELECT * FROM pg_stat_activity;"

# Review Redis performance
docker-compose exec redis redis-cli --latency
```

**Service Failures**
```bash
# Check service logs
docker-compose logs <service> --tail=100

# Restart problematic service
docker-compose restart <service>
```

## Alerting Strategy (Planned)

### Critical Alerts
- Service down > 1 minute
- Error rate > 10%
- Response time > 5s (P95)
- Disk usage > 90%

### Warning Alerts
- Error rate > 5%
- Response time > 2s (P95)
- Memory usage > 80%
- Failed LLM API calls > 10/hour

## Implementation Roadmap

### Phase 1: Basic Monitoring ✅
- Health endpoints
- Docker health checks
- Basic logging

### Phase 2: Metrics Collection (Next)
- Prometheus integration
- Application metrics export
- Grafana dashboards

### Phase 3: Advanced Monitoring
- Distributed tracing
- Log aggregation
- Predictive alerting

## Configuration

### Environment Variables
```bash
# Monitoring configuration (future)
METRICS_ENABLED=true
METRICS_PORT=9090
LOG_LEVEL=INFO
TRACE_ENABLED=false
```

### Docker Compose Addition (Planned)
```yaml
prometheus:
  image: prom/prometheus:latest
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

## Best Practices

1. **Start Simple**: Focus on key metrics first
2. **Set Baselines**: Understand normal behavior
3. **Automate Alerts**: Reduce manual monitoring
4. **Document Incidents**: Learn from failures
5. **Regular Reviews**: Adjust thresholds based on experience

---
*Note: This monitoring guide reflects the current state (basic health checks) and planned enhancements. Full monitoring implementation is part of the PM-T001 technical debt item.*
---
*Last Updated: June 27, 2025*

## Revision Log
- **June 27, 2025**: Post-PM-011 consolidation: Updated deployment/user guides for web interface, fixed PostgreSQL port, added monitoring/security/config documentation
- **June 27, 2025**: Added systematic documentation dating and revision tracking
