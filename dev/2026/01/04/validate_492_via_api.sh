#!/bin/bash
# Issue #492: Canonical Query Validation via API
# Tests all 25 canonical queries against the running server

BASE_URL="http://localhost:8001"

echo "============================================================"
echo "Issue #492: Canonical Query Test Matrix Validation"
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo "============================================================"

# Function to test a query
test_query() {
    local num=$1
    local query=$2
    local expected=$3

    # Make the API call
    response=$(curl -s -X POST "${BASE_URL}/api/v1/intent" \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"${query}\"}" 2>/dev/null)

    # Check for error response
    if echo "$response" | grep -q "authentication_required"; then
        echo "  ⚠️  Q${num}: AUTH_REQUIRED - ${query}"
        return
    fi

    if echo "$response" | grep -q "error"; then
        echo "  💥 Q${num}: ERROR - ${query}"
        echo "      Response: $(echo "$response" | head -c 100)"
        return
    fi

    # Extract category from response
    category=$(echo "$response" | grep -o '"category"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)"$/\1/')

    if [ -z "$category" ]; then
        echo "  ❓ Q${num}: NO_CATEGORY - ${query}"
    elif [ "${category^^}" == "${expected}" ]; then
        echo "  ✅ Q${num}: PASS (${category}) - ${query}"
    else
        echo "  ⚠️  Q${num}: ${category} (expected ${expected}) - ${query}"
    fi
}

echo ""
echo "### Identity Queries (1-5) ###"
test_query "1" "What's your name?" "IDENTITY"
test_query "2" "What can you help me with?" "IDENTITY"
test_query "3" "Are you working properly?" "IDENTITY"
test_query "4" "How do I get help?" "IDENTITY"
test_query "5" "What makes you different?" "IDENTITY"

echo ""
echo "### Temporal Queries (6-10) ###"
test_query "6" "What day is it?" "TEMPORAL"
test_query "7" "What did we accomplish yesterday?" "TEMPORAL"
test_query "8" "What's on the agenda for today?" "TEMPORAL"
test_query "9" "When was the last time we worked on this?" "TEMPORAL"
test_query "10" "How long have we been working on this project?" "TEMPORAL"

echo ""
echo "### Spatial Queries (11-15) ###"
test_query "11" "What projects are we working on?" "STATUS"
test_query "12" "Show me the project landscape" "STATUS"
test_query "13" "Which project should I focus on?" "PRIORITY"
test_query "14" "What's the status of piper-morgan?" "STATUS"
test_query "15" "Where are we in the project lifecycle?" "STATUS"

echo ""
echo "### Capability Queries (16-20) ###"
test_query "16" "Create a GitHub issue about testing" "EXECUTION"
test_query "17" "Analyze this document" "EXECUTION"
test_query "18" "List all my projects" "QUERY"
test_query "19" "Generate a status report" "QUERY"
test_query "20" "Search for authentication in our documents" "QUERY"

echo ""
echo "### Predictive Queries (21-25) ###"
test_query "21" "What should I focus on today?" "PRIORITY"
test_query "22" "What patterns do you see?" "LEARNING"
test_query "23" "What risks should I be aware of?" "ANALYSIS"
test_query "24" "What opportunities should I pursue?" "SYNTHESIS"
test_query "25" "What's the next milestone?" "PLANNING"

echo ""
echo "============================================================"
echo "Validation complete"
echo "============================================================"
