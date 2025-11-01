# Alpha Database Architecture

**Issue**: #280 CORE-ALPHA-DATA-LEAK
**Date**: November 1, 2025
**Status**: Active Architecture

---

## The Fundamental Principle: Code vs Data Separation

### Code (In Git Repositories)
- **Location**: Git branches (main, production)
- **Contents**: Python files, SQL schemas, migration scripts, config templates
- **Shared**: YES - all developers and testers pull the same code
- **Versioned**: YES - tracked in git history
- **Examples**:
  - `services/database/models.py` (defines `alpha_users` table schema)
  - `scripts/migrate_personal_data.py` (migration script)
  - `config/PIPER.md` (generic system config template)

### Data (In PostgreSQL Databases)
- **Location**: Local PostgreSQL instance on each machine
- **Contents**: Actual user records, preferences, uploaded files, session data
- **Shared**: NO - each environment has separate database
- **Versioned**: NO - not in git (in .gitignore)
- **Examples**:
  - Alpha user 'xian' with Christian's personal data
  - Alpha user 'alfy' with generic/test data
  - Uploaded files, conversation history

---

## Key Insight: Databases NEVER Merge

```
┌──────────────────────────────────────────────────────┐
│ GIT REPOSITORY (Code Only - Shared)                  │
├──────────────────────────────────────────────────────┤
│                                                       │
│  main branch:       Active development (PM's work)   │
│  production branch: Stable code for alpha testers    │
│                                                       │
│  Contains: Python files, schemas, scripts            │
│  Does NOT contain: User data, preferences, uploads   │
│                                                       │
└──────────────────────────────────────────────────────┘
                        ↓ git pull/clone
                        ↓
┌──────────────────────────────────────────────────────┐
│ LOCAL ENVIRONMENTS (Code + Data - Separate)          │
├──────────────────────────────────────────────────────┤
│                                                       │
│ [Dev Laptop - xian]                                  │
│   Code: main branch (latest development)             │
│   PostgreSQL DB #1:                                  │
│     - alpha_users table                              │
│     - Row: username='xian', preferences={Christian}  │
│                                                       │
│ [Test Laptop - xian]                                 │
│   Code: production branch (stable releases)          │
│   PostgreSQL DB #2:                                  │
│     - alpha_users table                              │
│     - Row: username='alfy', preferences={}           │
│                                                       │
│ [External Tester - future]                           │
│   Code: production branch (stable releases)          │
│   PostgreSQL DB #3:                                  │
│     - alpha_users table                              │
│     - Row: username='tester123', preferences={...}   │
│                                                       │
└──────────────────────────────────────────────────────┘

DATABASE #1 ≠ DATABASE #2 ≠ DATABASE #3

These databases NEVER merge. Each is independent.
```

---

## Branch Strategy

### `main` Branch
- **Purpose**: Active development by PM (Christian)
- **Stability**: May have experimental features
- **Who uses**: PM only
- **Database**: PM's dev laptop PostgreSQL with 'xian' user
- **Merge target**: Merged TO `production` when features are stable

### `production` Branch
- **Purpose**: Stable releases for alpha testers
- **Stability**: Tested, documented, ready for external use
- **Who uses**: All alpha testers (alfy, future testers)
- **Database**: Each tester's LOCAL PostgreSQL with their own user
- **Merge target**: Receives merges FROM `main` when PM declares release

**Important**: Branches contain CODE, not DATA. Both branches have the same `alpha_users` table definition, but each tester's database has different rows.

---

## User Data Architecture

### Alpha Phase (Current)

**Personal Data Storage**:
- **Where**: `alpha_users.preferences` JSONB field
- **Who**: Each alpha user has their own row in their LOCAL database
- **Access**: User-specific (xian sees xian's data, alfy sees alfy's data)
- **Migration**: Per-user via `scripts/migrate_personal_data.py`

**Generic System Config**:
- **Where**: `config/PIPER.md` file (in git)
- **Who**: ALL users (shared template)
- **Access**: Generic capabilities only, NO personal data
- **Purpose**: System features, default personality, integration list

**How It Works**:
1. User logs in → system identifies user_id
2. Load generic `PIPER.md` (shared template)
3. Load user preferences from `alpha_users.preferences` (user-specific)
4. Merge: user preferences override generic config
5. Result: Personalized experience with data isolation

### MVP/Production Phase (Future)

**Production Database**:
- **Where**: Hosted database (Render, Railway, Supabase, etc.)
- **Who**: ALL production users in ONE shared database
- **Tables**:
  - `users` table (production users)
  - `alpha_users` table (may be deprecated or merged)
- **Access**: Multi-tenant with row-level security

**Migration Path** (Alpha → Production):
1. Export alpha user's preferences: `SELECT preferences FROM alpha_users WHERE username='alfy'`
2. Create production user: `INSERT INTO users (username, email, preferences) VALUES (...)`
3. User can now log into production with their migrated data
4. This is MANUAL per user (no automatic merge)

---

## Database Migration Scripts

### `scripts/migrate_personal_data.py`

**Purpose**: Migrate user data from old PIPER.md to database

**Usage**:
```bash
# Migrate Christian's data to 'xian' user (default)
python scripts/migrate_personal_data.py --username xian

# Verify alfy user exists (no data migration)
python scripts/migrate_personal_data.py --username alfy --skip-migration

# Migrate custom data from JSON file
python scripts/migrate_personal_data.py --username tester123 --data-file tester_data.json
```

