# Investigation Instructions: Issue #262 UUID Migration

**Date**: November 8, 2025, 5:25 PM PT
**For**: Agent Investigation (Code/Cursor with database access)
**Purpose**: Gather all data needed before creating migration gameplan
**Estimated Time**: 45-60 minutes

---

## Investigation Objectives

Determine current state of user tables and all dependencies to inform safe UUID migration strategy.

---

## Section 1: Table Structure Investigation

### 1.1 Current User Tables Schema

```sql
-- Get complete schema for both user tables
\d+ users
\d+ alpha_users

-- Check column types specifically
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name IN ('users', 'alpha_users')
ORDER BY table_name, ordinal_position;
```

**Document**:
- Exact column types for id fields
- All columns in each table
- Which columns exist in both vs unique to each
- Any constraints or indexes

### 1.2 Record Counts and ID Formats

```sql
-- Count records in each table
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'alpha_users', COUNT(*) FROM alpha_users;

-- Sample IDs from each table to see format
SELECT 'users' as table_name, id, username, created_at
FROM users
LIMIT 5
UNION ALL
SELECT 'alpha_users', id::text, username, created_at
FROM alpha_users
LIMIT 5;

-- Check for any UUID-format IDs already in users table
SELECT COUNT(*)
FROM users
WHERE id ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$';

-- Check for any non-UUID format IDs in alpha_users
SELECT COUNT(*)
FROM alpha_users
WHERE id::text !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$';
```

**Document**:
- How many users in each table
- Format of IDs (VARCHAR like "xian" vs proper UUID)
- Any anomalies or mixed formats

### 1.3 Relationship Between Tables

```sql
-- Check if alpha_users references users table
SELECT
    au.id as alpha_user_id,
    au.username as alpha_username,
    au.prod_user_id,
    u.id as users_id,
    u.username as users_username
FROM alpha_users au
LEFT JOIN users u ON au.prod_user_id = u.id
LIMIT 10;

-- Check for username conflicts
SELECT username, COUNT(*) as count
FROM (
    SELECT username FROM users
    UNION ALL
    SELECT username FROM alpha_users
) combined
GROUP BY username
HAVING COUNT(*) > 1;
```

**Document**:
- Is there a relationship between tables?
- Any username conflicts?
- Can we safely merge?

---

## Section 2: Foreign Key Dependencies

### 2.1 Find All Tables with FKs to User Tables

```sql
-- Find all foreign keys pointing to users table
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND ccu.table_name IN ('users', 'alpha_users')
ORDER BY tc.table_name;

-- Also check for columns that SHOULD be FKs but aren't constrained
SELECT DISTINCT table_name, column_name
FROM information_schema.columns
WHERE column_name IN ('user_id', 'created_by', 'updated_by', 'owner_id')
    AND table_name NOT IN ('users', 'alpha_users')
ORDER BY table_name, column_name;
```

**Document**:
- Complete list of tables with FK to users
- Complete list of tables with FK to alpha_users
- Any tables with user_id columns but no FK constraint

### 2.2 Check Each Dependent Table's ID Format

For each table found above with user_id columns:

```sql
-- Example for each dependent table (replace TABLE_NAME)
SELECT
    'TABLE_NAME' as table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT user_id) as unique_users,
    pg_typeof(user_id) as user_id_type
FROM TABLE_NAME
GROUP BY pg_typeof(user_id);

-- Check if any user_ids don't exist in parent table
SELECT COUNT(*) as orphaned_records
FROM TABLE_NAME t
LEFT JOIN users u ON t.user_id = u.id
WHERE u.id IS NULL AND t.user_id IS NOT NULL;
```

