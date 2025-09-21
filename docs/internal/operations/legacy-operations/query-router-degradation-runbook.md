# QueryRouter Graceful Degradation - Operations Runbook

**PM-063: QueryRouter Graceful Degradation - Prevent Cascade Failures**

## Overview

The QueryRouter graceful degradation system prevents cascade failures by implementing circuit breakers and intelligent fallbacks for all query operations. This runbook provides operational procedures for monitoring, troubleshooting, and managing the degradation system.

## Current Status: PM-063 Implementation Complete (Method Level)

**Implementation Status**:
- ✅ **Unit Tests**: All 11 degradation tests passing
- ✅ **Circuit Breaker**: Robust failure handling with graceful degradation
- ✅ **Test Mode Coverage**: Graceful degradation for all 12 operations
- ❌ **Integration Tests**: 5/7 failing due to critical API integration issue
- ❌ **Production Ready**: Critical fix needed in `main.py` lines 310-330

**Critical Issue**: Missing return statement in normal flow causes `None` responses and 500 errors

## System Architecture

```
QueryRouter
├── QueryDegradationHandler
│   ├── QueryCircuitBreaker (MCP pattern-based)
│   ├── Database failure handlers
│   └── Service-specific fallbacks
├── Circuit breaker protection (ALL 12 operations)
├── Backward compatibility (test_mode preserved)
└── Monitoring integration
```

## Monitoring Dashboard

### Key Metrics to Monitor

| Metric | Normal Range | Warning Threshold | Critical Threshold |
|--------|-------------|-------------------|-------------------|
| Circuit Breaker State | "closed" | "half-open" | "open" |
| Degradation Activation Rate | <1% | 1-5% | >5% |
| Query Error Rate | <0.5% | 0.5-2% | >2% |
| Response Time P95 | <500ms | 500-1000ms | >1000ms |
| Failed Degradation Attempts | 0 | 1-3/hour | >3/hour |

### Monitoring Endpoints

- **Health Check**: `GET /api/v1/health/query-router`
- **Degradation Status**: `GET /api/v1/query-router/degradation-status`
- **Circuit Breaker Metrics**: `GET /api/v1/metrics/circuit-breakers`

### Sample Queries

```bash
# Check current degradation status
curl -s http://localhost:8001/api/v1/query-router/degradation-status | jq

# Monitor circuit breaker state
curl -s http://localhost:8001/api/v1/metrics/circuit-breakers | jq '.query_router.state'

# Test degradation behavior (requires admin privileges)
curl -X POST http://localhost:8001/api/v1/admin/test-degradation \
  -H "Content-Type: application/json" \
  -d '{"service": "project_queries", "action": "list_projects"}'
```

## Alert Definitions

### Critical Alerts

#### Circuit Breaker Open
**Condition**: Circuit breaker state = "open" for >5 minutes
**Impact**: All queries of affected service type are degraded
**Response**: Immediate investigation required

```yaml
alert: QueryRouterCircuitBreakerOpen
expr: query_router_circuit_breaker_state == 1
for: 5m
severity: critical
description: "QueryRouter circuit breaker has been open for {{ $value }} minutes"
```

#### High Degradation Rate
**Condition**: >10% of queries are degraded for >10 minutes
**Impact**: Poor user experience, potential underlying service issues
**Response**: Check service health and investigate root cause

```yaml
alert: QueryRouterHighDegradationRate
expr: (rate(query_router_degraded_responses_total[5m]) / rate(query_router_total_requests[5m])) > 0.1
for: 10m
severity: critical
description: "{{ $value }}% of QueryRouter requests are being degraded"
```

### Warning Alerts

#### Increased Error Rate
**Condition**: Query error rate >2% for >15 minutes
**Impact**: Elevated failure rate, circuit breaker may open soon
**Response**: Monitor closely, prepare for potential degradation

#### Response Time Degradation
**Condition**: P95 response time >1s for >20 minutes
**Impact**: Slow user experience, may indicate resource constraints
**Response**: Check system resources and database performance

## Troubleshooting Procedures

### Circuit Breaker is Open

1. **Immediate Assessment**
   ```bash
   # Check circuit breaker status
   curl -s http://localhost:8001/api/v1/query-router/degradation-status

   # Review recent error logs
   docker logs piper-morgan-api | grep -i "circuit.*breaker\|degradation" | tail -20
   ```

2. **Identify Root Cause**
   - Database connectivity issues
   - Service dependency failures
   - Resource exhaustion
   - Configuration problems

3. **Resolution Steps**
   ```bash
   # Check database connection
   docker exec -it piper-postgres pg_isready -U piper

   # Verify service dependencies
   docker-compose ps

   # Check resource usage
   docker stats piper-morgan-api

   # Review configuration
   env | grep -i circuit_breaker
   ```

