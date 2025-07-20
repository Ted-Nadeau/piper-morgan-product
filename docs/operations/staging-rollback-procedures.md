# Staging Rollback Procedures - PM-038

**Environment**: Staging
**Version**: PM-038-staging
**Last Updated**: 2025-07-20

## Overview

This document provides comprehensive rollback procedures for the Piper Morgan staging environment, including specific procedures for PM-038 MCP integration features.

## Quick Rollback Commands

### Emergency Rollback (30 seconds)
```bash
# Stop all staging services immediately
docker-compose -f docker-compose.staging.yml down

# Restore previous version (if tagged)
docker-compose -f docker-compose.staging.yml pull
docker-compose -f docker-compose.staging.yml up -d
```

### Safe Rollback with Data Preservation (2-5 minutes)
```bash
# Execute the rollback script
./scripts/rollback_staging.sh --preserve-data --version=previous
```

## Rollback Scenarios

### 1. Application-Level Rollback

**Trigger Conditions:**
- Health checks failing for >5 minutes
- Critical API endpoints returning 5xx errors
- MCP integration completely non-functional
- Performance degradation >50%

**Steps:**
```bash
# 1. Identify target rollback version
docker images | grep piper-api

# 2. Stop current application services
docker-compose -f docker-compose.staging.yml stop api-staging web-staging

# 3. Tag current version for potential recovery
docker tag piper-api:staging piper-api:rollback-$(date +%Y%m%d-%H%M%S)

# 4. Deploy previous version
docker tag piper-api:previous piper-api:staging
docker-compose -f docker-compose.staging.yml up -d api-staging web-staging

# 5. Verify rollback
curl -f http://localhost:8001/health/comprehensive
```

### 2. Database Rollback

**Trigger Conditions:**
- Migration failures
- Data corruption
- Schema incompatibility

**Steps:**
```bash
# 1. Stop all services
docker-compose -f docker-compose.staging.yml down

# 2. Restore database from backup
docker run --rm -v piper_postgres_staging_data:/var/lib/postgresql/data \
  -v $(pwd)/backups:/backups postgres:15 \
  sh -c "rm -rf /var/lib/postgresql/data/* && \
         tar -xzf /backups/staging_db_backup_$(date +%Y%m%d).tar.gz -C /"

# 3. Start database service
docker-compose -f docker-compose.staging.yml up -d postgres-staging

# 4. Wait for database to be ready
until docker-compose -f docker-compose.staging.yml exec postgres-staging \
  pg_isready -U piper -d piper_morgan_staging; do sleep 2; done

# 5. Start remaining services
docker-compose -f docker-compose.staging.yml up -d
```

### 3. MCP Integration Rollback (PM-038 Specific)

**Trigger Conditions:**
- MCP health checks failing
- Connection pool errors
- Content search performance >500ms
- Circuit breaker permanently open

**Steps:**
```bash
# 1. Disable MCP features immediately
echo "ENABLE_MCP_FILE_SEARCH=false" >> .env.staging
echo "USE_MCP_POOL=false" >> .env.staging

# 2. Restart API service with MCP disabled
docker-compose -f docker-compose.staging.yml restart api-staging

# 3. Verify basic functionality without MCP
curl -f http://localhost:8001/health

# 4. If stable, investigate MCP issues
# 5. If unstable, proceed with full application rollback
```

### 4. Infrastructure Rollback

**Trigger Conditions:**
- Multiple service failures
- Network connectivity issues
- Resource exhaustion
- Security breaches

**Steps:**
```bash
# 1. Complete environment shutdown
docker-compose -f docker-compose.staging.yml down --volumes

# 2. Clean up networks and orphaned containers
docker network prune -f
docker container prune -f

# 3. Restore from infrastructure backup
./scripts/restore_staging_infrastructure.sh

# 4. Deploy previous known-good configuration
git checkout previous-stable-tag
./scripts/deploy_staging.sh
```

## Rollback Decision Matrix

| Issue Type | Severity | Time to Rollback | Rollback Type | Data Preservation |
|------------|----------|------------------|---------------|-------------------|
| API Errors | High | <30 seconds | Application | Yes |
| MCP Failures | Medium | <60 seconds | Feature Disable | Yes |
| DB Issues | High | <5 minutes | Database | Depends |
| Performance | Medium | <2 minutes | Application | Yes |
| Security | Critical | <10 seconds | Infrastructure | No |

