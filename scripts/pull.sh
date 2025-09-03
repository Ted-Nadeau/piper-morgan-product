   git add main.py tests/test_api_query_integration.py
   git commit -m "Harden query API error handling, align tests, and ensure robust contract (PM-009)

- Refactored error handling in /api/v1/intent to return 422 for missing/invalid context
- Allowed HTTPException to propagate for correct status codes/messages
- Updated integration tests to match improved API contract
- All query API tests now pass
- Noted asyncpg/SQLAlchemy connection cleanup warnings for future improvement
"
