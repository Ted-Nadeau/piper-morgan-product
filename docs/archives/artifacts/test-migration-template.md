# Test Migration Template: AsyncSessionFactory Patterns

This document provides templates for migrating tests from legacy database session patterns to the new AsyncSessionFactory patterns.

## Overview

The test infrastructure has been updated to use `AsyncSessionFactory` patterns that match production code. This ensures consistency and prevents transaction-related bugs.

## Available Fixtures

### New Fixtures (Use these for new tests)

1. **`async_session`** - For basic database operations
2. **`async_transaction`** - For operations requiring explicit transactions
3. **`db_session`** - Legacy fixture (now uses AsyncSessionFactory internally)

## Migration Patterns

### Pattern 1: Basic Database Operations

**OLD:**
```python
async def test_something(db_session: AsyncSession):
    repo = SomeRepository(db_session)
    result = await repo.find_by_id("some-id")
    assert result is not None
```

**NEW:**
```python
async def test_something(async_session):
    async with async_session as session:
        repo = SomeRepository(session)
        result = await repo.find_by_id("some-id")
        assert result is not None
```

### Pattern 2: Database Operations with Transactions

**OLD:**
```python
async def test_create_and_find(db_session: AsyncSession):
    repo = SomeRepository(db_session)

    # Create entity
    entity = SomeEntity(name="test")
    db_session.add(entity)
    await db_session.commit()

    # Find entity
    result = await repo.find_by_id(entity.id)
    assert result is not None
```

**NEW:**
```python
async def test_create_and_find(async_transaction):
    async with async_transaction as session:
        repo = SomeRepository(session)

        # Create entity
        entity = SomeEntity(name="test")
        session.add(entity)
        await session.flush()  # Make data available in same transaction

        # Find entity
        result = await repo.find_by_id(entity.id)
        assert result is not None
```

### Pattern 3: Multiple Database Operations

**OLD:**
```python
async def test_multiple_operations(db_session: AsyncSession):
    repo1 = Repository1(db_session)
    repo2 = Repository2(db_session)

    # Multiple operations with shared session
    entity1 = await repo1.create(name="test1")
    entity2 = await repo2.create(name="test2", ref_id=entity1.id)

    await db_session.commit()

    # Verify
    result1 = await repo1.find_by_id(entity1.id)
    result2 = await repo2.find_by_id(entity2.id)
    assert result1 and result2
```

**NEW:**
```python
async def test_multiple_operations(async_transaction):
    async with async_transaction as session:
        repo1 = Repository1(session)
        repo2 = Repository2(session)

        # Multiple operations with shared session
        entity1 = await repo1.create(name="test1")
        entity2 = await repo2.create(name="test2", ref_id=entity1.id)

        await session.flush()  # Make data available in same transaction

        # Verify
        result1 = await repo1.find_by_id(entity1.id)
        result2 = await repo2.find_by_id(entity2.id)
        assert result1 and result2
```

### Pattern 4: Loop Operations (HIGH PRIORITY)

**OLD:**
```python
async def test_loop_operations(db_session_factory):
    for i in range(10):
        async with await db_session_factory() as session:
            repo = SomeRepository(session)
            await repo.create(name=f"test-{i}")
```

**NEW:**
```python
async def test_loop_operations(async_session):
    for i in range(10):
        async with async_session as session:
            repo = SomeRepository(session)
            await repo.create(name=f"test-{i}")
```

## Import Changes

### Remove Old Imports

```python
# Remove these imports
from sqlalchemy.ext.asyncio import AsyncSession
from services.database.connection import db
```

### Add New Imports (if needed)

```python
# Only add if you need to import specific types
from services.database.session_factory import AsyncSessionFactory
```

## Key Differences

1. **Session Management**: Use `async with` context manager instead of direct session access
2. **Transaction Control**: Use `async_transaction` for explicit transactions
3. **Data Availability**: Use `await session.flush()` instead of `await session.commit()` in tests
4. **Type Hints**: Remove `AsyncSession` type hints from test function parameters

## Migration Checklist

For each test file:

- [ ] Replace `db_session: AsyncSession` with `async_session` or `async_transaction`
- [ ] Wrap database operations in `async with` context managers
- [ ] Replace `await session.commit()` with `await session.flush()` in tests
- [ ] Remove `AsyncSession` imports
- [ ] Update type hints to remove `AsyncSession` references
- [ ] Test the migration with `PYTHONPATH=. pytest tests/your_test_file.py`

## Example Full Migration

**Before:**
```python
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from services.repositories.some_repository import SomeRepository

async def test_repository_operations(db_session: AsyncSession):
    repo = SomeRepository(db_session)

    # Create
    entity = await repo.create(name="test")
    await db_session.commit()

    # Read
    result = await repo.find_by_id(entity.id)
    assert result.name == "test"
```

**After:**
```python
import pytest

from services.repositories.some_repository import SomeRepository

async def test_repository_operations(async_transaction):
    async with async_transaction as session:
        repo = SomeRepository(session)

        # Create
        entity = await repo.create(name="test")
        await session.flush()

        # Read
        result = await repo.find_by_id(entity.id)
        assert result.name == "test"
```

## Testing Your Migration

After migrating a test file, verify it works:

```bash
# Run the specific test file
PYTHONPATH=. pytest tests/your_migrated_test.py -v

# Run all tests to ensure no regressions
PYTHONPATH=. pytest
```

## Common Issues

1. **"Transaction already begun"** - Use `async_session` instead of `async_transaction`
2. **Data not found** - Use `await session.flush()` to make data available
3. **Import errors** - Remove old `AsyncSession` imports
4. **Type errors** - Remove `AsyncSession` type hints from test parameters

## Priority Order

Migrate tests in this order:
1. **Critical infrastructure tests** (repositories, database models)
2. **High-usage test files** (frequently run tests)
3. **Integration tests** (end-to-end scenarios)
4. **Unit tests** (isolated component tests)
