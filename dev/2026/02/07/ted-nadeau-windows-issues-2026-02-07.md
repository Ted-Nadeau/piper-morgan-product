# GitHub Issues: Windows Setup Bugs from Ted Nadeau

**Source**: Ted Nadeau's E1-E30 bug report (Feb 4-6, 2026)
**Extracted by**: HOSR session, Feb 7, 2026
**For**: Lead Developer to create as GitHub issues

---

## Instructions for Agent

Create each issue below as a GitHub issue in the piper-morgan-product repository. Use the provided title, labels, and body. Link related issues where noted.

---

## BLOCKER PRIORITY

### Issue 1: uvloop Windows Incompatibility

**Title**: `[SETUP] uvloop fails to install on Windows - use PEP 508 environment markers`

**Labels**: `bug`, `setup`, `windows`, `blocker`

**Body**:
```markdown
## Problem

`uvloop==0.21.0` fails to install on Windows with error:
```
RuntimeError: uvloop does not support Windows at the moment
```

This blocks all Windows users from completing `pip install -r requirements.txt`.

## Source

Ted Nadeau Windows setup attempt (E3, E5)

## Proposed Fix

Use PEP 508 environment markers in requirements.txt:

```
# Only install on non-Windows
uvloop==0.21.0; sys_platform != 'win32'
```

## Acceptance Criteria

- [ ] requirements.txt updated with platform marker
- [ ] Windows user can complete `pip install -r requirements.txt`
- [ ] Linux/Mac installs still get uvloop
```

---

### Issue 2: Migration Fails on Missing 'features' Table

**Title**: `[DB] Migration 70847a6596f3 fails - 'features' table does not exist`

**Labels**: `bug`, `database`, `migration`, `blocker`

**Body**:
```markdown
## Problem

Running `alembic upgrade head` fails at migration `70847a6596f3_add_lifecycle_state_to_mux_objects_` with:

```
psycopg2.errors.UndefinedTable: relation "features" does not exist
[SQL: ALTER TABLE features ADD COLUMN lifecycle_state VARCHAR(50)]
```

## Context

This occurs on a fresh database after running all prior migrations successfully. The migration assumes `features` table exists, but no prior migration creates it.

## Source

Ted Nadeau Windows setup attempt (E25, E26)

## Investigation Needed

1. Which migration should create `features` table?
2. Is there a missing migration file?
3. Is the migration order incorrect?

## Acceptance Criteria

- [ ] Root cause identified
- [ ] Migration chain fixed so `alembic upgrade head` completes on fresh DB
- [ ] Verified on both Mac and Windows
```

---

## HIGH PRIORITY

### Issue 3: Windows Line Endings Cause Docker Launch Failure

**Title**: `[SETUP] Windows CRLF line endings break Docker container startup`

**Labels**: `bug`, `setup`, `windows`, `docker`

**Body**:
```markdown
## Problem

`piper-app` and `piper-orchestration` containers fail to start on Windows due to CRLF vs LF line ending differences in shell scripts.

## Workaround

Stop all containers and restart the process (time-consuming).

## Source

Ted Nadeau Windows setup attempt (E15)

## Proposed Fix

Add `.gitattributes` to enforce LF line endings for all shell scripts:

```
*.sh text eol=lf
entrypoint.sh text eol=lf
```

## Acceptance Criteria

- [ ] `.gitattributes` added with shell script rules
- [ ] Existing shell scripts converted to LF
- [ ] Docker containers start successfully on Windows after fresh clone
```

---

### Issue 4: Schema Drift - 6 Mismatches Between Models and Database

**Title**: `[DB] Schema validation reports 6 mismatches - DateTime vs timestamptz and missing table`

**Labels**: `bug`, `database`, `schema`

**Body**:
```markdown
## Problem

Schema validation (Issue #484) reports 6 mismatches:

| Location | Model | Database | Issue |
|----------|-------|----------|-------|
| `features.created_at` | DateTime | timestamptz | Type mismatch |
| `features.updated_at` | DateTime | timestamptz | Type mismatch |
| `knowledge_nodes.embedding_vector` | JSON | _float8 | Type mismatch |
| `todo_lists` | (table) | (missing) | Critical - table not found |
| `conversational_memory_entries.timestamp` | DateTime | timestamptz | Type mismatch |
| `conversational_memory_entries.created_at` | DateTime | timestamptz | Type mismatch |

## Source

Ted Nadeau Windows setup attempt (E29)

## Impact

> ⚠️ WARNING: Schema drift detected!
> Database may not match models. Check logs for details.
> This could cause runtime errors.

## Acceptance Criteria

- [ ] Investigate DateTime vs timestamptz mismatches (may be acceptable)
- [ ] Create `todo_lists` table or remove from model
- [ ] Investigate `knowledge_nodes.embedding_vector` type
- [ ] Schema validation passes clean
```

