#!/bin/bash
# Pattern Sweep - Compound Learning Acceleration Tool
# Standalone pattern detection for development workflow optimization
#
# Usage: ./scripts/run_pattern_sweep.sh [--learn-usage-patterns] [--verbose]

set -e

# Change to project root
cd "$(dirname "$0")/.."

# Default options
LEARN_PATTERNS=""
VERBOSE=""

# Parse arguments
for arg in "$@"; do
    case $arg in
        --learn-usage-patterns)
            LEARN_PATTERNS="--learn-usage-patterns"
            shift
            ;;
        --verbose|-v)
            VERBOSE="--verbose"
            shift
            ;;
        --help|-h)
            echo "Pattern Sweep - Compound Learning Acceleration Tool"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --learn-usage-patterns    Include session log pattern learning"
            echo "  --verbose, -v            Verbose output"
            echo "  --help, -h               Show this help"
            echo ""
            echo "Examples:"
            echo "  $0                              # Basic pattern sweep"
            echo "  $0 --verbose                    # With verbose output"
            echo "  $0 --learn-usage-patterns -v   # Full analysis with session logs"
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "🔍 Pattern Sweep - Compound Learning Acceleration"
echo "================================================"

# Run pattern sweep with proper Python path
PYTHONPATH=. python3 scripts/pattern_sweep.py --pattern-sweep-only $LEARN_PATTERNS $VERBOSE

echo ""
echo "✅ Pattern sweep complete! Check scripts/pattern_sweep_data.json for results."