Run for each of these tables (based on Issue #262 description):
- conversations
- user_api_keys
- audit_logs
- token_blacklist
- feedback
- personality_profiles
- sessions (if has user_id)
- todos (if has user_id)

**Document**:
- Which tables have VARCHAR user_ids
- Which have UUID user_ids
- Any orphaned records (referencing non-existent users)

---

## Section 3: Application Code Investigation

### 3.1 Model Definitions

```bash
# Find all model files that reference User
grep -r "class User" --include="*.py" services/
grep -r "class AlphaUser" --include="*.py" services/

# Find the actual model definitions
cat services/database/models.py | grep -A 20 "class User"
cat services/database/models.py | grep -A 20 "class AlphaUser"
```

**Document**:
- How are User and AlphaUser models defined?
- What type hints are used for id field?
- Are they using relationship() to other models?

### 3.2 Service Layer Usage

```bash
# Find all user_id type hints
grep -r "user_id: str" --include="*.py" services/
grep -r "user_id: UUID" --include="*.py" services/
grep -r "user_id: int" --include="*.py" services/

# Find user lookups
grep -r "get_user\|find_user\|user_by_id" --include="*.py" services/ | head -20

# Check auth service specifically
grep -r "users\|alpha_users" services/auth/ --include="*.py"
```

**Document**:
- How many files assume user_id is string?
- How many assume UUID?
- Which services directly query user tables?

### 3.3 Critical Path Analysis

```bash
# Authentication flow
grep -r "login\|authenticate" services/auth/ --include="*.py" -A 5 -B 5 | grep -E "(users|alpha_users|user_id)"

# Session management
grep -r "session.*user_id\|user_id.*session" services/ --include="*.py" | head -10

# Token blacklist (since it's blocked by this)
cat services/database/models.py | grep -A 10 -B 10 "TokenBlacklist"
```

**Document**:
- Which table does auth currently use?
- How are sessions linked to users?
- Current TokenBlacklist model definition

---

## Section 4: Migration Risks and Constraints

### 4.1 Check for Hard-Coded User IDs

```bash
# Look for hardcoded string user IDs
grep -r '"xian"\|"test"\|"admin"' --include="*.py" services/ tests/

# Look for specific user checks
grep -r "user.*==.*['\"]" --include="*.py" services/ | head -20
```

**Document**:
- Any hardcoded user IDs that would break
- Any string comparisons that need updating

### 4.2 Database Constraints Check

```sql
-- Check all unique constraints on user tables
SELECT
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name IN ('users', 'alpha_users')
    AND tc.constraint_type IN ('UNIQUE', 'PRIMARY KEY');

-- Check for any triggers on user tables
SELECT * FROM information_schema.triggers
WHERE event_object_table IN ('users', 'alpha_users');
```

**Document**:
- Unique constraints (username, email)
- Any triggers that might complicate migration
- Primary key constraints

---

## Section 5: Rollback Planning Data

### 5.1 Backup Size Estimation

```sql
-- Estimate size for backup planning
SELECT
    pg_size_pretty(pg_table_size('users')) as users_table_size,
    pg_size_pretty(pg_table_size('alpha_users')) as alpha_users_size,
    pg_size_pretty(pg_database_size(current_database())) as total_db_size;

-- Transaction volume (to plan maintenance window)
SELECT
    date_trunc('hour', created_at) as hour,
    COUNT(*) as records_created
FROM users
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;
```

**Document**:
- Database sizes for backup planning
- Usage patterns (when is low-activity window?)

---

## Section 6: Special Considerations

### 6.1 Check Issue #263 Status (mentioned in #291)

```bash
# Was Issue #263 already completed?
git log --grep="#263" --oneline | head -5

# Check for any UUID migration attempts
git log --grep="UUID\|uuid" --oneline | head -10

# Check for migration files
ls -la alembic/versions/*uuid* 2>/dev/null || echo "No UUID migrations found"
ls -la migrations/*uuid* 2>/dev/null || echo "No UUID migrations found"
```

**Document**:
- Was #263 actually completed? (Lead Dev thinks yes)
- Any previous UUID migration attempts?
- Existing migration infrastructure?

### 6.2 Test Coverage Check

```bash
# Find tests that deal with users
find tests/ -name "*.py" -exec grep -l "user_id\|User\|AlphaUser" {} \; | head -20

# Check if we have migration tests
ls -la tests/*migrat* 2>/dev/null || echo "No migration tests found"
ls -la tests/database/*migrat* 2>/dev/null || echo "No migration tests found"
```

**Document**:
- Which tests will need updating
- Do we have migration test infrastructure?

---

## Output Format

Please compile findings in this format:

```markdown
# Investigation Results: Issue #262 UUID Migration

## Summary
- Users table has X records with VARCHAR IDs
- Alpha_users table has Y records with UUID IDs
- Z tables depend on user FKs
- Approximately N files need code changes

## Critical Findings
[Any blocking issues or concerns discovered]

## Table Details
[Detailed findings from Section 1]

## Foreign Key Dependencies
[Detailed findings from Section 2]

## Code Impact Analysis
[Detailed findings from Section 3]

## Risk Assessment
[Based on Sections 4-6]

## Recommendation
[Can we proceed with Option 1? Any modifications needed?]
```

---

## Time Estimate

- Section 1: 10 minutes (database queries)
- Section 2: 10 minutes (FK analysis)
- Section 3: 10 minutes (code analysis)
- Section 4: 5 minutes (risk check)
- Section 5: 5 minutes (rollback data)
- Section 6: 5 minutes (special checks)
- Compilation: 10-15 minutes

**Total: 45-60 minutes**

---

After receiving these results, Chief Architect will create comprehensive gameplan for the migration incorporating all findings.

---

*Investigation instructions complete - ready for agent execution*
