# Issue: Add Schema Validation Check on Startup

**Type**: Enhancement
**Priority**: P1
**Sprint**: S2 (Security Polish)
**Estimate**: 4-6 hours
**Labels**: security, integration-testing, architecture

## Context

From Dec 7 alpha testing, we discovered that database schema and SQLAlchemy models had drifted: schema defined `owner_id` columns as `uuid` type while models defined them as `String`. This caused all CRUD operations to fail despite 705 unit tests passing.

This is an instance of the "Green Tests, Red User" pattern where unit tests with mocks pass but real database operations fail.

## Problem Statement

Schema/model drift can occur when:
- Migrations change column types but models aren't updated
- Models are modified without corresponding migrations
- Type definitions diverge over time

Currently, this drift is only discovered when users encounter failures in production/alpha.

## Proposed Solution

Implement a startup validation check that:
1. Introspects actual database schema
2. Compares with SQLAlchemy model definitions
3. Reports type mismatches, missing columns, or extra columns
4. Fails fast with clear error messages if drift detected

## Acceptance Criteria

- [ ] Create `schema_validator.py` utility that compares DB schema with models
- [ ] Check runs automatically on application startup (can be disabled via env var for tests)
- [ ] Validates all critical tables: users, todos, projects, files, lists, workflows
- [ ] Reports specific mismatches (e.g., "ProjectDB.owner_id expects String but DB has uuid")
- [ ] Non-blocking warnings for non-critical differences
- [ ] Blocking errors for type mismatches that would cause runtime failures
- [ ] Performance: validation completes in <2 seconds for full schema
- [ ] Documentation: Add to developer setup guide

## Technical Approach

```python
# Example implementation pattern
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import UUID
from typing import List, Dict, Any

class SchemaValidator:
    def __init__(self, engine):
        self.engine = engine
        self.inspector = inspect(engine)

    def validate_model(self, model_class) -> List[str]:
        """Compare model definition with actual database schema"""
        errors = []
        table_name = model_class.__tablename__

        # Get actual columns from database
        db_columns = {col['name']: col for col in
                     self.inspector.get_columns(table_name)}

        # Compare with model columns
        for column in model_class.__table__.columns:
            if column.name in db_columns:
                # Check type compatibility
                if not self._types_compatible(column.type,
                                             db_columns[column.name]['type']):
                    errors.append(
                        f"{model_class.__name__}.{column.name}: "
                        f"Model expects {column.type} but DB has "
                        f"{db_columns[column.name]['type']}"
                    )

        return errors
```

## Testing

- [ ] Unit tests with mock schemas (both matching and mismatched)
- [ ] Integration test against real PostgreSQL
- [ ] Test with deliberately mismatched migration
- [ ] Performance test with full production schema
- [ ] Test disable flag for CI/CD environments

## Dependencies

- Requires SQLAlchemy introspection capabilities (already available)
- Should run after database connection established
- Must run before first query execution

## Related Issues

- #479: CRUD Failures (root cause this would prevent)
- #440: ALPHA-SETUP-TEST (includes schema validation in scope)
- Pattern-044: "Green Tests, Red User" (this implements prevention strategy)

## Success Metrics

- Zero schema/model drift incidents after implementation
- Developers catch drift during local development, not in alpha/production
- Clear error messages reduce debugging time from hours to minutes

## Notes

This is a critical integration testing gap identified during Dec 7 debugging marathon. Implementing this prevents the entire class of bugs where models and schema diverge.

The Chief of Staff memo identified this as a prevention strategy for the "Green Tests, Red User" pattern.
