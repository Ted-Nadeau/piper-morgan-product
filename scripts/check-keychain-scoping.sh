#!/usr/bin/env bash
# check-keychain-scoping.sh — CI guard for #849 keychain scoping discipline
#
# Catches regressions where keychain calls bypass user-scoped keys.
# Exit 0 = clean, Exit 1 = violations found.
#
# Usage: ./scripts/check-keychain-scoping.sh
# CI:    Add to .github/workflows as a lint step

set -euo pipefail

VIOLATIONS=0
WARNINGS=0

echo "=== Keychain Scoping Guard (Issue #849) ==="
echo ""

# ─── Pattern 1: f-string provider names in keychain calls ────────────────────
# BAD:  store_api_key(f"slack_bot_{user_id}", token)
# GOOD: store_api_key("slack_bot", token, username=user_id)
echo "Checking for f-string provider names in keychain calls..."
FSTRING_HITS=$(grep -rn 'store_api_key(f"' services/ web/ --include='*.py' 2>/dev/null || true)
if [ -n "$FSTRING_HITS" ]; then
    echo "VIOLATION: f-string in keychain provider name (use username= param instead):"
    echo "$FSTRING_HITS"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "  OK: No f-string provider names found"
fi

# ─── Pattern 2: Global keychain calls in route handlers ──────────────────────
# BAD:  keychain.get_api_key("github_token")       (no username)
# GOOD: keychain.get_api_key("github_token", username=current_user.sub)
echo ""
echo "Checking for non-scoped keychain calls in route handlers..."
ROUTE_GLOBAL_HITS=$(grep -rn '\.get_api_key("[^"]*")$' web/api/routes/ --include='*.py' 2>/dev/null || true)
ROUTE_STORE_HITS=$(grep -rn '\.store_api_key("[^"]*", [^,)]*)\s*$' web/api/routes/ --include='*.py' 2>/dev/null || true)
ROUTE_DELETE_HITS=$(grep -rn '\.delete_api_key("[^"]*")$' web/api/routes/ --include='*.py' 2>/dev/null || true)

if [ -n "$ROUTE_GLOBAL_HITS" ]; then
    echo "VIOLATION: get_api_key without username= in routes:"
    echo "$ROUTE_GLOBAL_HITS"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "  OK: No global get_api_key calls in routes"
fi

if [ -n "$ROUTE_STORE_HITS" ]; then
    echo "VIOLATION: store_api_key without username= in routes:"
    echo "$ROUTE_STORE_HITS"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "  OK: No global store_api_key calls in routes"
fi

if [ -n "$ROUTE_DELETE_HITS" ]; then
    echo "VIOLATION: delete_api_key without username= in routes:"
    echo "$ROUTE_DELETE_HITS"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "  OK: No global delete_api_key calls in routes"
fi

# ─── Pattern 3: CalendarIntegrationRouter() without user_id ──────────────────
# BAD:  CalendarIntegrationRouter()
# GOOD: CalendarIntegrationRouter(user_id=user_id)
# EXEMPT: docstrings, comments, CalendarPlugin singleton (documented in #849)
echo ""
echo "Checking for CalendarIntegrationRouter() without user_id..."
CAL_HITS=$(grep -rn 'CalendarIntegrationRouter()' services/ web/ --include='*.py' 2>/dev/null | grep -v '^\s*#' | grep -v '"""' | grep -v "'''" | grep -v 'test_' || true)
if [ -n "$CAL_HITS" ]; then
    echo "WARNING: CalendarIntegrationRouter() without user_id (verify if intentional):"
    echo "$CAL_HITS"
    WARNINGS=$((WARNINGS + 1))
else
    echo "  OK: No bare CalendarIntegrationRouter() calls"
fi

# ─── Pattern 4: Wrong key names in connection tests ──────────────────────────
# BAD:  get_api_key("slack")    — should be "slack_bot"
# BAD:  get_api_key("github")   — should be "github_token"
echo ""
echo "Checking for wrong key names in connection tests..."
WRONG_SLACK=$(grep -rn 'get_api_key("slack")' web/ services/ --include='*.py' 2>/dev/null || true)
WRONG_GITHUB=$(grep -rn 'get_api_key("github")' web/ services/ --include='*.py' 2>/dev/null || true)

if [ -n "$WRONG_SLACK" ]; then
    echo "VIOLATION: get_api_key(\"slack\") — should be \"slack_bot\":"
    echo "$WRONG_SLACK"
    VIOLATIONS=$((VIOLATIONS + 1))
fi

if [ -n "$WRONG_GITHUB" ]; then
    echo "VIOLATION: get_api_key(\"github\") — should be \"github_token\":"
    echo "$WRONG_GITHUB"
    VIOLATIONS=$((VIOLATIONS + 1))
fi

if [ -z "$WRONG_SLACK" ] && [ -z "$WRONG_GITHUB" ]; then
    echo "  OK: No wrong key names found"
fi

# ─── Pattern 5: Wrong disconnect key names ───────────────────────────────────
# BAD:  delete_api_key("slack_bot_token")  — should be "slack_bot"
echo ""
echo "Checking for wrong disconnect key names..."
WRONG_DISCONNECT=$(grep -rn 'delete_api_key("slack_bot_token")' web/ services/ --include='*.py' 2>/dev/null || true)
if [ -n "$WRONG_DISCONNECT" ]; then
    echo "VIOLATION: delete_api_key(\"slack_bot_token\") — should be \"slack_bot\":"
    echo "$WRONG_DISCONNECT"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "  OK: No wrong disconnect key names"
fi

# ─── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo "=== Results ==="
echo "Violations: $VIOLATIONS"
echo "Warnings:   $WARNINGS"

if [ $VIOLATIONS -gt 0 ]; then
    echo ""
    echo "FAILED: $VIOLATIONS keychain scoping violation(s) found."
    echo "See Issue #849 for the canonical keychain scoping pattern."
    exit 1
fi

if [ $WARNINGS -gt 0 ]; then
    echo ""
    echo "PASSED with $WARNINGS warning(s). Review recommended."
    exit 0
fi

echo ""
echo "PASSED: All keychain scoping checks clean."
exit 0