**What It Does**:
- Finds user in `alpha_users` table (local database only)
- Loads personal data (default Christian data OR custom JSON file)
- Stores in `alpha_users.preferences` JSONB field
- Verifies migration completed successfully

**What It Does NOT Do**:
- Modify git repository
- Merge databases across machines
- Share data between users

---

## Common Questions

### Q: "Are alpha users in the database on main or production?"

**A**: This is a category error. Alpha users are in LOCAL DATABASES (one per machine), not in GIT BRANCHES.

- The `alpha_users` table SCHEMA is in both `main` and `production` branches (code)
- The `alpha_users` table ROWS are in each machine's PostgreSQL (data)
- Dev laptop DB has row: `xian`
- Test laptop DB has row: `alfy`
- These are different databases, never merged

### Q: "How do I share my database with other developers?"

**A**: You don't. Each developer/tester creates their own local database with their own users.

**Correct approach**:
1. Tester clones repo from `production` branch (gets code)
2. Tester runs `docker-compose up -d` (creates LOCAL database)
3. Tester runs setup wizard (creates THEIR user in THEIR database)
4. Tester optionally runs migration (adds THEIR personal data)

### Q: "When I push code, do my database changes get pushed too?"

**A**: No. Only code is pushed to git. Database data stays local.

**What gets pushed**:
- ✅ Migration scripts (`scripts/migrate_personal_data.py`)
- ✅ Model schemas (`services/database/models.py`)
- ✅ Generic config (`config/PIPER.md`)

**What does NOT get pushed**:
- ❌ User records (`alpha_users` table rows)
- ❌ Personal preferences (JSONB data)
- ❌ Uploaded files
- ❌ Conversation history

### Q: "How do alpha testers get production data later?"

**A**: Manual export/import per user when they want to migrate.

**Process** (when we deploy to production):
1. Set up production database (ONE shared database on server)
2. For each alpha user who wants to migrate:
   - Export: `SELECT preferences FROM alpha_users WHERE username='alfy'`
   - Import: `INSERT INTO users (username, preferences) VALUES ('alfy', exported_prefs)`
3. User logs into production system with new credentials
4. Their personal data (preferences) is now in production

---

## Security Considerations

### Alpha Phase
- ✅ Data isolation: Each user sees only their data
- ✅ Local databases: No shared production data
- ⚠️ No encryption: Alpha data on local disk (encrypted at OS level)
- ⚠️ No email verification: Users created manually via wizard
- ⚠️ No password reset: Manual process for alpha

### MVP/Production Phase (Future)
- 🔐 Multi-tenant database with row-level security
- 🔐 Encrypted connections (SSL/TLS)
- 🔐 Email verification required
- 🔐 Password reset via email service (SendGrid, Mailgun)
- 🔐 Rate limiting to prevent spam
- 🔐 API authentication (JWT tokens)

**Email Backend Security**:
- Use reputable email service (SendGrid, Mailgun, AWS SES)
- Implement rate limiting (max 5 emails/hour per user)
- Require email verification before allowing sends
- Monitor for spam patterns
- Implement captcha for signup
- NOT a blocker for alpha (alpha uses manual password reset)

---

## File Organization

### What's in Git
```
config/
  PIPER.md                      # Generic system config (NO personal data)
  PIPER.md.backup-20251101      # Backup of old personal data

scripts/
  migrate_personal_data.py      # Migration tool (flexible username)
  create_test_alpha_user.py     # User creation utility

services/database/
  models.py                     # Table schemas (AlphaUser, User, etc.)
  connection.py                 # Database connection logic

docs/
  ALPHA_DATABASE_ARCHITECTURE.md  # This file
```

### What's NOT in Git (.gitignore)
```
postgres_data/      # PostgreSQL data directory
*.db                # SQLite files (if used)
.env                # Environment variables (DB passwords, etc.)
uploads/            # User-uploaded files
```

---

## Next Steps

### For Alpha Phase
1. ✅ Generic PIPER.md created (no personal data)
2. ✅ Migration script supports flexible usernames
3. ✅ UserContextService loads user-specific preferences
4. ✅ Data isolation verified (tests passing)
5. ⏭️ External alpha testers onboard with their own users
6. ⏭️ Each tester's data stays in their local database

### For MVP/Production Phase
1. Deploy production database (Render, Railway, Supabase)
2. Implement user authentication (JWT tokens)
3. Add email service for verification/password reset
4. Migrate alpha users who want to continue (manual export/import)
5. Implement rate limiting and security measures
6. Set up monitoring and backups

---

## Summary

**Key Takeaways**:
1. **Code** (in git) ≠ **Data** (in PostgreSQL)
2. Each environment has its own LOCAL database
3. Databases NEVER merge across machines
4. `main` branch and `production` branch contain same SCHEMA but different machines have different DATA
5. User data lives in `alpha_users.preferences` JSONB field
6. Generic system config lives in `config/PIPER.md` (shared)
7. Migration to production is manual per user when ready

**Mental Model**:
- Think of git branches as "templates" (code)
- Think of databases as "filled-in forms" (data)
- Everyone uses the same template (code from git)
- But everyone fills in their own form (data in their database)

---

**Last Updated**: November 1, 2025, 8:10 AM
**Maintained By**: PM (Christian)
**Related Issues**: #280 (CORE-ALPHA-DATA-LEAK)