4. **Manual Circuit Breaker Reset** (if needed)
   ```bash
   # Reset circuit breaker (admin endpoint)
   curl -X POST http://localhost:8001/api/v1/admin/reset-circuit-breaker \
     -H "Authorization: Bearer $ADMIN_TOKEN"
   ```

### Degradation Not Working

1. **Verify Feature Flags**
   ```bash
   # Check if degradation is enabled
   curl -s http://localhost:8001/api/v1/feature-flags | jq '.circuit_breakers'
   ```

2. **Check Configuration**
   ```bash
   # Verify environment variables
   env | grep -E "(CIRCUIT_BREAKER|DEGRADATION)" | sort
   ```

3. **Test Degradation Manually**
   ```bash
   # Enable test mode temporarily
   curl -X POST http://localhost:8001/api/v1/admin/enable-test-mode

   # Send test query
   curl -X POST http://localhost:8001/api/v1/intent \
     -H "Content-Type: application/json" \
     -d '{"message": "list all projects", "session_id": "test-session"}'
   ```

### Performance Issues

1. **Check Resource Usage**
   ```bash
   # Container resource usage
   docker stats piper-morgan-api piper-postgres piper-redis

   # System resource usage
   htop
   ```

2. **Database Performance**
   ```bash
   # Check database connections
   docker exec -it piper-postgres psql -U piper -d piper_morgan \
     -c "SELECT count(*) FROM pg_stat_activity;"

   # Check slow queries
   docker exec -it piper-postgres psql -U piper -d piper_morgan \
     -c "SELECT query, calls, total_exec_time FROM pg_stat_statements WHERE total_exec_time > 1000 ORDER BY total_exec_time DESC LIMIT 10;"
   ```

## Recovery Procedures

### Database Recovery

1. **Restart Database Container**
   ```bash
   docker-compose restart postgres
   ```

2. **Verify Connection**
   ```bash
   # Wait for circuit breaker recovery timeout (default 60s)
   sleep 60

   # Test query
   curl -X POST http://localhost:8001/api/v1/intent \
     -H "Content-Type: application/json" \
     -d '{"message": "list projects", "session_id": "recovery-test"}'
   ```

### Service Recovery

1. **Restart Application**
   ```bash
   docker-compose restart piper-morgan-api
   ```

2. **Verify Degradation System**
   ```bash
   # Check degradation status
   curl -s http://localhost:8001/api/v1/query-router/degradation-status | jq '.degradation_handler.state'
   ```

### Rollback Procedures

1. **Disable Degradation** (Emergency)
   ```bash
   # Set environment variable
   export ENABLE_CIRCUIT_BREAKERS=false

   # Restart service
   docker-compose restart piper-morgan-api
   ```

2. **Revert to Test Mode** (Temporary)
   ```bash
   # Enable test mode for all queries
   curl -X POST http://localhost:8001/api/v1/admin/enable-global-test-mode
   ```

## Maintenance Procedures

### Configuration Updates

1. **Update Circuit Breaker Thresholds**
   ```bash
   # Edit environment file
   vim .env

   # Update values
   QUERY_CIRCUIT_BREAKER_FAILURE_THRESHOLD=5
   QUERY_CIRCUIT_BREAKER_RECOVERY_TIMEOUT=60

   # Restart to apply changes
   docker-compose restart piper-morgan-api
   ```

2. **Verify Changes**
   ```bash
   # Check applied configuration
   curl -s http://localhost:8001/api/v1/query-router/degradation-status | jq '.degradation_handler'
   ```

### Testing in Production

1. **Controlled Degradation Test**
   ```bash
   # Enable test mode for specific session
   curl -X POST http://localhost:8001/api/v1/admin/test-degradation \
     -H "Content-Type: application/json" \
     -d '{"session_id": "ops-test-123", "service": "project_queries", "duration_seconds": 60}'
   ```

2. **Monitor Test Results**
   ```bash
   # Check test session responses
   tail -f /var/log/piper-morgan/degradation-tests.log
   ```

## Emergency Contacts

- **Primary On-Call**: Engineering Team Lead
- **Secondary**: Senior DevOps Engineer
- **Escalation**: CTO
- **Slack Channel**: #piper-morgan-incidents
- **PagerDuty**: Piper Morgan Critical Alerts

## Useful Commands Reference

```bash
# Quick health check
curl -s http://localhost:8001/api/v1/health | jq '.status'

# Circuit breaker status
curl -s http://localhost:8001/api/v1/query-router/degradation-status | jq '.degradation_handler.state'

# Recent degradation events
docker logs piper-morgan-api | grep -i degradation | tail -10

# Reset all circuit breakers
curl -X POST http://localhost:8001/api/v1/admin/reset-all-circuit-breakers

# Enable maintenance mode
curl -X POST http://localhost:8001/api/v1/admin/maintenance-mode/enable

# Disable maintenance mode
curl -X POST http://localhost:8001/api/v1/admin/maintenance-mode/disable
```