---

### Issue 5: Account Creation Fails in Setup Wizard

**Title**: `[SETUP] Account creation fails with generic error in web setup wizard`

**Labels**: `bug`, `setup`, `auth`, `needs-investigation`

**Body**:
```markdown
## Problem

In the web setup wizard at `http://127.0.0.1:8001/setup`, Step 3 (Account Creation) fails with:

> Account Creation Failed - failed to create account

No additional error details shown to user.

## Context

- Step 1 (System): All green ✓
- Step 2 (API Keys): Configured (with some issues, see separate issue)
- Step 3 (Account): ❌ Fails
- Cannot navigate back to previous steps after failure

## Source

Ted Nadeau Windows setup attempt (Feb 6 email)

## Investigation Needed

1. Check server logs for actual error
2. May be related to migration/schema issues (features table, schema drift)
3. May be database connection issue

## Acceptance Criteria

- [ ] Root cause identified
- [ ] Clear error message shown to user
- [ ] Account creation succeeds on fresh setup
- [ ] Add "Back" navigation to setup wizard
```

---

## MEDIUM PRIORITY

### Issue 6: Documentation Uses Wrong docker-compose Command

**Title**: `[DOCS] Update docker-compose to docker compose (modern syntax)`

**Labels**: `documentation`, `setup`, `docker`

**Body**:
```markdown
## Problem

Documentation uses `docker-compose` (with hyphen) but modern Docker Desktop uses `docker compose` (space, no hyphen).

```
# Old (deprecated)
docker-compose up -d

# New (current)
docker compose up -d
```

## Source

Ted Nadeau Windows setup attempt (E8, E9)

## Files to Update

- README.md
- docs/setup.md
- ALPHA_QUICKSTART.md
- Any other setup documentation

## Acceptance Criteria

- [ ] All docs use `docker compose` syntax
- [ ] Verified commands work on current Docker Desktop
```

---

### Issue 7: Quick Start Time Estimates Are Inaccurate

**Title**: `[DOCS] Quick Start claims 30 seconds but takes 4+ hours - improve time estimates`

**Labels**: `documentation`, `setup`, `ux`

**Body**:
```markdown
## Problem

Quick Start documentation claims "30 seconds" but actual time for Ted was ~4 hours over 2 days. This sets incorrect expectations and causes frustration.

## Source

Ted Nadeau Windows setup attempt (E10)

## Proposed Improvements

1. **Time estimates per step**:
   - `pip install`: ~5-10 minutes (216 packages)
   - `docker compose up -d`: ~20-60 minutes (first run, downloads ~4GB)
   - `docker compose build orchestration`: ~20 minutes
   - `alembic upgrade head`: ~1-2 minutes

2. **Progress indicators**:
   - Show package count during pip install
   - Show download progress during docker pull

3. **Storage requirements**:
   - Docker images: ~4GB
   - Python packages: ~1GB
   - Database: varies

4. **Explain WHY** each dependency is needed

5. **Add validation** after each step

## Acceptance Criteria

- [ ] Realistic time estimates in documentation
- [ ] Storage requirements documented
- [ ] Each major step explains its purpose
```

---

### Issue 8: Differentiate "Run" vs "Develop" Setup Paths

**Title**: `[DOCS] Create separate setup paths for running vs developing Piper Morgan`

**Labels**: `documentation`, `setup`, `dx`

**Body**:
```markdown
## Problem

Current setup documentation doesn't distinguish between:
- **Running** Piper Morgan (should be minimal)
- **Developing** Piper Morgan (full dev environment)

A user just wanting to try Piper shouldn't need the full dev stack.

## Source

Ted Nadeau Windows setup attempt (E12)

## Proposed Structure

```
## Quick Start (Users)
Minimal setup to run Piper Morgan
- Docker only
- Pre-built images
- ~5 minutes

## Developer Setup
Full development environment
- Python venv
- All dependencies
- Database migrations
- ~30 minutes
```

## Acceptance Criteria

- [ ] Two distinct setup paths documented
- [ ] User path is significantly simpler
- [ ] Developer path is complete and accurate
```

---

### Issue 9: Document venv Activation Requirement for main.py

**Title**: `[DOCS] Clarify that main.py must run inside activated virtual environment`

**Labels**: `documentation`, `setup`

**Body**:
```markdown
## Problem

It's unclear that `python main.py` must be run inside an activated virtual environment. Users who restart their terminal lose the venv activation.

## Source

Ted Nadeau Windows setup attempt (E19)

## Proposed Fix

Add explicit reminder before `python main.py`:

```bash
# Make sure your virtual environment is activated!
# Windows:
venv\Scripts\Activate.ps1

# Mac/Linux:
source venv/bin/activate

# Then run:
python main.py
```

## Acceptance Criteria

