# Sprint A7 Gameplan: Polish & Buffer (REVISED)

**Sprint**: A7 (Final Alpha Sprint)
**Theme**: "Alpha Polish & User Architecture"
**Duration**: 1 day estimated (based on 88% velocity pattern + Chief Architect guidance)
**Context**: Final sprint before Alpha Wave 2 launch
**Revision**: v2.0 - Updated with Chief Architect's execution order (Oct 22, 5:40 PM)

---

## Executive Summary

Sprint A7 delivers the final polish and infrastructure needed for Alpha launch. This includes critical security fixes, user architecture separation, UX enhancements, API key management improvements, and conversational preference gathering.

**Key Change**: Chief Architect recommended executing **Critical Fixes FIRST** to unblock other work, followed by CORE-USER as foundation for multi-user testing.

Based on Sprint A6's 88% faster pattern, the 12 issues should complete in 1 day (~5 hours actual).

---

## Sprint Goals

1. **Fix critical security TODOs** (boundary enforcement, JWT injection) - **FIRST**
2. **Separate Alpha from Production users** (clean data isolation) - **SECOND**
3. **Polish UX** for Alpha users (quiet mode, status detection, auto-browser) - **THIRD**
4. **Enhance API key management** (rotation reminders, validation, analytics) - **FOURTH**
5. **Enable conversational preferences** (complete Piper Education) - **LAST**

---

## Chief Architect's Guidance

### Key Architectural Decisions

**1. User Table Architecture**: ✅ SEPARATE TABLE
```sql
CREATE TABLE alpha_users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    migration_status VARCHAR(20) DEFAULT 'active',
    migration_date TIMESTAMP NULL,
    prod_user_id UUID REFERENCES users(id) NULL,
    preferences JSONB DEFAULT '{}'::jsonb
);
```
**Rationale**: Clean isolation, prevents test data contamination, user control

**2. Execution Order**: ✅ CRITICAL FIXES FIRST
- Unblocks other work
- Better dependency management
- Security-first approach

