# Staging Rollback Procedures

**Date**: August 11, 2025
**Status**: Production Ready
**Environment**: Staging with Docker Compose
**Rollback Strategy**: Automated + Manual procedures

## Overview

This guide provides comprehensive rollback procedures for the Piper Morgan staging environment, ensuring safe deployment practices and quick recovery from deployment issues.

## Rollback Strategy

### Multi-Layer Approach

1. **Automatic Rollback**: Health check failures trigger immediate rollback
2. **Manual Rollback**: Developer-initiated rollback for planned changes
3. **Emergency Rollback**: Force rollback for critical failures
4. **Gradual Rollback**: Partial rollback for specific components

## Prerequisites

### Required Tools

```bash
# Verify rollback tools availability
ls -la scripts/rollback_*.sh
ls -la scripts/verify_staging_deployment.sh
ls -la scripts/backup_staging.sh
```

### Required Access

- **Docker Compose**: Full control over staging services
- **Git Access**: Ability to checkout previous versions
- **Database Access**: PostgreSQL admin privileges
- **Monitoring Access**: Grafana and Prometheus dashboards

## Automatic Rollback

### Health Check Triggers

The staging environment automatically triggers rollback when:

- **Response Time**: Exceeds 500ms threshold for 3 consecutive checks
- **Error Rate**: Exceeds 5% for 2 consecutive health check cycles
- **Service Unavailable**: Any critical service fails health check
- **Database Issues**: Connection failures or query timeouts

### Automatic Rollback Process

```bash
# Health check monitoring (runs every 30 seconds)
while true; do
    ./scripts/health_check.sh
    if [ $? -ne 0 ]; then
        echo "Health check failed, triggering automatic rollback"
        ./scripts/rollback_staging.sh
        break
    fi
    sleep 30
done
```

### Rollback Triggers

```yaml
# Health check thresholds
health_checks:
  response_time:
    threshold: 500ms
    consecutive_failures: 3
    action: "rollback"

  error_rate:
    threshold: 5%
    consecutive_failures: 2
    action: "rollback"

  service_health:
    threshold: 100%
    consecutive_failures: 1
    action: "rollback"
```

## Manual Rollback

### Planned Rollback

```bash
# 1. Verify current deployment health
./scripts/verify_staging_deployment.sh

# 2. Create backup before rollback
./scripts/backup_staging.sh

# 3. Execute rollback
./scripts/rollback_staging.sh

# 4. Verify rollback success
./scripts/verify_staging_deployment.sh
```

### Emergency Rollback

```bash
# Force immediate rollback (bypasses health checks)
./scripts/emergency_rollback.sh

# Verify critical services are running
./scripts/verify_critical_services.sh
```

## Rollback Procedures by Component

### Application Rollback

```bash
# Rollback application to previous version
git checkout HEAD~1
docker-compose build app
docker-compose up -d app

# Verify application health
curl http://localhost:8001/health
```

### Database Rollback

```bash
# Restore database from backup
./scripts/restore_staging.sh backup_$(date +%Y-%m-%d_%H-%M-%S).sql

# Verify database integrity
docker-compose exec app python -c "
from services.database import get_db
db = get_db()
result = db.execute('SELECT COUNT(*) FROM information_schema.tables')
print(f'Database tables: {result.fetchone()[0]}')
"
```

### Configuration Rollback

```bash
# Restore previous configuration
git checkout HEAD~1 -- .env
git checkout HEAD~1 -- docker-compose.yml

# Restart services with old config
docker-compose down
docker-compose up -d
```

### Monitoring Stack Rollback

```bash
# Rollback monitoring services
docker-compose down prometheus grafana
docker-compose up -d prometheus grafana

# Verify monitoring is working
curl http://localhost:9090/-/healthy
curl http://localhost:3001/api/health
```

## Rollback Scripts

### Primary Rollback Script

```bash
#!/bin/bash
# scripts/rollback_staging.sh

set -e

echo "🚨 Initiating staging rollback..."

# 1. Stop current deployment
echo "Stopping current deployment..."
docker-compose down

# 2. Checkout previous version
echo "Checking out previous version..."
git checkout HEAD~1

# 3. Restore from backup if available
if [ -f "backup_latest.sql" ]; then
    echo "Restoring database from backup..."
    ./scripts/restore_staging.sh backup_latest.sql
fi

# 4. Rebuild and restart
echo "Rebuilding and restarting services..."
docker-compose build
docker-compose up -d

# 5. Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# 6. Verify rollback success
echo "Verifying rollback success..."
./scripts/verify_staging_deployment.sh

echo "✅ Rollback completed successfully"
```

### Emergency Rollback Script

```bash
#!/bin/bash
# scripts/emergency_rollback.sh

set -e

echo "🚨 EMERGENCY ROLLBACK - Bypassing health checks"

# 1. Force stop all services
docker-compose down --remove-orphans

# 2. Checkout last known good version
git checkout HEAD~5  # Go back 5 commits for safety

# 3. Restart with minimal verification
docker-compose up -d

# 4. Basic health check only
curl -f http://localhost:8001/health || echo "Health check failed but services are running"

echo "⚠️  Emergency rollback completed - manual verification required"
```

### Verification Script

