#!/bin/bash

# Pre-commit Security Check Hook
# Runs basic security checks before allowing commits

set -e

echo "🔍 Running pre-commit security checks..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository"
    exit 1
fi

# Function to check for secrets in staged files
check_secrets() {
    echo "  Checking for hardcoded secrets..."

    # Common secret patterns
    PATTERNS=(
        "api[_-]?key.*=.*['\"][a-zA-Z0-9]{20,}['\"]"
        "secret.*=.*['\"][a-zA-Z0-9]{20,}['\"]"
        "token.*=.*['\"][a-zA-Z0-9]{20,}['\"]"
        "password.*=.*['\"][^'\"]{8,}['\"]"
        "AWS[_-]?ACCESS[_-]?KEY"
        "AWS[_-]?SECRET[_-]?ACCESS[_-]?KEY"
        "GITHUB[_-]?TOKEN"
        "ghp_[a-zA-Z0-9]{36}"
        "ghs_[a-zA-Z0-9]{36}"
        "sk-[a-zA-Z0-9]{48}"  # OpenAI API key
    )

    FOUND_SECRETS=0
    for pattern in "${PATTERNS[@]}"; do
        if git diff --cached --name-only | xargs -I {} git diff --cached {} | grep -iE "$pattern" > /dev/null 2>&1; then
            echo "  ⚠️  Potential secret detected matching pattern: $pattern"
            FOUND_SECRETS=1
        fi
    done

    if [ $FOUND_SECRETS -eq 1 ]; then
        echo "  ❌ Potential secrets found in staged files!"
        echo "     Please review your changes and remove any hardcoded secrets."
        echo "     Use environment variables or secure secret management instead."
        return 1
    else
        echo "  ✅ No obvious secrets detected"
        return 0
    fi
}

# Function to check NPM vulnerabilities (if package files changed)
check_npm_security() {
    if git diff --cached --name-only | grep -E "package(-lock)?\.json" > /dev/null; then
        echo "  Checking NPM dependencies for vulnerabilities..."

        if command -v npm &> /dev/null; then
            # Run audit but don't block on low/moderate issues
            if npm audit --audit-level=high > /dev/null 2>&1; then
                echo "  ✅ No high or critical NPM vulnerabilities"
            else
                echo "  ⚠️  High or critical NPM vulnerabilities found!"
                echo "     Run 'npm audit' for details and 'npm audit fix' to resolve"
                # Uncomment the next line to block commits with vulnerabilities
                # return 1
            fi
        else
            echo "  ⚠️  npm not found - skipping dependency check"
        fi
    fi
    return 0
}

# Function to check Python dependencies (if requirements files changed)
check_python_security() {
    if git diff --cached --name-only | grep -E "requirements.*\.txt|Pipfile|pyproject\.toml" > /dev/null; then
        echo "  Checking Python dependencies for vulnerabilities..."

        if command -v safety &> /dev/null; then
            if safety check --json > /dev/null 2>&1; then
                echo "  ✅ No known Python vulnerabilities"
            else
                echo "  ⚠️  Python dependency vulnerabilities found!"
                echo "     Run 'safety check' for details"
                # Uncomment the next line to block commits with vulnerabilities
                # return 1
            fi
        else
            echo "  ℹ️  'safety' not installed - run 'pip install safety' to enable Python security checks"
        fi
    fi
    return 0
}

# Function to check for debug code
check_debug_code() {
    echo "  Checking for debug code..."

    DEBUG_PATTERNS=(
        "console\.log"
        "print\("
        "debugger"
        "import pdb"
        "pdb\.set_trace"
        "breakpoint\(\)"
        "TODO.*security"
        "FIXME.*security"
        "XXX.*security"
    )

    FOUND_DEBUG=0
    for pattern in "${DEBUG_PATTERNS[@]}"; do
        if git diff --cached --name-only | xargs -I {} git diff --cached {} | grep -E "$pattern" > /dev/null 2>&1; then
            echo "  ℹ️  Debug/development code found: $pattern"
            # This is informational only, not blocking
        fi
    done

    echo "  ✅ Debug code check complete"
    return 0
}

# Main execution
echo ""
check_secrets || exit 1
check_npm_security
check_python_security
check_debug_code

echo ""
echo "✅ Pre-commit security checks passed!"
echo ""
