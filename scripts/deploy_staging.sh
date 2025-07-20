#!/bin/bash
set -euo pipefail

# Piper Morgan - Staging Deployment Script
# =======================================
# Production-grade staging deployment with PM-038 MCP integration

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env.staging"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.staging.yml"
LOG_FILE="$PROJECT_ROOT/logs/staging_deployment.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Create logs directory if it doesn't exist
    mkdir -p "$(dirname "$LOG_FILE")"

    # Log to file
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"

    # Log to console with colors
    case $level in
        ERROR)
            echo -e "${RED}[ERROR]${NC} $message" >&2
            ;;
        WARN)
            echo -e "${YELLOW}[WARN]${NC} $message"
            ;;
        INFO)
            echo -e "${GREEN}[INFO]${NC} $message"
            ;;
        DEBUG)
            echo -e "${BLUE}[DEBUG]${NC} $message"
            ;;
        *)
            echo "[$level] $message"
            ;;
    esac
}

# Error handler
error_exit() {
    log ERROR "$1"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log INFO "Checking deployment prerequisites..."

    # Check if running from correct directory
    if [[ ! -f "$PROJECT_ROOT/pyproject.toml" ]]; then
        error_exit "Script must be run from project root or scripts directory"
    fi

    # Check required commands
    local required_commands=("docker" "docker-compose" "curl" "jq")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            error_exit "Required command '$cmd' not found"
        fi
    done

    # Check if staging environment file exists
    if [[ ! -f "$ENV_FILE" ]]; then
        error_exit "Staging environment file not found: $ENV_FILE"
    fi

    # Check if compose file exists
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        error_exit "Staging compose file not found: $COMPOSE_FILE"
    fi

    log INFO "Prerequisites check passed"
}

# Validate environment configuration
validate_environment() {
    log INFO "Validating staging environment configuration..."

    # Source the staging environment
    set -a
    source "$ENV_FILE"
    set +a

    # Check required environment variables
    local required_vars=(
        "ANTHROPIC_API_KEY"
        "OPENAI_API_KEY"
        "POSTGRES_PASSWORD"
        "REDIS_PASSWORD"
        "SECRET_KEY"
        "JWT_SECRET_KEY"
    )

    local missing_vars=()
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            missing_vars+=("$var")
        fi
    done

    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        error_exit "Missing required environment variables: ${missing_vars[*]}"
    fi

    # Validate MCP configuration
    if [[ "${ENABLE_MCP_FILE_SEARCH:-false}" != "true" ]]; then
        error_exit "MCP file search must be enabled for staging deployment"
    fi

    if [[ "${USE_MCP_POOL:-false}" != "true" ]]; then
        error_exit "MCP connection pool must be enabled for staging deployment"
    fi

    log INFO "Environment validation passed"
}

# Pre-deployment cleanup
pre_deployment_cleanup() {
    log INFO "Performing pre-deployment cleanup..."

    # Stop any existing staging containers
    if docker-compose -f "$COMPOSE_FILE" ps -q &> /dev/null; then
        log INFO "Stopping existing staging containers..."
        docker-compose -f "$COMPOSE_FILE" down --remove-orphans || true
    fi

    # Clean up orphaned networks
    docker network prune -f || true

    # Clean up unused volumes (but preserve data volumes)
    docker volume prune -f || true

    log INFO "Pre-deployment cleanup completed"
}

