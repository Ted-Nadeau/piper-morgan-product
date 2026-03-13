# Phase 1: Database Schema Creation - CORE-KNOW #99

**Agent**: Claude Code (Programmer)
**Issue**: #99 - CORE-KNOW
**Phase**: 1 - Database Schema Creation
**Date**: October 18, 2025, 2:10 PM
**Duration**: ~30 minutes estimated

---

## Mission

Create the PostgreSQL tables for the Knowledge Graph. The schema is already documented in the repository code (KnowledgeGraphRepository lines 274-520), but the tables haven't been created in the database.

## Context

**From Phase -1 Discovery**:
- ✅ KnowledgeGraphService exists (468+ lines, fully implemented)
- ✅ KnowledgeGraphRepository exists (PostgreSQL backend ready)
- ✅ Schema documented in code
- ❌ PostgreSQL tables NOT created/deployed
- ❌ Cannot test Knowledge Graph without tables

**This is a quick win**: Just need to extract schema from code and create tables.

---

## Your Task

### Step 1: Find the Schema Definition (5 minutes)

**Locate schema in repository**:
```python
# From Phase -1, we know it's at:
# services/knowledge/knowledge_graph_repository.py (lines 274-520)

# Use Serena to read the schema
mcp__serena__view_file(
    path="services/knowledge/knowledge_graph_repository.py",
    start_line=274,
    end_line=520
)
```

**Look for**:
- Table definitions (CREATE TABLE statements or SQLAlchemy models)
- Column definitions
- Indexes
- Foreign keys
- Constraints

### Step 2: Create Migration File (10 minutes)

**Location**: `migrations/versions/YYYYMMDD_HHMM_knowledge_graph_schema.sql`

**Example structure**:
```sql
-- Migration: Knowledge Graph Schema
-- Date: 2025-10-18
-- Issue: #99 CORE-KNOW

BEGIN;

-- Knowledge Nodes Table
CREATE TABLE IF NOT EXISTS knowledge_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_type VARCHAR(50) NOT NULL,
    content JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding VECTOR(1536),  -- If using pgvector
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge Edges Table
CREATE TABLE IF NOT EXISTS knowledge_edges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    target_id UUID NOT NULL REFERENCES knowledge_nodes(id) ON DELETE CASCADE,
    edge_type VARCHAR(50) NOT NULL,
    properties JSONB DEFAULT '{}',
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_id, target_id, edge_type)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_nodes_type ON knowledge_nodes(node_type);
CREATE INDEX IF NOT EXISTS idx_nodes_created ON knowledge_nodes(created_at);
CREATE INDEX IF NOT EXISTS idx_edges_source ON knowledge_edges(source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target ON knowledge_edges(target_id);
CREATE INDEX IF NOT EXISTS idx_edges_type ON knowledge_edges(edge_type);

-- Composite index for graph traversal
CREATE INDEX IF NOT EXISTS idx_edges_source_type ON knowledge_edges(source_id, edge_type);
CREATE INDEX IF NOT EXISTS idx_edges_target_type ON knowledge_edges(target_id, edge_type);

-- JSONB indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_nodes_metadata ON knowledge_nodes USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_edges_properties ON knowledge_edges USING GIN(properties);

COMMIT;
```

**Adapt to actual schema** found in repository code.

### Step 3: Apply Migration (10 minutes)

**Check if there's a migration system**:
```bash
# Look for migration tools
ls migrations/
ls alembic/  # If using Alembic
```

**Option A: If migration system exists**:
```bash
# Use existing migration tool
alembic upgrade head
# or
./scripts/migrate.sh
```

**Option B: If no migration system** (likely):
```bash
# Apply directly to PostgreSQL
psql -U piper_morgan -d piper_morgan_db -f migrations/versions/20251018_2010_knowledge_graph_schema.sql

# Or using Python
python -c "
from services.database import get_db_connection
conn = get_db_connection()
with open('migrations/versions/20251018_2010_knowledge_graph_schema.sql') as f:
    conn.execute(f.read())
conn.commit()
"
```

### Step 4: Verify Tables Created (5 minutes)

**Test table creation**:
```python
# Quick verification script
import asyncio
from services.knowledge.knowledge_graph_repository import KnowledgeGraphRepository

async def verify_tables():
    repo = KnowledgeGraphRepository()

    # Try to create a test node
    test_node = await repo.create_node(
        node_type="test",
        content={"message": "Schema verification test"}
    )

    print(f"✅ Tables created! Test node ID: {test_node.id}")

    # Clean up
    await repo.delete_node(test_node.id)
    print("✅ Cleanup successful")

asyncio.run(verify_tables())
```

**Expected Output**:
```
✅ Tables created! Test node ID: 550e8400-e29b-41d4-a716-446655440000
✅ Cleanup successful
```

---

## Important Notes

### Schema Discovery

**From Phase -1, schema is documented at**:
- File: `services/knowledge/knowledge_graph_repository.py`
- Lines: 274-520
- Likely contains: SQLAlchemy models or raw SQL

**Your job**: Extract and create the actual tables.

### Database Connection

**Check configuration**:
```python
# Look for database config
mcp__serena__search_project(
    query="DATABASE_URL.*knowledge",
    file_pattern="**/*.py"
)

# Or check environment variables
grep -r "DATABASE" .env* config/
```

**Database likely**:
- Name: `piper_morgan_db` (or similar)
- User: `piper_morgan`
- Host: `localhost`
- Port: `5432`

### Vector Extension (If Needed)

If schema uses `pgvector` for embeddings:
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;
```

### Error Handling

**If tables already exist**:
- Use `CREATE TABLE IF NOT EXISTS`
- Or check first: `SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = 'knowledge_nodes')`

**If migration fails**:
- Check PostgreSQL is running
- Verify database exists
- Check user permissions
- Look for syntax errors

---

## Success Criteria

Phase 1 is complete when:

- [ ] Migration file created with complete schema
- [ ] Tables created in PostgreSQL
- [ ] Indexes created for performance
- [ ] Verification test passes (create/delete node)
- [ ] No errors in table creation
- [ ] Ready for Phase 2 (IntentService integration)

---

## Deliverables

1. **Migration File**: `migrations/versions/YYYYMMDD_HHMM_knowledge_graph_schema.sql`
2. **Verification Script**: `dev/2025/10/18/verify-kg-schema.py`
3. **Phase 1 Report**: `dev/2025/10/18/phase-1-schema-report.md`

---

## Time Estimate

- Schema discovery: 5 minutes
- Migration file creation: 10 minutes
- Apply migration: 10 minutes
- Verification: 5 minutes
- **Total**: 30 minutes

**Time Lords applies**: Take time needed for correctness.

---

## Next Phase Preview

**Phase 2** (after this completes):
- Integrate KnowledgeGraphService with IntentService
- Add feature flag control
- Enhance context with graph insights
- Test with canonical queries

But first: Get the database tables created!

---

## Questions?

If you encounter:
- **Unclear schema**: Read KnowledgeGraphRepository code more carefully
- **No database**: May need to create database first
- **Permission errors**: Check database user permissions
- **Migration system unclear**: Just use raw SQL

---

**Ready to create the Knowledge Graph database schema!** 🗄️

**This unlocks all of Phase 2 (integration) and makes the KG operational.**
