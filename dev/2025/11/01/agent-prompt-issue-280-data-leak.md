# Claude Code Prompt: CORE-ALPHA-DATA-LEAK (#280)

**Date**: November 1, 2025, 7:00 AM PT
**Mission**: Remove personal data from PIPER.md and migrate to user database
**Effort**: Small (2-3 hours)
**GitHub Issue**: #280

---

## Your Identity

You are Claude Code, a specialized development agent on the Piper Morgan project. You follow systematic methodology and provide filesystem evidence for all claims.

---

## CRITICAL FIRST ACTION: Use Serena MCP

**Before doing ANYTHING, use Serena to understand current state**:

```python
# Find and examine PIPER.md
serena.view_file("config/PIPER.md")

# Find configuration loading code
serena.find_symbol("ConfigService")
serena.find_referencing_symbols("PIPER.md")

# Check alpha_users table structure
serena.find_symbol("AlphaUser")
serena.find_symbol("preferences")
```

**Report what you find** before proceeding.

---

## Cathedral Context

**Read this gameplan section for full context**:
- `/mnt/user-data/uploads/gameplan-p0-alpha-blockers-v2.md` (Issue #1 section)

**The Problem**:
PIPER.md contains Christian's (xian's) personal production data that all alpha testers see. This is a critical privacy violation.

**The Solution**:
1. Audit PIPER.md for personal data
2. Extract personal data and save to temp file
3. Create generic PIPER.md with only system capabilities
4. Migrate xian's personal data to alpha_users.preferences (JSONB field)
5. Update ConfigService to load user-specific preferences
6. Test with multiple users

---

## Mission

Remove all personal/company data from `config/PIPER.md` and migrate Christian's data to the `alpha_users.preferences` field in the database, then update ConfigService to merge generic + user-specific configuration.

---

## Phase -1: Verify Infrastructure (15 minutes)

**Use Serena to check**:
1. Where is PIPER.md loaded?
2. Does alpha_users.preferences exist (JSONB field)?
3. Is there a ConfigService?
4. What services consume PIPER.md?

**Report findings with evidence** before proceeding.

---

## Implementation Plan

### Phase 0: Audit & Backup (30 minutes)

1. **Read current PIPER.md completely**
   ```bash
   cat config/PIPER.md
   ```

2. **Identify personal data** (look for):
   - Q4 goals, VA project, DRAGONS
   - Kind Systems, team size
   - Personal preferences, meetings
   - Any non-generic examples

3. **Create backup**:
   ```bash
   cp config/PIPER.md config/PIPER.md.backup-$(date +%Y%m%d)
   git add config/PIPER.md.backup-*
   git commit -m "BACKUP: PIPER.md before personal data extraction"
   ```

4. **Extract personal data**:
   ```bash
   # Save identified personal sections to file
   # This will be migrated to database
   cat > extracted_personal_data.md << 'EOF'
   [paste personal sections here]
   EOF
   ```

**Checkpoint**: Report what personal data you found with evidence.

### Phase 1: Create Generic PIPER.md (45 minutes)

**Create NEW PIPER.md with ONLY**:
- Generic capabilities (document analysis, integrations)
- Default personality traits
- Available integrations list
- System behaviors

**NO**:
- Personal examples
- Specific projects
- Individual preferences
- Company names
- Team structures

**Example structure** (adapt to actual content):
```markdown
# PIPER.md - Generic System Configuration

## Capabilities
- Document analysis and summarization
- Task management and tracking
- GitHub, Slack, Notion, Calendar integrations
[etc - generic only]

## Default Personality
- Professional and friendly
- Concise but thorough
[etc - generic only]
```

**Evidence Required**:
```bash
# Show new file has no personal data
grep -i "Q4\|VA\|DRAGONS\|Kind Systems" config/PIPER.md
# Expected: No matches

# Show generic content
cat config/PIPER.md
```

### Phase 2: Database Migration Script (45 minutes)

**Create `scripts/migrate_personal_data_to_xian.py`**:

```python
"""
One-time migration: Move Christian's personal data
from PIPER.md to alpha_users.preferences
"""
import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Import your database session and model
# Adapt imports based on what Serena shows you
from database import get_db_session
from models.user import AlphaUser  # or wherever AlphaUser is defined

async def migrate_personal_data():
    """Move xian's personal data to database"""

    async with get_db_session() as db:
        # Get xian's user record
        result = await db.execute(
            select(AlphaUser).where(AlphaUser.username == 'xian')
        )
        user = result.scalar_one_or_none()

        if not user:
            print("ERROR: User 'xian' not found in alpha_users")
            print("Available users:")
            all_users = await db.execute(select(AlphaUser))
            for u in all_users.scalars():
                print(f"  - {u.username}")
            return

        # Personal context extracted from PIPER.md
        personal_context = {
            "projects": [
                # Add projects you found in PIPER.md
            ],
            "preferences": {
                # Add preferences you found
            },
            "q4_goals": [
                # Add goals you found
            ],
            # etc - based on what you extracted
        }

        # Merge with existing preferences
        current_prefs = user.preferences or {}
        updated_prefs = {**current_prefs, **personal_context}

        # Update user record
        user.preferences = updated_prefs
        await db.commit()

        print(f"✅ Personal data migrated for user 'xian'")
        print(f"   User ID: {user.id}")
        print(f"   Preferences keys: {list(personal_context.keys())}")

        return str(user.id)

if __name__ == "__main__":
    result = asyncio.run(migrate_personal_data())
    print(f"\nMigration complete. User ID: {result}")
```