**3. xian Migration**: ✅ KEEP IT SIMPLE
- Move config → database
- Create proper user_id
- Archive legacy config (don't delete)

**4. Database Strategy**: ✅ LIGHTWEIGHT ALEMBIC
- One migration for alpha_users
- JSONB for preferences (flexibility)
- Don't over-engineer - this is alpha

**5. Testing Priorities**: ✅ FOCUSED
- Multi-user isolation
- Boundary enforcement
- JWT with proper DI
- Key rotation logic

---

## Issue Breakdown (12 Total)

**EXECUTION ORDER** (Chief Architect guidance):
1. Critical Fixes → 2. CORE-USER → 3. CORE-UX → 4. CORE-KEYS → 5. CORE-PREF

---

### Group 1: Critical Fixes (2 issues, ~45 min actual) ⭐ **EXECUTE FIRST**

**Rationale**: These unblock other work and fix security TODOs

**#257: CORE-KNOW-BOUNDARY-COMPLETE** - Complete BoundaryEnforcer Integration
- Fix 5 TODOs in knowledge_graph_service.py
- Wire boundary checks into all queries
- **Why First**: Unblocks CORE-USER testing (multi-user isolation requires working boundaries)
- **Testing Priority**: Critical for alpha multi-user
- Estimated: 2-3h → Likely: 30 min

**#258: CORE-AUTH-CONTAINER** - Fix JWT Dependency Injection
- Fix 3 TODOs in auth services
- Create AuthContainer for proper DI
- **Why First**: Unblocks CORE-KEYS work (rotation/validation needs proper auth)
- **Testing Priority**: Critical for JWT with DI
- Estimated: 1-2h → Likely: 15 min

---

### Group 2: CORE-USER (3 issues, ~1 hour actual) ⭐ **EXECUTE SECOND**

**Rationale**: Foundation for multi-user testing

**#259: CORE-USER-ALPHA-TABLE** - Create Alpha Users Table
```sql
-- Chief Architect's schema specification
CREATE TABLE alpha_users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    migration_status VARCHAR(20) DEFAULT 'active',  -- 'active', 'migrated', 'declined'
    migration_date TIMESTAMP NULL,
    prod_user_id UUID REFERENCES users(id) NULL,
    preferences JSONB DEFAULT '{}'::jsonb,  -- Flexibility during alpha
    CONSTRAINT valid_migration_status CHECK (migration_status IN ('active', 'migrated', 'declined'))
);

-- Indexes for common queries
CREATE INDEX idx_alpha_users_migration_status ON alpha_users(migration_status);
CREATE INDEX idx_alpha_users_prod_user ON alpha_users(prod_user_id) WHERE prod_user_id IS NOT NULL;
```

**Implementation Notes**:
- **Chief's Decision**: Separate table for clean isolation (not single table with flags)
- Use Alembic for migration: `alembic revision -m "create_alpha_users_table"`
- JSONB preferences provide flexibility during alpha
- **Why Second**: Foundation for all multi-user work

**Testing**:
- Verify alpha_users can be created
- Verify isolation from users table
- Verify JSONB preferences work

Estimated: 1-2h → Likely: 20 min

---

**#260: CORE-USER-MIGRATION** - Alpha→Production Migration Tool

**CLI Implementation**:
```bash
# New CLI command
python main.py migrate-user <alpha_user_id> [--preview] [--dry-run]

# Examples:
python main.py migrate-user abc-123 --preview  # Show what would migrate
python main.py migrate-user abc-123            # Execute migration
```

**Migration Scope** (lift and shift all data):
1. ✅ User record (alpha_users → users)
2. ✅ API keys (preserve OS keychain references)
3. ✅ Conversations/messages
4. ✅ Knowledge graph (nodes + edges + embeddings)
5. ✅ Audit logs (preserve security trail)
6. ✅ Preferences (JSONB → structured preferences)
7. ✅ Integration connections

**Implementation Notes**:
- Preview mode shows what will migrate (no changes)
- Dry-run mode simulates migration (rollback at end)
- Track migration in audit logs
- Update migration_status in alpha_users table
- **Chief's Guidance**: Keep it lightweight, don't over-engineer

**Testing**:
- Preview mode works without side effects
- Migration preserves all relationships
- Rollback works if migration fails
- Audit trail captures migration

Estimated: 2-3h → Likely: 20 min

---

**#261: CORE-USER-XIAN** - Migrate xian Superuser

**Implementation Steps**:
1. **Create xian superuser in users table**:
```sql
INSERT INTO users (id, username, email, role, created_at)
VALUES (
  'xian-production-uuid',
  'xian',
  'xian@piper-morgan.dev',
  'superuser',
  NOW()
);
```

2. **Migrate legacy data**:
   - Move API keys from config/PIPER.user.md → database
   - Associate orphaned knowledge nodes (user_id IS NULL → xian's user_id)
   - Associate orphaned conversations
   - Track migration in metadata

3. **Update hardcoded references**:
   - Search codebase for "xian" hardcoding
   - Replace with user lookup via username
   - Example: `user_service.get_user_by_username("xian")`

4. **Archive legacy config**:
   - Move config/PIPER.user.md → config/archive/PIPER.user.md.legacy
   - Keep for reference (don't delete!)
   - Add README explaining migration

**Chief's Guidance**: "Keep it simple" - This is configuration migration, not complex infrastructure

**Testing**:
- xian superuser can authenticate
- xian has superuser powers (can bypass boundaries)
- Legacy data accessible via new xian account
- No hardcoded references remain

Estimated: 1-2h → Likely: 20 min

---

### Group 3: CORE-UX (3 issues, ~1 hour actual) ⭐ **EXECUTE THIRD**

**Rationale**: Quick wins for momentum

**#254: CORE-UX-QUIET** - Quiet Startup Mode
- Add `--quiet` and `--verbose` flags to CLI
- Default: verbose (current behavior)
- `--quiet`: Suppress startup messages, only show errors
- `--verbose`: Explicit verbose mode (same as default)

**Implementation**:
```python
# main.py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--quiet', action='store_true', help='Suppress startup messages')
parser.add_argument('--verbose', action='store_true', help='Verbose output (default)')

if args.quiet:
    logging.getLogger().setLevel(logging.ERROR)
else:
    logging.getLogger().setLevel(logging.INFO)
```

Estimated: 2h → Likely: 20 min

---

**#255: CORE-UX-STATUS-USER** - Status Checker User Detection
- Display current user in status output
- Show user context in health checks
- Detect user from session/JWT token

**Implementation**:
```python
# scripts/status_checker.py

async def show_status():
    # Detect current user
    current_user = await get_current_user()  # From JWT or session

    print(f"\nCurrent User: {current_user.username} (role: {current_user.role})")
    print(f"User Type: {current_user.user_type}")  # alpha or production

    # Show user's API keys
    print("\nAPI Keys:")
    keys = await get_user_api_keys(current_user.id)
    for key in keys:
        print(f"  {key.provider}: {'Valid' if key.is_valid else 'Invalid'}")
```

Estimated: 3h → Likely: 30 min

---

**#256: CORE-UX-BROWSER** - Auto-Launch Browser
- Auto-open http://localhost:8001 on startup
- Add `--no-browser` flag to disable
- Handle headless environments gracefully

**Implementation**:
```python
import webbrowser

# main.py
parser.add_argument('--no-browser', action='store_true', help='Don\'t auto-launch browser')

if not args.no_browser and not is_headless():
    webbrowser.open('http://localhost:8001')
```

Estimated: 1h → Likely: 10 min

---

### Group 4: CORE-KEYS (3 issues, ~1.5 hours actual) ⭐ **EXECUTE FOURTH**

**Rationale**: Builds on user architecture

**#250: CORE-KEYS-ROTATION-REMINDERS** - Automated Key Rotation Reminders
- Implement 90-day rotation reminders
- Track key age in UserAPIKeyService
- Send notifications via preferred channel

**Implementation**:
```python
# services/security/user_api_key_service.py

class UserAPIKeyService:
    async def check_key_age(self, user_id: str) -> List[RotationReminder]:
        keys = await self.get_user_keys(user_id)
        reminders = []

        for key in keys:
            age_days = (datetime.now() - key.created_at).days

            if age_days >= 90:
                reminders.append(RotationReminder(
                    provider=key.provider,
                    age_days=age_days,
                    severity='urgent' if age_days > 100 else 'warning'
                ))

        return reminders
```

Estimated: 2h → Likely: 20 min

---

**#252: CORE-KEYS-STRENGTH-VALIDATION** - API Key Strength & Security Validation
- Validate key format and strength
- Check for common/weak patterns
- Warn about insecure keys

**Implementation**:
```python
class KeyStrengthValidator:
    def validate_openai_key(self, key: str) -> ValidationResult:
        # Format: sk-...
        if not key.startswith('sk-'):
            return ValidationResult(valid=False, reason='Invalid format')

        # Length check
        if len(key) < 40:
            return ValidationResult(valid=False, reason='Key too short')

        # Entropy check (basic)
        if self.is_low_entropy(key):
            return ValidationResult(valid=True, warning='Low entropy detected')

        return ValidationResult(valid=True)
```

Estimated: 2h → Likely: 20 min

---

**#253: CORE-KEYS-COST-ANALYTICS** - API Cost Tracking & Usage Analytics
- Track API calls per service
- Calculate estimated costs
- Usage dashboard/reports

**Implementation**:
```python
class APIUsageTracker:
    async def track_call(self, user_id: str, provider: str, model: str,
                         tokens: int, cost_usd: float):
        await self.db.execute(
            """
            INSERT INTO api_usage (user_id, provider, model, tokens, cost_usd)
            VALUES (:user_id, :provider, :model, :tokens, :cost_usd)
            """,
            {
                'user_id': user_id,
                'provider': provider,
                'model': model,
                'tokens': tokens,
                'cost_usd': cost_usd
            }
        )

    async def get_user_usage(self, user_id: str,
                             period: str = 'month') -> UsageReport:
        # Aggregate usage by provider/model
        # Calculate total costs
        # Return formatted report
        pass
```

Estimated: 3h → Likely: 30 min

---

### Group 5: CORE-PREF (1 issue, ~45 min actual) ⭐ **EXECUTE LAST**

**Rationale**: Integrates everything

**#248: CORE-PREF-CONVO** - Conversational Preference Gathering
- Interactive personality assessment
- Completes Piper Education (final 10%)
- Store preferences in alpha_users.preferences (JSONB)
- Bridges learning infrastructure to UX

**Implementation**:
```python
# Conversational flow
async def gather_preferences(user_id: str):
    """Interactive preference gathering"""

    preferences = {}

    # Communication style
    response = await ask_user(
        "How do you prefer Piper Morgan to communicate?",
        options=['concise', 'balanced', 'detailed']
    )
    preferences['communication_style'] = response

    # Work style
    response = await ask_user(
        "What's your typical work style?",
        options=['structured', 'flexible', 'exploratory']
    )
    preferences['work_style'] = response

    # Domain preferences
    # Decision-making style
    # Learning preferences
    # ... (full personality assessment)

    # Store in JSONB
    await update_user_preferences(user_id, preferences)
```

**Chief's Guidance**: Use JSONB in alpha_users table for flexibility

Estimated: 3-5h → Likely: 45 min

---

## Execution Plan

### Day 1 (Wed Oct 23) - Complete Sprint

**Morning (9 AM - 12 PM)**:
```
Phase 0: Quick Discovery (30 min)
- Audit existing infrastructure
- Validate assumptions
- Document findings

Phase 1: Critical Fixes (45 min)
- Issue #257: CORE-KNOW-BOUNDARY-COMPLETE
- Issue #258: CORE-AUTH-CONTAINER
- Why first: Unblock everything else

Phase 2: CORE-USER (1 hour)
- Issue #259: CORE-USER-ALPHA-TABLE
- Issue #260: CORE-USER-MIGRATION
- Issue #261: CORE-USER-XIAN
- Why second: Foundation for multi-user
```

**Afternoon (1 PM - 4 PM)**:
```
Phase 3: CORE-UX (1 hour)
- Issue #254: CORE-UX-QUIET
- Issue #255: CORE-UX-STATUS-USER
- Issue #256: CORE-UX-BROWSER
- Why third: Quick wins for momentum

Phase 4: CORE-KEYS (1.5 hours)
- Issue #250: CORE-KEYS-ROTATION-REMINDERS
- Issue #252: CORE-KEYS-STRENGTH-VALIDATION
- Issue #253: CORE-KEYS-COST-ANALYTICS
- Why fourth: Builds on user architecture

Phase 5: CORE-PREF (45 min)
- Issue #248: CORE-PREF-CONVO
- Why last: Integrates everything
```

**End of Day**:
- Result: All 12 issues complete in ONE DAY
- Total Time: ~5 hours actual work
- Testing: Critical priorities (multi-user isolation, boundaries, JWT, keys)

---

## Testing Requirements (Chief Architect)

### Critical Tests (Must Pass)

**1. Multi-User Isolation**
```python
def test_alpha_user_cannot_see_production_data():
    # Create alpha user and production user
    # Verify alpha user queries don't return production data
    pass

def test_production_user_cannot_see_alpha_data():
    # Create production user and alpha user
    # Verify production user queries don't return alpha data
    pass

def test_user_migrations_preserve_isolation():
    # Migrate alpha user to production
    # Verify data isolation maintained
    pass
```

**2. Boundary Enforcement**
```python
def test_knowledge_queries_respect_boundaries():
    # Query with regular user
    # Verify boundaries enforced
    pass

def test_superuser_can_bypass_boundaries():
    # Query with superuser (xian)
    # Verify boundaries can be bypassed
    pass

def test_admin_cannot_bypass_boundaries():
    # Query with admin user
    # Verify boundaries still enforced
    pass
```

**3. JWT with Proper DI**
```python
def test_auth_container_provides_jwt_service():
    # Get JWT service from container
    # Verify no circular dependencies
    pass

def test_jwt_blacklist_works_with_di():
    # Blacklist a token
    # Verify it's rejected
    pass
```

**4. Key Rotation Logic**
```python
def test_90_day_rotation_reminder_triggers():
    # Create key with old timestamp
    # Verify reminder triggered
    pass

def test_key_strength_validation_catches_weak_keys():
    # Submit weak key
    # Verify warning shown
    pass

def test_cost_analytics_tracks_usage():
    # Make API calls
    # Verify usage tracked
    pass
```

---

## Success Metrics

### Sprint Success
- All 12 issues complete (100%)
- Zero critical bugs
- All tests passing (4 critical test suites)
- Security boundaries enforced
- Multi-user isolation verified

### Quality Metrics
- Test coverage maintained >80%
- Performance unchanged (<100ms API)
- No technical debt added
- Documentation complete

---

## Risk Assessment

### Low Risk (High Confidence)
- **CORE-UX**: Simple flag additions
- **Critical Fixes**: Just wiring existing code
- **CORE-USER-XIAN**: Configuration migration

### Medium Risk
- **CORE-KEYS**: May need new infrastructure
- **CORE-USER tables**: Database migrations
- **CORE-PREF-CONVO**: UI complexity

### Mitigation
- Start with Phase 0 discovery
- Critical fixes first unblock other work
- CORE-USER foundation enables rest of sprint
- Testing priorities focus on critical paths

---

## Definition of Done

**Sprint A7 Complete When**:
1. All 12 issues closed with evidence
2. All critical tests passing (4 test suites)
3. Critical TODOs resolved (8 of 145)
4. Multi-user architecture operational
5. Alpha_users table created and working
6. xian superuser migrated successfully
7. Ready for Alpha Wave 2 launch

---

## Velocity Prediction

Based on Sprint A6's 88% faster pattern + Chief Architect guidance:

**Realistic**: 1 day (~5 hours actual work)
**Conservative**: 1.5 days (if complexity hits)
**Optimistic**: <1 day (if all infrastructure perfect)

Given that:
- Sprint A6 completed 6 issues in <1 day
- Sprint A7 has 12 issues but simpler scope
- Critical fixes first unblock everything else
- Chief provided clear architectural decisions

**1 day completion is achievable and realistic.**

---

## Next Steps

### Today (Oct 22, 5:40 PM)
1. ✅ Gameplan updated with Chief's order
2. ✅ Architectural decisions documented
3. ✅ Ready for execution tomorrow

### Tomorrow (Oct 23)
1. Execute Day 1 (all 12 issues)
2. Follow revised order (Critical Fixes first)
3. Run critical testing (4 test suites)
4. Sprint A7 complete!

### Thursday (Oct 24)
1. Sprint A8: Alpha Prep begins
2. Documentation updates
3. Alpha deployment planning

### Early November
1. Alpha Wave 2 launch
2. First external testers onboarded

---

## Alpha Launch Timeline

**Monday Oct 28**: Final testing and prep
**Tuesday Oct 29**: First alpha user (potentially!)
**Early November**: Alpha Wave 2 full launch

---

## Chief Architect's Wisdom Applied

✅ **Separate alpha_users table** - Clean isolation
✅ **Critical fixes first** - Unblock dependencies
✅ **Keep xian migration simple** - Config → database
✅ **Lightweight Alembic** - One migration, JSONB for flexibility
✅ **Focus testing** - Multi-user isolation, boundaries, JWT, keys
✅ **Don't over-engineer** - This is alpha, not production

---

*Sprint A7 gameplan revised and ready for execution!*

**Version**: 2.0 (Chief Architect guidance applied)
**Last Updated**: October 22, 2025, 5:40 PM PDT
**Ready**: YES - Deploy agents tomorrow morning!