## Automated Rollback Scripts

### Create Rollback Script
```bash
# scripts/rollback_staging.sh
#!/bin/bash
set -euo pipefail

# Parse command line options
PRESERVE_DATA=false
TARGET_VERSION=""
ROLLBACK_TYPE="application"

while [[ $# -gt 0 ]]; do
  case $1 in
    --preserve-data)
      PRESERVE_DATA=true
      shift
      ;;
    --version=*)
      TARGET_VERSION="${1#*=}"
      shift
      ;;
    --type=*)
      ROLLBACK_TYPE="${1#*=}"
      shift
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# Validate rollback conditions
validate_rollback() {
    log "Validating rollback conditions..."

    # Check if services are actually unhealthy
    if curl -sf http://localhost:8001/health > /dev/null 2>&1; then
        read -p "Services appear healthy. Continue with rollback? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log "Rollback cancelled by user"
            exit 0
        fi
    fi

    # Check for ongoing operations
    if docker-compose -f docker-compose.staging.yml ps | grep -q "restarting"; then
        log "WARNING: Services are currently restarting. This may interfere with rollback."
        sleep 5
    fi
}

# Perform application rollback
rollback_application() {
    log "Performing application rollback..."

    # Create snapshot of current state
    if [[ "$PRESERVE_DATA" == "true" ]]; then
        log "Creating data snapshot before rollback..."
        docker-compose -f docker-compose.staging.yml exec postgres-staging \
          pg_dump -U piper piper_morgan_staging > \
          "backups/pre_rollback_$(date +%Y%m%d_%H%M%S).sql"
    fi

    # Stop application services
    log "Stopping application services..."
    docker-compose -f docker-compose.staging.yml stop api-staging web-staging

    # Tag current version for potential recovery
    docker tag piper-api:staging piper-api:rollback-$(date +%Y%m%d-%H%M%S)
    docker tag piper-web:staging piper-web:rollback-$(date +%Y%m%d-%H%M%S)

    # Deploy target version
    if [[ -n "$TARGET_VERSION" ]]; then
        log "Deploying version: $TARGET_VERSION"
        docker tag piper-api:$TARGET_VERSION piper-api:staging
        docker tag piper-web:$TARGET_VERSION piper-web:staging
    else
        log "Deploying previous version"
        docker tag piper-api:previous piper-api:staging
        docker tag piper-web:previous piper-web:staging
    fi

    # Start services
    log "Starting rolled-back services..."
    docker-compose -f docker-compose.staging.yml up -d api-staging web-staging

    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30

    # Verify rollback
    local max_attempts=10
    local attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        if curl -sf http://localhost:8001/health > /dev/null 2>&1; then
            log "Rollback verification successful"
            return 0
        fi
        sleep 10
        ((attempt++))
    done

    log "ERROR: Rollback verification failed"
    return 1
}

# Perform MCP-specific rollback
rollback_mcp() {
    log "Performing MCP-specific rollback..."

    # Disable MCP features
    log "Disabling MCP features..."
    sed -i.bak 's/ENABLE_MCP_FILE_SEARCH=true/ENABLE_MCP_FILE_SEARCH=false/' .env.staging
    sed -i.bak 's/USE_MCP_POOL=true/USE_MCP_POOL=false/' .env.staging

    # Restart API with MCP disabled
    docker-compose -f docker-compose.staging.yml restart api-staging

    # Verify basic functionality
    sleep 15
    if curl -sf http://localhost:8001/health > /dev/null 2>&1; then
        log "MCP rollback successful - basic functionality restored"
        log "NOTE: MCP features are now disabled. Investigate and re-enable when ready."
        return 0
    else
        log "ERROR: MCP rollback failed - proceeding with full application rollback"
        rollback_application
    fi
}

# Main rollback execution
main() {
    log "Starting staging environment rollback..."
    log "Type: $ROLLBACK_TYPE"
    log "Preserve data: $PRESERVE_DATA"
    log "Target version: ${TARGET_VERSION:-previous}"

    validate_rollback

    case $ROLLBACK_TYPE in
        application)
            rollback_application
            ;;
        mcp)
            rollback_mcp
            ;;
        infrastructure)
            log "Infrastructure rollback requires manual intervention"
            exit 1
            ;;
        *)
            log "Unknown rollback type: $ROLLBACK_TYPE"
            exit 1
            ;;
    esac

    log "Rollback completed successfully"
    log "Services status:"
    docker-compose -f docker-compose.staging.yml ps
}

main "$@"
```