- [ ] Documentation clearly shows venv activation before main.py
- [ ] Both Windows and Mac/Linux commands shown
```

---

### Issue 10: localhost vs 127.0.0.1 Resolution on Windows

**Title**: `[SETUP] localhost:8001 doesn't work on Windows, 127.0.0.1:8001 does`

**Labels**: `bug`, `setup`, `windows`, `networking`

**Body**:
```markdown
## Problem

On Windows, navigating to `http://localhost:8001` doesn't work, but `http://127.0.0.1:8001` does work.

## Source

Ted Nadeau Windows setup attempt (E30)

## Investigation Needed

1. Docker networking configuration on Windows
2. Windows hosts file configuration
3. IPv4 vs IPv6 resolution

## Workaround

Use `http://127.0.0.1:8001` instead of `localhost:8001`

## Acceptance Criteria

- [ ] Root cause identified
- [ ] Either fix the issue or document the workaround clearly
```

---

## LOW PRIORITY

### Issue 11: Add pip Upgrade to Setup Instructions

**Title**: `[DOCS] Add pip upgrade step before installing requirements`

**Labels**: `documentation`, `setup`

**Body**:
```markdown
## Problem

pip may be outdated, causing warnings or compatibility issues.

```
[notice] A new release of pip is available: 24.0 -> 26.0
```

## Source

Ted Nadeau Windows setup attempt (E4)

## Proposed Fix

Add to setup instructions:

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

## Acceptance Criteria

- [ ] pip upgrade added to setup documentation
```

---

### Issue 12: Add Installation Validation/Smoke Test

**Title**: `[SETUP] Create smoke test script to validate successful installation`

**Labels**: `enhancement`, `setup`, `testing`

**Body**:
```markdown
## Problem

After completing setup, there's no quick way to validate everything is working correctly.

## Source

Ted Nadeau Windows setup attempt (E7, E27)

## Proposed Solution

Create `scripts/validate_install.py` or similar that:

1. Checks all Docker containers are running
2. Verifies database connection
3. Confirms API responds at /health
4. Validates required environment variables
5. Reports clear pass/fail status

## Usage

```bash
python scripts/validate_install.py
```

Output:
```
✓ Docker containers: 7/7 running
✓ Database: connected
✓ API health: OK
✓ Environment: all required vars set
✅ Installation validated successfully!
```

## Acceptance Criteria

- [ ] Validation script created
- [ ] Checks all critical components
- [ ] Clear pass/fail output
- [ ] Added to setup documentation
```

---

### Issue 13: Document PostgreSQL Database Browsing for Developers

**Title**: `[DOCS] Add instructions for browsing PostgreSQL database directly`

**Labels**: `documentation`, `dx`

**Body**:
```markdown
## Problem

Developers should be able to browse the PostgreSQL database directly for debugging, but connection details aren't documented.

## Source

Ted Nadeau Windows setup attempt (E28)

## Proposed Content

Add to developer documentation:

```
## Database Access

PostgreSQL is available at:
- Host: localhost
- Port: 5433
- Database: piper_morgan
- User: (from .env)
- Password: (from .env)

### GUI Tools

**pgAdmin** (recommended):
1. Download from https://www.pgadmin.org/
2. Add server with above credentials

**DBeaver** (alternative):
1. Download from https://dbeaver.io/
2. Create PostgreSQL connection
```

## Acceptance Criteria

- [ ] Connection details documented
- [ ] At least one GUI tool recommended
- [ ] Credentials location clarified
```

---

### Issue 14: Improve Error Messages with Remediation Guidance

**Title**: `[UX] Error messages should include interpretation and fix suggestions`

**Labels**: `enhancement`, `ux`, `dx`

**Body**:
```markdown
## Problem

Error messages show raw output without interpretation or remediation steps, leaving users unsure how to proceed.

## Source

Ted Nadeau Windows setup attempt (E17)

## Proposed Pattern

```
Before:
  ERROR: relation "features" does not exist

After:
  ERROR: relation "features" does not exist

  What this means: The database is missing a required table.

  How to fix:
  1. Run: alembic upgrade head
  2. If that fails, see: docs/troubleshooting.md#missing-tables
```

## Acceptance Criteria

- [ ] Critical error paths identified
- [ ] Each includes interpretation and fix suggestion
- [ ] Links to relevant documentation where appropriate
```

---

## Summary

| Priority | Count | Issue Numbers |
|----------|-------|---------------|
| BLOCKER | 2 | #1 (uvloop), #2 (features table) |
| HIGH | 3 | #3 (line endings), #4 (schema drift), #5 (account creation) |
| MEDIUM | 5 | #6-10 |
| LOW | 4 | #11-14 |

**Total: 14 issues**

---

*Extracted from Ted Nadeau's bug report by HOSR, Feb 7, 2026*