**Run it**:
```bash
python scripts/migrate_personal_data_to_xian.py
```

**Evidence Required**: Show script output proving data was stored.

### Phase 3: Update ConfigService (45 minutes)

**Find and modify ConfigService** (use Serena to locate):

```python
# Modify ConfigService to support user overlay
class ConfigService:
    def __init__(self, db_session):
        self.db = db_session
        self._piper_md_cache = None

    async def load_config(
        self,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Load configuration with user overlay.
        Generic PIPER.md + user preferences from database.
        """
        # 1. Load generic PIPER.md
        base_config = self._load_piper_md()

        # 2. If no user, return generic
        if not user_id:
            return base_config

        # 3. Load user preferences from database
        user_prefs = await self._load_user_preferences(user_id)

        # 4. Merge (user overrides base)
        return self._merge_configs(base_config, user_prefs)

    def _load_piper_md(self) -> Dict[str, Any]:
        """Load generic PIPER.md (cached)"""
        if self._piper_md_cache:
            return self._piper_md_cache

        with open('config/PIPER.md', 'r') as f:
            content = f.read()

        # Parse into dict structure
        config = self._parse_markdown(content)
        self._piper_md_cache = config
        return config

    async def _load_user_preferences(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """Load user preferences from alpha_users"""
        from sqlalchemy import select
        from models.user import AlphaUser

        result = await self.db.execute(
            select(AlphaUser).where(AlphaUser.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user or not user.preferences:
            return {}

        return user.preferences

    def _merge_configs(
        self,
        base: Dict,
        user: Dict
    ) -> Dict:
        """Merge user preferences over base"""
        merged = base.copy()
        for key, value in user.items():
            if isinstance(value, dict) and key in merged:
                merged[key] = {**merged.get(key, {}), **value}
            else:
                merged[key] = value
        return merged
```

**Evidence Required**: Show file modifications with line numbers.

---

## Verification & Testing (30 minutes)

### Test 1: Check PIPER.md has no personal data
```bash
grep -i "christian\|xian\|VA\|DRAGONS\|Q4\|Kind Systems" config/PIPER.md
# Expected: No matches (exit code 1)
```

### Test 2: Verify xian's data in database
```python
# Quick verification script
python -c "
import asyncio
from sqlalchemy import select
from database import get_db_session
from models.user import AlphaUser

async def check():
    async with get_db_session() as db:
        result = await db.execute(
            select(AlphaUser).where(AlphaUser.username == 'xian')
        )
        user = result.scalar_one()
        print(f'User: {user.username}')
        print(f'Preferences keys: {list((user.preferences or {}).keys())}')
        print(f'Has personal data: {bool(user.preferences)}')

asyncio.run(check())
"
```

### Test 3: ConfigService loads correctly
```python
# Test config loading
python -c "
import asyncio
from services.config.config_service import ConfigService
from database import get_db_session

async def test():
    async with get_db_session() as db:
        cs = ConfigService(db)

        # Generic config (no user)
        generic = await cs.load_config()
        print('Generic config keys:', list(generic.keys()))

        # User config (with xian's data)
        # Get xian's user_id first
        from sqlalchemy import select
        from models.user import AlphaUser
        result = await db.execute(
            select(AlphaUser).where(AlphaUser.username == 'xian')
        )
        user = result.scalar_one()

        user_config = await cs.load_config(user_id=str(user.id))
        print('User config has personal data:', 'projects' in user_config)

asyncio.run(test())
"
```

**Expected**:
- Generic config: Only system capabilities
- User config: Includes personal projects/preferences

---

## Success Criteria

**Check all before claiming complete**:
- [ ] PIPER.md contains zero personal/company data
- [ ] Generic capabilities clearly documented in PIPER.md
- [ ] Christian's personal data in alpha_users.preferences (JSONB)
- [ ] Migration script runs successfully
- [ ] ConfigService loads user-specific data correctly
- [ ] Tests pass showing data isolation
- [ ] No personal data leaks to other users
- [ ] All changes committed to git with descriptive messages

---

## Evidence Format

**For completion, provide**:

1. **Files Modified**:
   ```
   config/PIPER.md: New content (X lines)
   scripts/migrate_personal_data_to_xian.py: Created (Y lines)
   services/config/config_service.py: Modified (Z lines changed)
   ```

2. **Terminal Outputs**:
   - Backup creation: `git log --oneline -1`
   - Personal data check: `grep` output showing no matches
   - Migration script: Full output
   - Test results: All 3 tests passing

3. **Database Verification**:
   - Query showing xian's preferences field populated

4. **Git Status**:
   ```bash
   git status
   git log --oneline -3
   ```

---

## Time Lord Reminder

No deadlines. Take the time needed for complete, verified work. Quality > speed.

If you find issues or discrepancies, STOP and report. Don't guess or assume.

---

## Questions for PM (if needed)

- If PIPER.md structure is different than expected
- If alpha_users.preferences doesn't exist
- If ConfigService doesn't exist or is structured differently
- If you need clarification on what counts as "personal data"

**Ask before assuming!**

---

Good luck! This is a straightforward but important security fix. The foundation is there, you're just cleaning up the data exposure.
