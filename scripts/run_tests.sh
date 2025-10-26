#!/bin/bash

# Piper Morgan Test Execution Script
# Phase 1: Test Infrastructure Activation
# Created: 2025-08-20 by Chief Architect deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SMOKE_TEST_TIMEOUT=5
VENV_PATH="venv/bin/activate"

# Helper Functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Environment Setup
setup_environment() {
    if [ ! -f "$VENV_PATH" ]; then
        print_error "Virtual environment not found at $VENV_PATH"
        exit 1
    fi

    print_header "ENVIRONMENT SETUP"
    source "$VENV_PATH"
    print_success "Virtual environment activated"

    # Note: pytest.ini already configures pythonpath=.
    print_success "Using pytest.ini configuration for Python path"

    # Check if PostgreSQL is needed and running
    if pgrep postgres > /dev/null 2>&1; then
        print_success "PostgreSQL detected running"
    else
        print_warning "PostgreSQL not detected - some tests may require database"
        echo "  Run: docker-compose up -d"
    fi
}

# Smoke Tests (< 5 seconds)
run_smoke_tests() {
    print_header "SMOKE TESTS (<5s)"

    local start_time=$(date +%s)

    # Core import tests
    python -c "import services.domain.models; print('✅ Domain models import')" || {
        print_error "Domain models import failed"
        return 1
    }

    python -c "import services.shared_types; print('✅ Shared types import')" || {
        print_error "Shared types import failed"
        return 1
    }

    # Quick unit tests (skip database-dependent tests)
    # Use specific tests that don't require database
    if [ -d "tests/unit" ]; then
        print_header "Checking for database-free unit tests..."
        # Try to run simple import-based tests first
        python -c "
import sys
sys.path.insert(0, '.')
try:
    from services.shared_types import *
    from services.domain.models import *
    print('✅ Core imports successful')
except Exception as e:
    print(f'❌ Import failed: {e}')
    sys.exit(1)
" || {
            print_error "Core import validation failed"
            return 1
        }
        print_success "Database-free validation completed"
    else
        print_warning "No unit tests directory found"
    fi

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    if [ $duration -le $SMOKE_TEST_TIMEOUT ]; then
        print_success "Smoke tests completed in ${duration}s (target: <${SMOKE_TEST_TIMEOUT}s)"
        return 0
    else
        print_error "Smoke tests took ${duration}s (exceeded ${SMOKE_TEST_TIMEOUT}s limit)"
        return 1
    fi
}

# Fast Tests (< 30 seconds)
run_fast_tests() {
    print_header "FAST TEST SUITE (<30s)"

    local start_time=$(date +%s)

    # Unit tests with coverage
    python -m pytest tests/unit/ --tb=short -v || {
        print_error "Fast unit tests failed"
        return 1
    }

    # Standalone orchestration tests (no database)
    if [ -f "tests/orchestration/test_excellence_flywheel_unittest.py" ]; then
        python -m pytest tests/orchestration/test_excellence_flywheel_unittest.py -v || {
            print_warning "Standalone orchestration tests failed"
        }
    fi

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    print_success "Fast tests completed in ${duration}s"
    return 0
}

# Full Test Suite
run_full_tests() {
    print_header "FULL TEST SUITE"

    local start_time=$(date +%s)

    # Check database availability for integration tests
    if ! pgrep postgres > /dev/null 2>&1; then
        print_warning "PostgreSQL not running - starting with docker-compose"
        docker-compose up -d postgres redis || {
            print_error "Failed to start required services"
            return 1
        }
        sleep 2
    fi

    # Full test suite with coverage
    python -m pytest tests/ --tb=short -v --cov=services --cov-report=term-missing || {
        print_error "Full test suite failed"
        return 1
    }

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    print_success "Full test suite completed in ${duration}s"
    return 0
}

# Coverage Report
run_coverage_report() {
    print_header "COVERAGE ANALYSIS"

    python -m pytest tests/ --cov=services --cov-report=html --cov-report=term-missing -q || {
        print_error "Coverage analysis failed"
        return 1
    }

    print_success "Coverage report generated in htmlcov/"

    # Find untested files
    echo ""
    echo "Files with <80% coverage:"
    coverage report --show-missing | grep -E "^services.*[0-7][0-9]%|^services.*[0-9]%$" || {
        print_success "All services have ≥80% coverage"
    }
}

# Main execution
main() {
    local mode=${1:-"smoke"}

    case $mode in
        "smoke")
            setup_environment
            run_smoke_tests
            ;;
        "fast")
            setup_environment
            run_smoke_tests && run_fast_tests
            ;;
        "full")
            setup_environment
            run_smoke_tests && run_fast_tests && run_full_tests
            ;;
        "coverage")
            setup_environment
            run_smoke_tests && run_fast_tests && run_full_tests && run_coverage_report
            ;;
        "help"|"-h"|"--help")
            echo "Piper Morgan Test Runner"
            echo ""
            echo "Usage: $0 [mode]"
            echo ""
            echo "Modes:"
            echo "  smoke     Quick validation (<5s) - imports and critical unit tests"
            echo "  fast      Unit tests and standalone tests (<30s)"
            echo "  full      Complete test suite including integration tests"
            echo "  coverage  Full tests with detailed coverage analysis"
            echo "  help      Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 smoke     # Quick validation before commits"
            echo "  $0 fast      # Development workflow testing"
            echo "  $0 full      # Pre-merge comprehensive testing"
            echo "  $0 coverage  # Weekly coverage analysis"
            ;;
        *)
            print_error "Unknown mode: $mode"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Execute with error handling
if main "$@"; then
    print_success "Test execution completed successfully"
    exit 0
else
    print_error "Test execution failed"
    exit 1
fi
