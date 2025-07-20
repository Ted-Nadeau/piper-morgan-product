#!/bin/bash
set -euo pipefail

# Piper Morgan - Staging Deployment Verification Script
# ====================================================
# Comprehensive verification of PM-038 staging deployment

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/logs/staging_verification.log"

# Test configuration
API_BASE_URL="http://localhost:8001"
WEB_BASE_URL="http://localhost:8081"
NGINX_BASE_URL="http://localhost:80"
GRAFANA_URL="http://localhost:3001"
PROMETHEUS_URL="http://localhost:9090"

# Performance thresholds
MAX_RESPONSE_TIME_MS=500
MAX_MCP_SEARCH_TIME_MS=500
MIN_HEALTH_PERCENTAGE=90

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
WARNINGS=0

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
        PASS)
            echo -e "${GREEN}[PASS]${NC} $message"
            ;;
        FAIL)
            echo -e "${RED}[FAIL]${NC} $message"
            ;;
        *)
            echo "[$level] $message"
            ;;
    esac
}

# Test tracking functions
start_test() {
    local test_name="$1"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    log INFO "Starting test: $test_name"
}

pass_test() {
    local test_name="$1"
    PASSED_TESTS=$((PASSED_TESTS + 1))
    log PASS "$test_name"
}

fail_test() {
    local test_name="$1"
    local reason="$2"
    FAILED_TESTS=$((FAILED_TESTS + 1))
    log FAIL "$test_name - $reason"
}

warn_test() {
    local test_name="$1"
    local reason="$2"
    WARNINGS=$((WARNINGS + 1))
    log WARN "$test_name - $reason"
}

# Utility functions
make_request() {
    local url="$1"
    local method="${2:-GET}"
    local data="${3:-}"
    local timeout="${4:-10}"

    if [[ "$method" == "POST" && -n "$data" ]]; then
        curl -sf --max-time "$timeout" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" "$url" 2>/dev/null
    else
        curl -sf --max-time "$timeout" -X "$method" "$url" 2>/dev/null
    fi
}

measure_response_time() {
    local url="$1"
    local method="${2:-GET}"
    local data="${3:-}"

    local start_time=$(date +%s%N)

    if [[ "$method" == "POST" && -n "$data" ]]; then
        curl -sf --max-time 30 -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" "$url" > /dev/null 2>&1
    else
        curl -sf --max-time 30 -X "$method" "$url" > /dev/null 2>&1
    fi

    local end_time=$(date +%s%N)
    local duration_ns=$((end_time - start_time))
    local duration_ms=$((duration_ns / 1000000))

    echo "$duration_ms"
}