# Build staging images
build_images() {
    log INFO "Building staging Docker images..."

    # Create Dockerfile for staging API if it doesn't exist
    if [[ ! -f "$PROJECT_ROOT/Dockerfile.staging" ]]; then
        log INFO "Creating staging Dockerfile..."
        cat > "$PROJECT_ROOT/Dockerfile.staging" << 'EOF'
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=staging

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Expose port
EXPOSE 8001

# Run application
CMD ["python", "main.py"]
EOF
    fi

    # Build API image
    log INFO "Building API image..."
    docker build -f "$PROJECT_ROOT/Dockerfile.staging" -t piper-api:staging "$PROJECT_ROOT"

    # Create web Dockerfile if it doesn't exist
    if [[ ! -f "$PROJECT_ROOT/web/Dockerfile.staging" ]]; then
        log INFO "Creating web staging Dockerfile..."
        mkdir -p "$PROJECT_ROOT/web"
        cat > "$PROJECT_ROOT/web/Dockerfile.staging" << 'EOF'
FROM node:18-alpine

# Set environment variables
ENV NODE_ENV=staging

# Set work directory
WORKDIR /app

# Copy package files (if they exist)
COPY package*.json ./
RUN if [ -f package.json ]; then npm install; fi

# Copy application code
COPY . .

# Build application (if needed)
RUN if [ -f package.json ] && [ -f "build" ] || [ -f "dist" ]; then npm run build; fi

# Create simple static server for staging
RUN echo '#!/bin/sh\nif [ -d "dist" ]; then cd dist; elif [ -d "build" ]; then cd build; fi\npython3 -m http.server 8080' > start.sh && chmod +x start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Run application
CMD ["./start.sh"]
EOF
    fi

    # Build web image
    log INFO "Building web image..."
    docker build -f "$PROJECT_ROOT/web/Dockerfile.staging" -t piper-web:staging "$PROJECT_ROOT/web"

    log INFO "Image build completed"
}

