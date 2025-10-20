#!/bin/bash
# Error Handling Test Suite - Task 5
# Testing all error scenarios for Standup API

RESULTS_FILE="dev/active/error-handling-test-results.txt"
API_URL="http://localhost:8001/api/v1/standup/generate"

# Test 1: No Authentication
echo "" >> $RESULTS_FILE
echo "=== Test 1: No Authentication ===" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE
curl -i -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"mode":"standard"}' >> $RESULTS_FILE 2>&1

# Test 2: Invalid Token
echo "" >> $RESULTS_FILE
echo "=== Test 2: Invalid Token ===" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE
curl -i -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token_123" \
  -d '{"mode":"standard"}' >> $RESULTS_FILE 2>&1

# Generate valid token for remaining tests
export PYTHONPATH=/Users/xian/Development/piper-morgan
TOKEN=$(python3 scripts/generate_test_token.py)

# Test 3: Invalid Mode
echo "" >> $RESULTS_FILE
echo "=== Test 3: Invalid Mode (Pydantic validation) ===" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE
curl -i -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"mode":"invalid_mode"}' >> $RESULTS_FILE 2>&1

# Test 4: Invalid Format
echo "" >> $RESULTS_FILE
echo "=== Test 4: Invalid Format (Pydantic validation) ===" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE
curl -i -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"mode":"standard","format":"invalid"}' >> $RESULTS_FILE 2>&1

# Test 5: Malformed JSON
echo "" >> $RESULTS_FILE
echo "=== Test 5: Malformed JSON ===" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE
curl -i -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{invalid json}' >> $RESULTS_FILE 2>&1

# Test 6: Empty Body (should use defaults and succeed)
echo "" >> $RESULTS_FILE
echo "=== Test 6: Empty Request Body (should use defaults) ===" >> $RESULTS_FILE
echo "" >> $RESULTS_FILE
curl -i -X POST $API_URL \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{}' >> $RESULTS_FILE 2>&1

echo "✅ All tests complete - results saved to $RESULTS_FILE"