# Test functions
test_basic_connectivity() {
    start_test "Basic Connectivity"

    local endpoints=(
        "$API_BASE_URL/health"
        "$WEB_BASE_URL"
        "$NGINX_BASE_URL/health"
        "$GRAFANA_URL/api/health"
        "$PROMETHEUS_URL/-/healthy"
    )

    local failed_endpoints=()

    for endpoint in "${endpoints[@]}"; do
        if ! make_request "$endpoint" GET "" 5; then
            failed_endpoints+=("$endpoint")
        fi
    done

    if [[ ${#failed_endpoints[@]} -eq 0 ]]; then
        pass_test "Basic Connectivity"
    else
        fail_test "Basic Connectivity" "Failed endpoints: ${failed_endpoints[*]}"
    fi
}

test_health_endpoints() {
    start_test "Health Endpoints"

    # Test basic health
    if ! make_request "$API_BASE_URL/health" > /dev/null; then
        fail_test "Health Endpoints" "Basic health endpoint failed"
        return 1
    fi

    # Test liveness probe
    if ! make_request "$API_BASE_URL/health/liveness" > /dev/null; then
        fail_test "Health Endpoints" "Liveness probe failed"
        return 1
    fi

    # Test readiness probe
    if ! make_request "$API_BASE_URL/health/readiness" > /dev/null; then
        fail_test "Health Endpoints" "Readiness probe failed"
        return 1
    fi

    # Test comprehensive health
    local health_response
    if health_response=$(make_request "$API_BASE_URL/health/comprehensive"); then
        local overall_status
        overall_status=$(echo "$health_response" | jq -r '.overall_status' 2>/dev/null || echo "unknown")

        if [[ "$overall_status" == "healthy" ]]; then
            pass_test "Health Endpoints"
        elif [[ "$overall_status" == "degraded" ]]; then
            warn_test "Health Endpoints" "Overall status is degraded"
        else
            fail_test "Health Endpoints" "Overall status: $overall_status"
        fi
    else
        fail_test "Health Endpoints" "Comprehensive health endpoint failed"
    fi
}

test_mcp_integration() {
    start_test "MCP Integration (PM-038)"

    # Test MCP health endpoint
    local mcp_response
    if mcp_response=$(make_request "$API_BASE_URL/health/mcp"); then
        local mcp_status
        mcp_status=$(echo "$mcp_response" | jq -r '.status' 2>/dev/null || echo "unknown")

        if [[ "$mcp_status" != "healthy" ]]; then
            fail_test "MCP Integration" "MCP status: $mcp_status"
            return 1
        fi

        # Check connection pooling
        local using_pool
        using_pool=$(echo "$mcp_response" | jq -r '.tests.connection_stats.using_pool' 2>/dev/null || echo "false")

        if [[ "$using_pool" != "true" ]]; then
            warn_test "MCP Integration" "Connection pooling not enabled (performance impact)"
        fi

        # Check search performance
        local search_time
        search_time=$(echo "$mcp_response" | jq -r '.tests.search_response_time_ms' 2>/dev/null || echo "999999")

        if (( $(echo "$search_time > $MAX_MCP_SEARCH_TIME_MS" | bc -l) )); then
            warn_test "MCP Integration" "Search time ${search_time}ms exceeds target ${MAX_MCP_SEARCH_TIME_MS}ms"
        fi

        # Check resource count
        local resource_count
        resource_count=$(echo "$mcp_response" | jq -r '.tests.resource_count' 2>/dev/null || echo "0")

        if [[ "$resource_count" -eq 0 ]]; then
            warn_test "MCP Integration" "No MCP resources available"
        fi

        pass_test "MCP Integration"
    else
        fail_test "MCP Integration" "MCP health endpoint failed"
    fi
}

test_api_functionality() {
    start_test "API Functionality"

    # Test intent classification endpoint
    local intent_payload='{"message": "test deployment verification", "session_id": "verification-test"}'
    local intent_response

    if intent_response=$(make_request "$API_BASE_URL/api/v1/intent" POST "$intent_payload" 15); then
        local intent_success
        intent_success=$(echo "$intent_response" | jq -r '.success' 2>/dev/null || echo "false")

        if [[ "$intent_success" == "true" ]]; then
            pass_test "API Functionality - Intent Classification"
        else
            warn_test "API Functionality" "Intent classification returned success=false"
        fi
    else
        fail_test "API Functionality" "Intent classification endpoint failed"
        return 1
    fi

    # Test file search endpoint (if MCP enabled)
    local search_response
    if search_response=$(make_request "$API_BASE_URL/api/v1/files/search?q=test&session_id=verification-test" GET "" 10); then
        local search_success
        search_success=$(echo "$search_response" | jq -r '.success' 2>/dev/null || echo "false")

        if [[ "$search_success" == "true" ]]; then
            pass_test "API Functionality - File Search"
        else
            warn_test "API Functionality" "File search returned success=false"
        fi
    else
        warn_test "API Functionality" "File search endpoint failed (may be expected if MCP disabled)"
    fi
}

test_performance() {
    start_test "Performance"

    local endpoints=(
        "$API_BASE_URL/health"
        "$API_BASE_URL/health/liveness"
        "$API_BASE_URL/health/readiness"
    )

    local slow_endpoints=()

    for endpoint in "${endpoints[@]}"; do
        local response_time
        response_time=$(measure_response_time "$endpoint")

        log DEBUG "Response time for $endpoint: ${response_time}ms"

        if [[ "$response_time" -gt "$MAX_RESPONSE_TIME_MS" ]]; then
            slow_endpoints+=("$endpoint (${response_time}ms)")
        fi
    done

    if [[ ${#slow_endpoints[@]} -eq 0 ]]; then
        pass_test "Performance"
    else
        warn_test "Performance" "Slow endpoints: ${slow_endpoints[*]}"
    fi
}

test_database_connectivity() {
    start_test "Database Connectivity"

    # Use docker exec to test database connection
    if docker-compose -f "$PROJECT_ROOT/docker-compose.staging.yml" exec -T postgres-staging \
        psql -U piper -d piper_morgan_staging -c "SELECT 1;" > /dev/null 2>&1; then
        pass_test "Database Connectivity"
    else
        fail_test "Database Connectivity" "PostgreSQL connection failed"
    fi
}

test_redis_connectivity() {
    start_test "Redis Connectivity"

    # Test Redis connectivity
    if docker-compose -f "$PROJECT_ROOT/docker-compose.staging.yml" exec -T redis-staging \
        redis-cli -a "staging_redis_secure_2025" ping > /dev/null 2>&1; then
        pass_test "Redis Connectivity"
    else
        fail_test "Redis Connectivity" "Redis connection failed"
    fi
}

test_chromadb_connectivity() {
    start_test "ChromaDB Connectivity"

    # Test ChromaDB heartbeat
    if make_request "http://localhost:8001/api/v1/heartbeat" > /dev/null 2>&1; then
        pass_test "ChromaDB Connectivity"
    else
        warn_test "ChromaDB Connectivity" "ChromaDB heartbeat failed"
    fi
}

test_container_health() {
    start_test "Container Health"

    # Get container status
    local container_status
    container_status=$(docker-compose -f "$PROJECT_ROOT/docker-compose.staging.yml" ps --format json 2>/dev/null || echo '[]')

    # Check for unhealthy containers
    local unhealthy_containers
    unhealthy_containers=$(echo "$container_status" | jq -r '.[] | select(.Health == "unhealthy") | .Name' 2>/dev/null || echo "")

    # Check for stopped containers
    local stopped_containers
    stopped_containers=$(echo "$container_status" | jq -r '.[] | select(.State != "running") | .Name' 2>/dev/null || echo "")

    if [[ -z "$unhealthy_containers" && -z "$stopped_containers" ]]; then
        pass_test "Container Health"
    else
        local issues=()
        if [[ -n "$unhealthy_containers" ]]; then
            issues+=("Unhealthy: $unhealthy_containers")
        fi
        if [[ -n "$stopped_containers" ]]; then
            issues+=("Stopped: $stopped_containers")
        fi
        fail_test "Container Health" "${issues[*]}"
    fi
}

test_monitoring_stack() {
    start_test "Monitoring Stack"

    # Test Prometheus
    if ! make_request "$PROMETHEUS_URL/-/healthy" > /dev/null 2>&1; then
        warn_test "Monitoring Stack" "Prometheus not healthy"
        return 1
    fi

    # Test Grafana
    if ! make_request "$GRAFANA_URL/api/health" > /dev/null 2>&1; then
        warn_test "Monitoring Stack" "Grafana not healthy"
        return 1
    fi

    pass_test "Monitoring Stack"
}

test_security_headers() {
    start_test "Security Headers"

    # Test for security headers via nginx
    local security_headers
    security_headers=$(curl -sI "$NGINX_BASE_URL" 2>/dev/null || echo "")

    local missing_headers=()

    if ! echo "$security_headers" | grep -qi "x-frame-options"; then
        missing_headers+=("X-Frame-Options")
    fi

    if ! echo "$security_headers" | grep -qi "x-content-type-options"; then
        missing_headers+=("X-Content-Type-Options")
    fi

    if [[ ${#missing_headers[@]} -eq 0 ]]; then
        pass_test "Security Headers"
    else
        warn_test "Security Headers" "Missing headers: ${missing_headers[*]}"
    fi
}

test_environment_variables() {
    start_test "Environment Variables"

    # Check if staging environment file exists and has required variables
    if [[ ! -f "$PROJECT_ROOT/.env.staging" ]]; then
        fail_test "Environment Variables" "Staging environment file not found"
        return 1
    fi

    local required_vars=(
        "APP_ENV=staging"
        "ENABLE_MCP_FILE_SEARCH=true"
        "USE_MCP_POOL=true"
    )

    local missing_vars=()

    for var in "${required_vars[@]}"; do
        if ! grep -q "$var" "$PROJECT_ROOT/.env.staging"; then
            missing_vars+=("$var")
        fi
    done

    if [[ ${#missing_vars[@]} -eq 0 ]]; then
        pass_test "Environment Variables"
    else
        fail_test "Environment Variables" "Missing or incorrect: ${missing_vars[*]}"
    fi
}

test_log_collection() {
    start_test "Log Collection"

    # Check if logs are being generated
    local log_files=(
        "$PROJECT_ROOT/logs/staging_deployment.log"
        "$PROJECT_ROOT/logs/staging_verification.log"
    )

    local missing_logs=()

    for log_file in "${log_files[@]}"; do
        if [[ ! -f "$log_file" ]] || [[ ! -s "$log_file" ]]; then
            missing_logs+=("$(basename "$log_file")")
        fi
    done

    if [[ ${#missing_logs[@]} -eq 0 ]]; then
        pass_test "Log Collection"
    else
        warn_test "Log Collection" "Missing or empty logs: ${missing_logs[*]}"
    fi
}

test_data_persistence() {
    start_test "Data Persistence"

    # Check if data volumes exist
    local volumes=(
        "piper_postgres_staging_data"
        "piper_redis_staging_data"
        "piper_chroma_staging_data"
    )

    local missing_volumes=()

    for volume in "${volumes[@]}"; do
        if ! docker volume ls | grep -q "$volume"; then
            missing_volumes+=("$volume")
        fi
    done

    if [[ ${#missing_volumes[@]} -eq 0 ]]; then
        pass_test "Data Persistence"
    else
        warn_test "Data Persistence" "Missing volumes: ${missing_volumes[*]}"
    fi
}

# Generate verification report
generate_verification_report() {
    log INFO "Generating verification report..."

    local report_file="$PROJECT_ROOT/logs/staging_verification_report_$(date +%Y%m%d_%H%M%S).json"
    local success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))

    # Get final health status
    local final_health
    final_health=$(make_request "$API_BASE_URL/health/comprehensive" 2>/dev/null || echo '{"overall_status": "unknown"}')

    cat > "$report_file" << EOF
{
  "verification_info": {
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "environment": "staging",
    "version": "PM-038-staging",
    "verifier": "${USER:-unknown}",
    "host": "$(hostname)"
  },
  "test_results": {
    "total_tests": $TOTAL_TESTS,
    "passed_tests": $PASSED_TESTS,
    "failed_tests": $FAILED_TESTS,
    "warnings": $WARNINGS,
    "success_rate_percent": $success_rate
  },
  "final_health_status": $final_health,
  "verification_status": "$(if [[ $FAILED_TESTS -eq 0 ]]; then echo "PASSED"; else echo "FAILED"; fi)",
  "recommendations": [
    $(if [[ $WARNINGS -gt 0 ]]; then echo "\"Review warning messages for potential issues\""; fi)
    $(if [[ $FAILED_TESTS -gt 0 ]]; then echo "\"Address failed tests before proceeding to production\""; fi)
  ]
}
EOF

    log INFO "Verification report generated: $report_file"
}

# Main verification function
main() {
    local start_time=$(date +%s)

    log INFO "Starting Piper Morgan staging deployment verification..."
    log INFO "Timestamp: $(date)"
    log INFO "Environment: staging"
    log INFO "Version: PM-038-staging"

    # Execute all tests
    test_basic_connectivity
    test_health_endpoints
    test_mcp_integration
    test_api_functionality
    test_performance
    test_database_connectivity
    test_redis_connectivity
    test_chromadb_connectivity
    test_container_health
    test_monitoring_stack
    test_security_headers
    test_environment_variables
    test_log_collection
    test_data_persistence

    # Generate report
    generate_verification_report

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))

    # Display summary
    log INFO "=== VERIFICATION SUMMARY ==="
    log INFO "Total Tests: $TOTAL_TESTS"
    log INFO "Passed: $PASSED_TESTS"
    log INFO "Failed: $FAILED_TESTS"
    log INFO "Warnings: $WARNINGS"
    log INFO "Success Rate: ${success_rate}%"
    log INFO "Duration: ${duration} seconds"
    log INFO "============================"

    # Final verdict
    if [[ $FAILED_TESTS -eq 0 ]]; then
        if [[ $WARNINGS -eq 0 ]]; then
            log INFO "🎉 Staging deployment verification PASSED - Ready for production!"
        else
            log INFO "✅ Staging deployment verification PASSED with warnings - Review warnings before production"
        fi
        exit 0
    else
        log ERROR "❌ Staging deployment verification FAILED - Address issues before proceeding"
        exit 1
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Check for required tools
    for tool in curl jq bc docker docker-compose; do
        if ! command -v "$tool" &> /dev/null; then
            log ERROR "Required tool '$tool' not found"
            exit 1
        fi
    done

    main "$@"
fi
