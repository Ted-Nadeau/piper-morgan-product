# Session Log: FileRepository Connection Pattern Investigation

**Date:** 2025-07-14
**Duration:** ~30 minutes
**Focus:** Investigating FileRepository connection pool vs session pattern issue
**Status:** Complete

## Summary
Investigated the architectural mismatch between FileRepository's asyncpg connection pool pattern and the test fixture's SQLAlchemy AsyncSession pattern. Analyzed the codebase architecture, patterns, and DDD compliance to determine the correct approach.

## Problems Addressed
1. FileRepository expects connection pool with `.acquire()` method
2. Test fixtures provide AsyncSession objects without `.acquire()`
3. Tests failing due to interface mismatch
4. Unclear whether to use pools or sessions as standard

## Solutions Implemented
No code changes implemented - this was an investigation and analysis session.

## Key Decisions Made

### Architectural Finding
Two repository systems currently coexist:
1. **SQLAlchemy Repositories** (most repos) - Use AsyncSession, follow pattern catalog
2. **Raw SQL Repositories** (FileRepository, WorkflowRepository) - Use asyncpg pools, predate standards

### DDD Analysis Results
- Pattern Catalog explicitly documents `BaseRepository(session: AsyncSession)` as the standard
- Repository is infrastructure layer - implementation details shouldn't leak to domain
- Domain models have no repository interfaces (correct DDD separation)
- Tests designed around session fixtures, not pool fixtures

### Recommendation
**Standardize on SQLAlchemy Sessions** by migrating FileRepository to:
- Inherit from BaseRepository
- Use AsyncSession instead of connection pools
- Convert raw SQL to SQLAlchemy ORM queries
- Maintain same public interface (return domain models)

This aligns with:
- Pattern Catalog documentation (Pattern #1: Repository Pattern)
- Existing test infrastructure
- Majority of existing repositories
- DDD principles (infrastructure standardization)

## Files Modified
None - investigation only

## Next Steps
1. Create a new FileRepository implementation using BaseRepository pattern
2. Migrate existing raw SQL queries to SQLAlchemy ORM
3. Update all FileRepository instantiations to use sessions
4. Verify all tests pass with new implementation
5. Consider similar migration for WorkflowRepository

## Technical Details

### Current FileRepository Pattern
```python
class FileRepository:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def get_file_by_id(self, file_id: str):
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM uploaded_files WHERE id = $1", file_id)
```

### Target Pattern (Following Pattern Catalog)
```python
class FileRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UploadedFileDB)

    async def get_file_by_id(self, file_id: str) -> Optional[UploadedFile]:
        result = await self.session.execute(
            select(UploadedFileDB).where(UploadedFileDB.id == file_id)
        )
        db_file = result.scalar_one_or_none()
        return self._to_domain(db_file) if db_file else None
```

### Production vs Test Usage
- **Production**: Uses DatabasePool.get_pool() for FileRepository
- **Tests**: Expect db_session fixture (AsyncSession)
- **Issue**: Interface mismatch causes test failures

### Architectural Principles Applied
1. **Repository Pattern**: Infrastructure concern, not domain
2. **DDD Compliance**: Keep domain pure, standardize infrastructure
3. **Test Alignment**: Tests should use same patterns as production
4. **Pattern Consistency**: Follow documented patterns in pattern-catalog.md