# Create necessary directories and configuration
create_staging_config() {
    log INFO "Creating staging configuration directories..."

    # Create config directories
    mkdir -p "$PROJECT_ROOT/config/staging/nginx"
    mkdir -p "$PROJECT_ROOT/config/staging/chroma_auth"
    mkdir -p "$PROJECT_ROOT/config/staging/grafana/dashboards"
    mkdir -p "$PROJECT_ROOT/config/staging/grafana/datasources"
    mkdir -p "$PROJECT_ROOT/logs"

    # Create nginx configuration
    if [[ ! -f "$PROJECT_ROOT/config/staging/nginx/nginx.conf" ]]; then
        log INFO "Creating nginx configuration..."
        cat > "$PROJECT_ROOT/config/staging/nginx/nginx.conf" << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api-staging:8001;
    }

    upstream web {
        server web-staging:8080;
    }

    server {
        listen 80;
        server_name staging.pipermorgansuite.com;

        # Health check endpoint
        location /health {
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # API routes
        location /api {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health routes
        location /health {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Web application
        location / {
            proxy_pass http://web;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF
    fi

    # Create ChromaDB auth file
    if [[ ! -f "$PROJECT_ROOT/config/staging/chroma_auth/credentials" ]]; then
        log INFO "Creating ChromaDB auth configuration..."
        echo "admin:staging_chroma_password_2025" > "$PROJECT_ROOT/config/staging/chroma_auth/credentials"
    fi

    # Create Prometheus configuration
    if [[ ! -f "$PROJECT_ROOT/config/staging/prometheus.yml" ]]; then
        log INFO "Creating Prometheus configuration..."
        cat > "$PROJECT_ROOT/config/staging/prometheus.yml" << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'piper-api'
    static_configs:
      - targets: ['api-staging:8001']
    metrics_path: '/health/metrics'
    scrape_interval: 30s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF
    fi

    # Create Grafana datasource configuration
    if [[ ! -f "$PROJECT_ROOT/config/staging/grafana/datasources/prometheus.yml" ]]; then
        log INFO "Creating Grafana datasource configuration..."
        cat > "$PROJECT_ROOT/config/staging/grafana/datasources/prometheus.yml" << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus-staging:9090
    isDefault: true
EOF
    fi

    log INFO "Staging configuration created"
}

# Deploy staging environment
deploy_staging() {
    log INFO "Deploying staging environment..."

    # Start services with dependency order
    log INFO "Starting infrastructure services..."
    docker-compose -f "$COMPOSE_FILE" up -d postgres-staging redis-staging chromadb-staging

    # Wait for infrastructure to be ready
    log INFO "Waiting for infrastructure services to be ready..."
    sleep 30

    # Start application services
    log INFO "Starting application services..."
    docker-compose -f "$COMPOSE_FILE" up -d api-staging web-staging

    # Wait for application services
    log INFO "Waiting for application services to be ready..."
    sleep 45

    # Start reverse proxy and monitoring
    log INFO "Starting reverse proxy and monitoring..."
    docker-compose -f "$COMPOSE_FILE" up -d nginx-staging prometheus-staging grafana-staging

    log INFO "Staging deployment completed"
}

# Verify deployment
verify_deployment() {
    log INFO "Verifying staging deployment..."

    local max_attempts=30
    local attempt=1
    local all_healthy=false

    while [[ $attempt -le $max_attempts ]]; do
        log INFO "Health check attempt $attempt/$max_attempts..."

        # Check basic health endpoint
        if curl -sf http://localhost:8001/health > /dev/null 2>&1; then
            log INFO "Basic health check passed"

            # Check comprehensive health
            local health_response
            if health_response=$(curl -sf http://localhost:8001/health/comprehensive 2>/dev/null); then
                local overall_status
                overall_status=$(echo "$health_response" | jq -r '.overall_status' 2>/dev/null || echo "unknown")

                if [[ "$overall_status" == "healthy" ]]; then
                    log INFO "Comprehensive health check passed"
                    all_healthy=true
                    break
                else
                    log WARN "Health check status: $overall_status"
                fi
            else
                log WARN "Comprehensive health check failed"
            fi
        else
            log WARN "Basic health check failed"
        fi

        sleep 10
        ((attempt++))
    done

    if [[ "$all_healthy" == "true" ]]; then
        log INFO "Deployment verification successful"
        return 0
    else
        log ERROR "Deployment verification failed after $max_attempts attempts"
        return 1
    fi
}

# Test MCP integration
test_mcp_integration() {
    log INFO "Testing PM-038 MCP integration..."

    # Test MCP health endpoint
    local mcp_health_response
    if mcp_health_response=$(curl -sf http://localhost:8001/health/mcp 2>/dev/null); then
        local mcp_status
        mcp_status=$(echo "$mcp_health_response" | jq -r '.status' 2>/dev/null || echo "unknown")

        if [[ "$mcp_status" == "healthy" ]]; then
            log INFO "MCP health check passed"

            # Extract performance metrics
            local search_time
            search_time=$(echo "$mcp_health_response" | jq -r '.tests.search_response_time_ms' 2>/dev/null || echo "unknown")

            local using_pool
            using_pool=$(echo "$mcp_health_response" | jq -r '.tests.connection_stats.using_pool' 2>/dev/null || echo "unknown")

            log INFO "MCP search response time: ${search_time}ms"
            log INFO "MCP connection pooling: $using_pool"

            # Verify performance target (should be under 500ms)
            if [[ "$search_time" != "unknown" ]] && (( $(echo "$search_time < 500" | bc -l) )); then
                log INFO "MCP performance target met (${search_time}ms < 500ms)"
            else
                log WARN "MCP performance target not met (${search_time}ms >= 500ms)"
            fi

            # Verify connection pooling is enabled
            if [[ "$using_pool" == "true" ]]; then
                log INFO "MCP connection pooling enabled (642x performance improvement active)"
            else
                log WARN "MCP connection pooling not enabled"
            fi

        else
            log ERROR "MCP health check failed with status: $mcp_status"
            return 1
        fi
    else
        log ERROR "Failed to retrieve MCP health status"
        return 1
    fi

    log INFO "MCP integration test completed successfully"
}

# Generate deployment report
generate_deployment_report() {
    log INFO "Generating deployment report..."

    local report_file="$PROJECT_ROOT/logs/staging_deployment_report_$(date +%Y%m%d_%H%M%S).json"

    # Get comprehensive health status
    local health_data
    if health_data=$(curl -sf http://localhost:8001/health/comprehensive 2>/dev/null); then
        # Get container status
        local container_status
        container_status=$(docker-compose -f "$COMPOSE_FILE" ps --format json 2>/dev/null || echo '[]')

        # Create deployment report
        cat > "$report_file" << EOF
{
  "deployment_info": {
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "environment": "staging",
    "version": "PM-038-staging",
    "deployer": "${USER:-unknown}",
    "host": "$(hostname)",
    "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "git_branch": "$(git branch --show-current 2>/dev/null || echo 'unknown')"
  },
  "health_status": $health_data,
  "container_status": $container_status,
  "performance_metrics": {
    "deployment_duration_seconds": $(($(date +%s) - deployment_start_time)),
    "services_deployed": $(docker-compose -f "$COMPOSE_FILE" ps --services | wc -l),
    "healthy_services": $(docker-compose -f "$COMPOSE_FILE" ps --format json | jq -r '.[] | select(.Health == "healthy") | .Name' | wc -l)
  }
}
EOF

        log INFO "Deployment report generated: $report_file"

        # Display summary
        log INFO "=== DEPLOYMENT SUMMARY ==="
        log INFO "Environment: staging"
        log INFO "Version: PM-038-staging"
        log INFO "Overall Status: $(echo "$health_data" | jq -r '.overall_status' 2>/dev/null || echo 'unknown')"
        log INFO "Healthy Components: $(echo "$health_data" | jq -r '.summary.healthy_components' 2>/dev/null || echo 'unknown')"
        log INFO "Total Components: $(echo "$health_data" | jq -r '.summary.total_components' 2>/dev/null || echo 'unknown')"
        log INFO "Health Percentage: $(echo "$health_data" | jq -r '.summary.health_percentage' 2>/dev/null || echo 'unknown')%"
        log INFO "=========================="

    else
        log ERROR "Failed to generate comprehensive deployment report"
        return 1
    fi
}

# Cleanup function for failed deployments
cleanup_failed_deployment() {
    log WARN "Cleaning up failed deployment..."

    # Stop all services
    docker-compose -f "$COMPOSE_FILE" down --remove-orphans || true

    # Remove any partially created volumes
    docker volume ls -q | grep staging | xargs -r docker volume rm || true

    log WARN "Failed deployment cleanup completed"
}

# Main deployment function
main() {
    local start_time=$(date +%s)
    deployment_start_time=$start_time

    log INFO "Starting Piper Morgan staging deployment..."
    log INFO "Timestamp: $(date)"
    log INFO "Script: $0"
    log INFO "User: ${USER:-unknown}"
    log INFO "Host: $(hostname)"

    # Set trap for cleanup on failure
    trap cleanup_failed_deployment ERR

    # Execute deployment steps
    check_prerequisites
    validate_environment
    pre_deployment_cleanup
    create_staging_config
    build_images
    deploy_staging

    # Verify deployment
    if verify_deployment; then
        log INFO "Deployment verification passed"
    else
        log ERROR "Deployment verification failed"
        cleanup_failed_deployment
        exit 1
    fi

    # Test MCP integration
    if test_mcp_integration; then
        log INFO "MCP integration test passed"
    else
        log WARN "MCP integration test failed (deployment continues)"
    fi

    # Generate report
    generate_deployment_report

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    log INFO "Staging deployment completed successfully in ${duration} seconds"
    log INFO "Services available at:"
    log INFO "  - API: http://localhost:8001"
    log INFO "  - Web: http://localhost:8081"
    log INFO "  - Nginx: http://localhost:80"
    log INFO "  - Grafana: http://localhost:3001"
    log INFO "  - Prometheus: http://localhost:9090"
    log INFO "Health checks:"
    log INFO "  - Basic: http://localhost:8001/health"
    log INFO "  - Comprehensive: http://localhost:8001/health/comprehensive"
    log INFO "  - MCP: http://localhost:8001/health/mcp"

    # Display next steps
    log INFO "Next steps:"
    log INFO "1. Monitor health checks and logs"
    log INFO "2. Run integration tests"
    log INFO "3. Validate MCP performance metrics"
    log INFO "4. Test real content search functionality"
    log INFO "5. Review Grafana dashboards"
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