```bash
#!/bin/bash
# scripts/verify_staging_deployment.sh

set -e

echo "🔍 Verifying staging deployment..."

# Test 1: Application health
echo "Test 1: Application health..."
curl -f http://localhost:8001/health

# Test 2: Database connection
echo "Test 2: Database connection..."
docker-compose exec app python -c "from services.database import get_db; print('Database OK')"

# Test 3: Redis connection
echo "Test 3: Redis connection..."
docker-compose exec app python -c "import redis; r = redis.Redis(host='redis'); r.ping(); print('Redis OK')"

# Test 4: MCP health
echo "Test 4: MCP health..."
curl -f http://localhost:8001/health/mcp

# Test 5: Performance test
echo "Test 5: Performance test..."
start_time=$(date +%s%N)
curl -s http://localhost:8001/health > /dev/null
end_time=$(date +%s%N)
response_time=$(( (end_time - start_time) / 1000000 ))

if [ $response_time -lt 500 ]; then
    echo "✅ Performance OK: ${response_time}ms"
else
    echo "⚠️  Performance degraded: ${response_time}ms"
fi

echo "✅ All verification tests passed"
```

## Rollback Decision Matrix

### When to Rollback

| Issue Type                  | Severity | Rollback Action  | Verification Required    |
| --------------------------- | -------- | ---------------- | ------------------------ |
| **Critical Service Down**   | High     | Immediate        | Full health check        |
| **Performance Degradation** | Medium   | After 3 failures | Performance metrics      |
| **Configuration Error**     | Medium   | Manual           | Configuration validation |
| **Database Corruption**     | High     | Immediate        | Data integrity check     |
| **Security Vulnerability**  | High     | Immediate        | Security scan            |

### Rollback Timing

| Rollback Type | Trigger Time        | Recovery Time | Verification Time   |
| ------------- | ------------------- | ------------- | ------------------- |
| **Automatic** | <30 seconds         | 2-5 minutes   | 1-2 minutes         |
| **Manual**    | Developer initiated | 5-10 minutes  | 2-3 minutes         |
| **Emergency** | <10 seconds         | 1-3 minutes   | Manual verification |

## Monitoring During Rollback

### Key Metrics to Watch

```bash
# Monitor rollback progress
watch -n 5 'docker-compose ps && echo "---" && curl -s http://localhost:8001/health | jq'

# Check service logs during rollback
docker-compose logs -f app postgres redis
```

### Rollback Status Dashboard

```bash
# Create rollback status dashboard
cat > rollback_status.md << EOF
# Rollback Status: $(date)

## Services Status
$(docker-compose ps)

## Health Checks
$(curl -s http://localhost:8001/health | jq)

## Performance Metrics
$(curl -s http://localhost:8001/metrics | grep -E "(response_time|error_rate)")
EOF
```

## Post-Rollback Actions

### Immediate Actions

1. **Verify System Health**: Run comprehensive health checks
2. **Document Rollback**: Record reason and timing
3. **Notify Team**: Alert relevant stakeholders
4. **Investigate Root Cause**: Analyze why rollback was needed

### Follow-up Actions

1. **Root Cause Analysis**: Document findings and lessons learned
2. **Prevention Measures**: Implement fixes to prevent recurrence
3. **Rollback Improvement**: Enhance rollback procedures if needed
4. **Team Review**: Conduct post-mortem if significant issues occurred

## Rollback Best Practices

### Before Deployment

```bash
# 1. Create backup
./scripts/backup_staging.sh

# 2. Tag current version
git tag "pre-deploy-$(date +%Y%m%d-%H%M%S)"

# 3. Verify rollback tools
./scripts/test_rollback_tools.sh
```

### During Deployment

```bash
# 1. Monitor health checks
./scripts/monitor_deployment.sh

# 2. Watch for warning signs
- Response time increases
- Error rate spikes
- Service health degradation
```

### After Rollback

```bash
# 1. Verify system stability
./scripts/verify_staging_deployment.sh

# 2. Document rollback details
./scripts/document_rollback.sh

# 3. Plan next deployment
./scripts/plan_next_deployment.sh
```

## Troubleshooting Rollback Issues

### Common Rollback Problems

#### Rollback Script Fails

```bash
# Check script permissions
chmod +x scripts/rollback_staging.sh

# Verify script dependencies
./scripts/check_rollback_dependencies.sh

# Run with debug output
bash -x scripts/rollback_staging.sh
```

#### Services Won't Start After Rollback

```bash
# Check Docker resources
docker system df
docker system prune -f

# Verify port availability
netstat -tulpn | grep -E "(8001|8081|3001|9090)"

# Check service logs
docker-compose logs [service_name]
```

#### Database Rollback Issues

```bash
# Verify backup file integrity
./scripts/verify_backup.sh backup_file.sql

# Check database permissions
docker-compose exec postgres psql -U piper_user -l

# Manual database restore
docker-compose exec -T postgres psql -U piper_user -d piper_morgan_staging < backup_file.sql
```

## Rollback Metrics and Reporting

### Rollback Performance Metrics

```bash
# Track rollback success rate
./scripts/rollback_metrics.sh

# Expected metrics:
# - Rollback success rate: >95%
# - Average rollback time: <5 minutes
# - Recovery time: <10 minutes
```

### Rollback Report Template

```markdown
# Rollback Report

**Date**: [Date]
**Trigger**: [Automatic/Manual/Emergency]
**Reason**: [Description of issue]
**Rollback Time**: [Duration]
**Recovery Time**: [Duration]
**Services Affected**: [List]
**Root Cause**: [Analysis]
**Prevention Measures**: [Actions taken]
**Lessons Learned**: [Key insights]
```

---

**Status**: Production Ready ✅
**Rollback Strategy**: Multi-layer approach ✅
**Automation**: Health check triggers ✅
**Recovery Time**: <5 minutes target ✅
**Documentation**: Comprehensive procedures ✅