## Post-Rollback Verification

### 1. Health Checks
```bash
# Basic health
curl -f http://localhost:8001/health

# Comprehensive health
curl -s http://localhost:8001/health/comprehensive | jq '.overall_status'

# MCP health (if enabled)
curl -s http://localhost:8001/health/mcp | jq '.status'
```

### 2. Functional Tests
```bash
# Test API endpoints
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "test rollback", "session_id": "rollback-test"}'

# Test file search (if MCP enabled)
curl -X GET "http://localhost:8001/api/v1/files/search?q=test&session_id=rollback-test"
```

### 3. Performance Validation
```bash
# Check response times
curl -w "@curl-format.txt" -s -o /dev/null http://localhost:8001/health

# Monitor system resources
docker stats --no-stream
```

## Recovery from Failed Rollback

### If Rollback Fails
```bash
# 1. Stop all services
docker-compose -f docker-compose.staging.yml down --remove-orphans

# 2. Restore from last known good backup
./scripts/restore_staging_from_backup.sh --date=$(date -d "yesterday" +%Y%m%d)

# 3. Deploy last stable version
git checkout last-stable-tag
./scripts/deploy_staging.sh

# 4. Notify team and document incident
```

### Emergency Contacts
- **Primary**: Engineering Team Lead
- **Secondary**: DevOps Engineer
- **Escalation**: CTO

## Incident Documentation

### Rollback Incident Report Template
```markdown
# Rollback Incident Report

**Date**: YYYY-MM-DD HH:MM UTC
**Environment**: Staging
**Rollback Trigger**: [Description]
**Rollback Type**: [Application/MCP/Infrastructure]
**Duration**: [X minutes]
**Data Loss**: [Yes/No - Details]

## Timeline
- HH:MM - Issue detected
- HH:MM - Rollback initiated
- HH:MM - Rollback completed
- HH:MM - Verification completed

## Root Cause
[Detailed analysis]

## Resolution
[Steps taken]

## Prevention
[Action items to prevent recurrence]

## Lessons Learned
[Key takeaways]
```

## Backup and Recovery Integration

### Pre-Rollback Backups
All rollback procedures automatically create:
- Database dump with timestamp
- Configuration file backup
- Docker image tags for recovery
- Application logs archive

### Backup Retention Policy
- **Hourly snapshots**: Kept for 24 hours
- **Daily backups**: Kept for 7 days
- **Weekly backups**: Kept for 4 weeks
- **Monthly backups**: Kept for 12 months

## Testing Rollback Procedures

### Monthly Rollback Drills
```bash
# Simulate rollback scenario
./scripts/test_rollback_procedures.sh --dry-run

# Execute actual rollback test
./scripts/test_rollback_procedures.sh --execute --environment=test
```

### Rollback Performance Metrics
- **Target Time to Rollback**: <5 minutes
- **Data Preservation Rate**: 100%
- **Success Rate**: >99%
- **Recovery Time Objective (RTO)**: <10 minutes
- **Recovery Point Objective (RPO)**: <15 minutes

## Integration with Monitoring

### Automated Rollback Triggers
The monitoring system can automatically initiate rollbacks when:
- Health check failures exceed threshold (5 consecutive failures)
- Response time >10 seconds for >2 minutes
- Error rate >50% for >1 minute
- MCP performance >1000ms for >5 minutes

### Rollback Notifications
- Slack alerts to #engineering-alerts
- Email notifications to on-call team
- PagerDuty escalation for failed rollbacks
- Dashboard status updates

---

**Note**: This document should be reviewed and updated after each rollback incident to improve procedures and capture lessons learned.

**Version**: 1.0
**Next Review**: 2025-08-20
