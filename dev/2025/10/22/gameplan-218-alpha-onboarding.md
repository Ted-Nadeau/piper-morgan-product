# Gameplan: Issue #218 Alpha User Onboarding

**Chief Architect**: Cursor
**Issue**: #218 CORE-USERS-ONBOARD
**Sprint**: A6 (Final Issue)
**Date**: Tuesday, October 22, 2025, 11:42 AM
**Estimated**: 24 hours → **Target: 3-4 hours** (if 88% faster pattern holds)

---

## Executive Summary

**Mission**: Enable Alpha Wave 2 (guided technical users) by creating setup wizard and health check system that leverages 85% complete infrastructure.

**Strategic Context**:
- Current DIY model works but blocks broader alpha testing
- All dependencies complete (#227, #228, #229, #249)
- Infrastructure ready: User model, API keys, JWT, database
- Just need UI/UX layer for guided onboarding

**Key Insight**: This is **primarily integration work**, not new architecture. Leverage existing services.

---

## Scope Decision: MVP for Alpha Wave 2

### In Scope (Must Have)
✅ **Phase 1A**: Setup Wizard CLI (8h → 1-2h)
- System checks (Docker, Python, ports)
- API key collection + real-time validation
- User account creation
- Secure key storage (uses #228)

✅ **Phase 1B**: Health Checks (4h → 30min-1h)
- `piper status` command
- Database, API keys, integrations status
- Performance metrics
- Actionable recommendations

### Out of Scope (Future Enhancements)
❌ **Phase 2**: Preferences Management (6h) - **Move to Sprint A7**
- Can use existing PIPER.user.md for alpha
- CLI preference commands are nice-to-have
- Not blocking Alpha Wave 2

❌ **Phase 3**: Documentation (6h) - **Partial, rest in Sprint A7**
- README updates (30min) - **IN SCOPE**
- Video walkthrough - **OUT OF SCOPE** (create later)
- FAQ - **OUT OF SCOPE** (build from alpha feedback)

**Revised Total**: 12 hours estimated → **2-3 hours actual** (if pattern holds)

---

## Phase 0: Infrastructure Verification (30 minutes)

### Pre-Implementation Checks

**Database & Models** (Code investigates):
```bash
# Verify User model supports onboarding
grep -A 20 "class User" services/database/models.py

# Check for any existing setup/config infrastructure
find . -name "*setup*" -o -name "*config*" -o -name "*wizard*" | grep -v __pycache__

# Verify UserAPIKeyService is ready
cat services/security/user_api_key_service.py | head -50
```

**Configuration System** (Code investigates):
```bash
# Check existing config patterns
ls -la config/
cat config/PIPER.user.md.example

# Check for preference management
find services -name "*preference*" -o -name "*config*"
```

**CLI Entry Points** (Code investigates):
```bash
# Check for existing CLI infrastructure
ls -la *.py | grep -E "(main|cli|setup)"
cat main.py | head -30

# Check for argument parsing
grep -r "argparse\|click\|typer" *.py
```

### Questions to Answer

1. **Is there existing CLI infrastructure?** (argparse/click/typer)
2. **Where should `piper` command live?** (setup.py entry point or scripts/)
3. **How are config files structured?** (YAML? JSON? MD?)
4. **Is there a preference service?** (or just direct file reading?)
5. **Are there existing health check utilities?** (database ping, etc.)

### Expected Findings

**Likely have**:
- ✅ User model (from #228)
- ✅ UserAPIKeyService with validation (from #228)
- ✅ Database connectivity (from #229)
- ✅ Config files (PIPER.user.md)

**Likely missing**:
- ❌ CLI framework setup
- ❌ Interactive prompts
- ❌ Setup wizard script
- ❌ Health check command

---

## Phase 1A: Setup Wizard CLI (8 hours → 1-2 hours)

### Implementation Strategy

**Option A: Python Script** (Recommended)
```python
# scripts/setup_wizard.py
import asyncio
from getpass import getpass
from services.security.user_api_key_service import UserAPIKeyService
# ... leverage existing services

async def run_setup():
    print("Welcome to Piper Morgan Alpha!")
    # Interactive prompts...
```

**Option B: CLI Framework** (More robust, but more work)
```python
# Use click or typer for professional CLI
import click

@click.command()
def setup():
    """Interactive setup wizard for Piper Morgan"""
    # ...
```

**Recommendation**: Start with Option A (simple script), can enhance later.

### Sub-Phases

#### 1. System Checks (2h → 20min)
```python
async def check_system():
    """Verify system requirements"""
    checks = {
        "docker": await check_docker_installed(),
        "python": await check_python_version(),
        "port_8001": await check_port_available(8001),
        "database": await check_database_connection()
    }
    return checks
```

**Leverage**:
- Docker check: `subprocess.run(["docker", "--version"])`
- Python check: `sys.version_info >= (3, 11)`
- Port check: `socket` library
- Database check: Existing session_factory

#### 2. API Key Collection (3h → 30-45min)
```python
async def collect_api_keys():
    """Interactive API key collection with validation"""

    # OpenAI (required)
    print("OpenAI API Key (required):")
    openai_key = getpass("sk-...")

    # Validate in real-time (uses #228 infrastructure!)
    is_valid = await user_api_key_service.validate_api_key("openai", openai_key)

    if is_valid:
        print("✓ Valid (gpt-4 access confirmed)")
        await user_api_key_service.store_user_key(user_id, "openai", openai_key)
    else:
        print("✗ Invalid key. Please try again.")
```

**Leverage**:
- ✅ UserAPIKeyService.validate_api_key() (from #228)
- ✅ UserAPIKeyService.store_user_key() (from #228)
- ✅ Real validation with provider APIs

**Providers**:
1. OpenAI (required)
2. Anthropic (optional)
3. GitHub (optional)

#### 3. User Account Creation (1h → 15min)
```python
async def create_user():
    """Create user account for multi-user support"""

    username = input("Username: ")
    email = input("Email (optional): ") or None

    # Create User via existing model
    user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        created_at=datetime.utcnow()
    )

    async with session_factory.session_scope() as session:
        session.add(user)
        await session.commit()

    return user
```

**Leverage**:
- ✅ User model (from #228)
- ✅ session_factory (from #229)
- ✅ Database ready

#### 4. Integration & Polish (2h → 20-30min)
```python
async def run_setup_wizard():
    """Main setup wizard flow"""

    print("Welcome to Piper Morgan Alpha!")
    print("Let's get you set up (5 minutes):\n")

    # 1. System checks
    print("1. System Check")
    checks = await check_system()
    for check, result in checks.items():
        print(f"   {'✓' if result else '✗'} {check}")

    if not all(checks.values()):
        print("\nPlease fix the issues above and try again.")
        return

    # 2. API keys
    print("\n2. API Keys")
    user_id = "default_user"  # Temp, will be from user account
    await collect_api_keys(user_id)

    # 3. User account
    print("\n3. User Account")
    user = await create_user()

    # 4. Success!
    print("\nSetup complete! 🎉")
    print("Starting Piper Morgan...")
    print("Access at: http://localhost:8001")
```

### Entry Point

**Create CLI command**:
```python
# main.py or scripts/piper_cli.py
import sys
from scripts.setup_wizard import run_setup_wizard

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        asyncio.run(run_setup_wizard())
    else:
        # Normal startup
        pass
```

**Usage**: `python main.py setup` or `./piper-morgan setup`

---

## Phase 1B: Health Checks (4 hours → 30min-1h)

### Implementation

```python
# scripts/status_checker.py
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService

class StatusChecker:
    """System health checker"""

    async def check_database(self):
        """Check database connectivity"""
        try:
            async with session_factory.session_scope() as session:
                await session.execute(text("SELECT 1"))
            return {"status": "✓", "message": "PostgreSQL connected"}
        except Exception as e:
            return {"status": "✗", "message": f"Database error: {e}"}

    async def check_api_keys(self, user_id: str):
        """Check API key validity"""
        keys = await user_api_key_service.list_user_keys(user_id)
        results = {}

        for key in keys:
            is_valid = await user_api_key_service.validate_api_key(
                key.provider,
                await user_api_key_service.retrieve_user_key(user_id, key.provider)
            )
            results[key.provider] = {
                "status": "✓" if is_valid else "✗",
                "message": "Valid" if is_valid else "Invalid or expired"
            }

        return results

    async def check_system_health(self):
        """Complete system health check"""
        print("System Status:\n")

        # Database
        print("Database:")
        db_status = await self.check_database()
        print(f"  {db_status['status']} {db_status['message']}")

        # API Keys
        print("\nAPI Keys:")
        key_status = await self.check_api_keys("default_user")
        for provider, status in key_status.items():
            print(f"  {status['status']} {provider}: {status['message']}")

        # Performance (basic)
        print("\nPerformance:")
        print(f"  ✓ Response time: {response_time}ms")

        print("\nRecommendations:")
        # Generate actionable recommendations
```

**CLI Command**:
```python
# In CLI
if sys.argv[1] == "status":
    checker = StatusChecker()
    asyncio.run(checker.check_system_health())
```

**Usage**: `python main.py status` or `./piper-morgan status`

---

## Phase 2: README Updates (30 minutes)

### Minimal Documentation

**Update `README.md`**:
```markdown
# Piper Morgan Alpha

## Quick Start

### Option 1: Guided Setup (Recommended)
```bash
git clone https://github.com/mediajunkie/piper-morgan
cd piper-morgan
python main.py setup
```

Follow the interactive wizard to:
1. Check system requirements
2. Add your API keys
3. Create your account
4. Start using Piper Morgan

### Option 2: Manual Setup (Advanced)
```bash
git clone https://github.com/mediajunkie/piper-morgan
cp config/PIPER.user.md.example config/PIPER.user.md
# Edit PIPER.user.md with your API keys
docker-compose up
```

## Commands

- `python main.py setup` - Interactive setup wizard
- `python main.py status` - Check system health
- `python main.py` - Start Piper Morgan (normal mode)

## Requirements

- Docker
- Python 3.11+
- OpenAI or Anthropic API key
```

**Update `docs/` folder** (if time permits):
- Create `docs/setup-guide.md` with detailed steps
- Create `docs/troubleshooting.md` with common issues

---

## Testing Strategy

### Manual Testing (Priority)
**PM as User 0** tests the wizard:
1. Clone fresh repo
2. Run `python main.py setup`
3. Follow wizard prompts
4. Verify keys stored correctly
5. Check `piper status` output
6. Start Piper Morgan normally
7. Verify first query works

### Automated Testing (If Time Permits)
```python
# tests/setup/test_setup_wizard.py
async def test_system_checks():
    """Test system requirement checks"""
    checks = await check_system()
    assert checks["python"] == True  # We're running Python!

async def test_api_key_validation():
    """Test API key validation"""
    # Mock API calls
    is_valid = await validate_api_key("openai", "sk-test-invalid")
    assert is_valid == False

async def test_status_checker():
    """Test status command"""
    checker = StatusChecker()
    status = await checker.check_database()
    assert status["status"] == "✓"
```

**DECISION POINT**: Ask PM if automated tests are needed or if manual testing is sufficient for Alpha.

---

## Acceptance Criteria

### Must Have (MVP for Alpha Wave 2) ✅
- [x] Setup wizard runs: `python main.py setup`
- [x] System checks verify Docker, Python, port, database
- [x] API key collection with real-time validation
- [x] OpenAI key required, Anthropic optional
- [x] Keys stored securely via UserAPIKeyService (#228)
- [x] User account created via User model
- [x] Status command: `python main.py status`
- [x] Status shows database, API keys, basic health
- [x] README updated with quick start instructions
- [x] Manual testing by PM successful

### Nice to Have (Can Defer) ⚠️
- [ ] Preference configuration in wizard
- [ ] Integration setup (GitHub, Notion, Slack)
- [ ] Automated tests for wizard
- [ ] Comprehensive troubleshooting docs
- [ ] Video walkthrough

### Out of Scope (Sprint A7) ❌
- [ ] CLI preference commands (`piper config set/get`)
- [ ] Preference management system
- [ ] Web-based setup wizard
- [ ] One-click Docker install
- [ ] Detailed FAQ from user feedback

---

## Agent Deployment Strategy

### Lead Developer Coordinates

**Code Agent** - Primary Implementation (2-3 hours):
1. **Phase 0**: Infrastructure investigation (30min)
   - Document existing CLI infrastructure
   - Map out config system
   - Identify integration points

2. **Phase 1A**: Setup Wizard (1-1.5h)
   - Create `scripts/setup_wizard.py`
   - Implement system checks
   - Implement API key collection + validation
   - Implement user account creation
   - Wire up CLI entry point

3. **Phase 1B**: Status Checker (30min)
   - Create `scripts/status_checker.py`
   - Implement health checks
   - Wire up CLI command

4. **Phase 2**: Documentation (30min)
   - Update README.md
   - Basic troubleshooting guide
   - Evidence package for GitHub

**Cursor Agent** - Verification & Polish (30min):
- Test setup wizard flow
- Verify API key validation works
- Test status command
- Cross-validate with Code's implementation
- Polish UX (error messages, formatting)

**Parallel Work**: Code can work on setup wizard while Cursor verifies existing infrastructure.

---

## Success Criteria

### Functional
- ✅ Setup wizard completes in <5 minutes
- ✅ Real API validation catches invalid keys
- ✅ Keys stored securely in OS keychain
- ✅ Status command shows accurate health
- ✅ No breaking changes to DIY workflow

### Technical
- ✅ Leverages 85% existing infrastructure
- ✅ Clean integration with #228 (API keys)
- ✅ Clean integration with #229 (database)
- ✅ No hardcoded credentials
- ✅ Error handling with helpful messages

### User Experience
- ✅ Clear prompts and progress indicators
- ✅ Validation happens in real-time
- ✅ Success confirmation at end
- ✅ Helpful error messages
- ✅ Optional steps clearly marked

---

## Risk Mitigation

### Risk 1: CLI Framework Complexity
**Mitigation**: Start with simple Python script, not full CLI framework

### Risk 2: Interactive Prompts Not Working
**Mitigation**: Use built-in `input()` and `getpass`, test early

### Risk 3: API Validation Slow/Unreliable
**Mitigation**: Cache validation results, allow skip for testing

### Risk 4: User Confusion During Setup
**Mitigation**: Clear progress indicators, helpful error messages, README updates

---

## Future Enhancements (Post-Sprint A6)

### Sprint A7
- **Preference Management**: CLI commands for config
- **Enhanced Documentation**: Video, comprehensive FAQ
- **GitHub Integration**: Setup wizard prompts for repo connection
- **Automated Tests**: Full test coverage for wizard

### Beta
- **Web-based Setup**: Alternative to CLI
- **One-click Install**: Automated Docker setup
- **Health Dashboard**: Web UI for system status
- **Remote Diagnostics**: Support team can check health

---

## Time Estimate vs Target

**Original Estimate**: 24 hours
- Phase 1A: 8 hours
- Phase 1B: 4 hours
- Phase 2: 6 hours
- Phase 3: 6 hours

**Revised MVP Estimate**: 12 hours
- Phase 1A: 8 hours
- Phase 1B: 4 hours
- Phase 2 (minimal): 30min

**Target (88% faster pattern)**: 2-3 hours actual
- Phase 0: 30min (investigation)
- Phase 1A: 1-1.5h (wizard)
- Phase 1B: 30min (status)
- Phase 2: 30min (docs)

**If completed by 2:30 PM**: Sprint A6 COMPLETE! 🎉

---

## Deployment Readiness

### Pre-Deployment Checklist
- [ ] Code investigation complete (Phase 0)
- [ ] Setup wizard implemented and tested
- [ ] Status checker implemented and tested
- [ ] README updated
- [ ] Manual testing by PM successful
- [ ] No regressions in existing DIY workflow

### Post-Deployment
- [ ] GitHub issue #218 updated with evidence
- [ ] Session logs complete
- [ ] Sprint A6 marked complete
- [ ] Chief Architect report prepared

---

## Notes for Agents

### For Code
- **Leverage existing services** - don't reinvent
- **Keep it simple** - basic Python script is fine
- **Test early** - validate API keys actually work
- **Clear errors** - users need helpful messages
- **STOP condition**: If infrastructure doesn't match assumptions

### For Cursor
- **Verify integration points** - check against #228, #229
- **Test user flow** - pretend to be Alpha user
- **Polish UX** - error messages, formatting, progress
- **Cross-validate** - ensure Code's work is production ready

### For Both
- **This is MVP** - perfection is the enemy of Alpha launch
- **User 0 test** - PM will be first user, watch for friction
- **Document assumptions** - what works, what doesn't
- **No scope creep** - stick to setup wizard + status check

---

## Handoff to Lead Developer

**Context for Lead Dev**:
- Final issue of Sprint A6
- All dependencies complete (#227, #228, #229, #249)
- 85% infrastructure ready
- Focus on MVP: wizard + status check
- Defer preferences and advanced docs to Sprint A7

**Agent Coordination**:
- Code: Primary implementation (2-3h)
- Cursor: Verification & polish (30min)
- Can work in parallel after Phase 0

**Success = Alpha Ready**:
- After this issue, we can launch Alpha Wave 2!
- Users can self-onboard with guided wizard
- System health is transparent

---

**Ready to deploy agents on Issue #218!** 🚀

**Gameplan Complete**: 11:45 AM, Tuesday, October 22, 2025
