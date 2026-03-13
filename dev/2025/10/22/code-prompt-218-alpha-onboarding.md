# Code Implementation Prompt: Alpha User Onboarding

**Agent**: Code (Lead Developer)
**Issue**: #218 CORE-USERS-ONBOARD
**Task**: Implement setup wizard and health checks for Alpha Wave 2 users
**Date**: Tuesday, October 22, 2025, 11:45 AM
**Estimated Duration**: 12 hours → Target 2-3 hours actual
**Gameplan**: See attached `gameplan-218-alpha-onboarding.md`

---

## Mission

**Goal**: Enable Alpha Wave 2 (guided technical users) to self-onboard with minimal friction using an interactive setup wizard.

**Strategic Context**: 85% of infrastructure is complete from Sprint A6 (#227, #228, #229, #249). This is primarily **integration and UX work** over existing services, not new architecture.

**Success Criteria**: PM can clone repo, run setup wizard, and have working Piper Morgan in <5 minutes.

---

## Your Responsibilities

### MVP Scope (Must Have)
- ✅ Setup wizard CLI (`python main.py setup`)
- ✅ System requirement checks (Docker, Python, ports, database)
- ✅ API key collection with real-time validation
- ✅ Secure key storage (using UserAPIKeyService from #228)
- ✅ User account creation (using User model from #228)
- ✅ Status checker CLI (`python main.py status`)
- ✅ Health checks (database, API keys, basic metrics)
- ✅ README updates with quick start instructions

### Out of Scope (Defer to Sprint A7)
- ❌ Preference management CLI commands
- ❌ Video walkthrough documentation
- ❌ Comprehensive FAQ (build from alpha feedback)
- ❌ Integration setup (GitHub, Notion, Slack) - optional for now

---

## Phase 0: Infrastructure Investigation (30 minutes)

**CRITICAL**: Verify infrastructure before planning implementation.

### Questions to Answer

1. **CLI Infrastructure**:
   ```bash
   # Is there existing CLI framework?
   grep -r "argparse\|click\|typer" *.py
   ls -la main.py setup.py

   # How is main.py structured?
   cat main.py | head -50
   ```

2. **Configuration System**:
   ```bash
   # How are configs structured?
   ls -la config/
   cat config/PIPER.user.md.example

   # Is there preference management?
   find services -name "*preference*" -o -name "*config*"
   ```

3. **Existing Services** (Verify from #228, #229):
   ```bash
   # UserAPIKeyService available?
   cat services/security/user_api_key_service.py | head -50

   # Does it have validate_api_key()?
   grep -A 10 "def validate_api_key" services/security/user_api_key_service.py

   # User model ready?
   grep -A 20 "class User" services/database/models.py

   # Session factory for database?
   cat services/database/session_factory.py | head -30
   ```

4. **Entry Points**:
   ```bash
   # How to add CLI commands?
   # Check for setup.py or pyproject.toml
   ls -la setup.py pyproject.toml

   # Check main.py for argument handling
   grep -A 20 "if __name__" main.py
   ```

### Document Your Findings

Create investigation report in your session log:

```markdown
## Phase 0: Infrastructure Investigation

### CLI Framework
- [Finding 1]
- [Finding 2]

### Configuration System
- [Finding 1]
- [Finding 2]

### Available Services
- UserAPIKeyService: [status and methods]
- User model: [fields and relationships]
- Database session: [how to get sessions]

### Recommended Approach
Based on findings, recommend:
1. Where to put setup_wizard.py
2. How to wire up CLI commands
3. How to integrate with existing services
```

---

## Phase 1A: Setup Wizard CLI (8 hours → 1-1.5 hours)

### Implementation Strategy

Create `scripts/setup_wizard.py` (or appropriate location based on Phase 0 findings).

### 1. System Checks (20 minutes)

```python
"""Setup wizard for Piper Morgan Alpha onboarding"""

import asyncio
import sys
import subprocess
import socket
from typing import Dict, Any

async def check_docker() -> bool:
    """Check if Docker is installed"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

async def check_python_version() -> bool:
    """Check Python version >= 3.11"""
    return sys.version_info >= (3, 11)

async def check_port_available(port: int = 8001) -> bool:
    """Check if port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", port))
        return True
    except OSError:
        return False

async def check_database() -> bool:
    """Check database connectivity"""
    try:
        from services.database.session_factory import AsyncSessionFactory
        session_factory = AsyncSessionFactory()

        async with session_factory.session_scope() as session:
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))

        return True
    except Exception as e:
        print(f"   Database check failed: {e}")
        return False

async def check_system() -> Dict[str, bool]:
    """Run all system checks"""
    print("1. System Check")

    checks = {
        "Docker installed": await check_docker(),
        "Python 3.11+": await check_python_version(),
        "Port 8001 available": await check_port_available(),
        "Database accessible": await check_database()
    }

    for name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"   {status} {name}")

    return checks
```

### 2. API Key Collection with Validation (30-45 minutes)

```python
from getpass import getpass
import uuid
from services.security.user_api_key_service import UserAPIKeyService

async def collect_and_validate_api_keys(user_id: str) -> Dict[str, str]:
    """Collect API keys with real-time validation"""

    print("\n2. API Keys")
    print("   (Keys are stored securely in your system keychain)")

    service = UserAPIKeyService()
    stored_keys = {}

    # OpenAI (required)
    print("\n   OpenAI API key (required):")
    while True:
        openai_key = getpass("   Enter key (sk-...): ")

        if not openai_key:
            print("   ✗ OpenAI key is required")
            continue

        print("   Validating...")

        try:
            # Use existing validation from #228
            is_valid = await service.validate_api_key("openai", openai_key)

            if is_valid:
                print("   ✓ Valid (gpt-4 access confirmed)")

                # Store securely using #228 infrastructure
                async with session_factory.session_scope() as session:
                    await service.store_user_key(
                        user_id=user_id,
                        provider="openai",
                        api_key=openai_key,
                        session=session
                    )
                    await session.commit()

                stored_keys["openai"] = openai_key
                break
            else:
                print("   ✗ Invalid key or API error. Please try again.")
        except Exception as e:
            print(f"   ✗ Validation error: {e}")
            print("   Please check your key and try again.")

    # Anthropic (optional)
    print("\n   Anthropic API key (optional, press Enter to skip):")
    anthropic_key = getpass("   Enter key (sk-ant-...): ")

    if anthropic_key:
        print("   Validating...")
        try:
            is_valid = await service.validate_api_key("anthropic", anthropic_key)

            if is_valid:
                print("   ✓ Valid (claude-3-opus access confirmed)")

                async with session_factory.session_scope() as session:
                    await service.store_user_key(
                        user_id=user_id,
                        provider="anthropic",
                        api_key=anthropic_key,
                        session=session
                    )
                    await session.commit()

                stored_keys["anthropic"] = anthropic_key
            else:
                print("   ✗ Invalid key. Skipping Anthropic setup.")
        except Exception as e:
            print(f"   ✗ Validation error: {e}. Skipping Anthropic setup.")
    else:
        print("   Skipped (you can add this later)")

    # GitHub (optional)
    print("\n   GitHub token (optional, press Enter to skip):")
    github_token = getpass("   Enter token (ghp_...): ")

    if github_token:
        print("   ✓ GitHub token saved (validation will happen on first use)")
        async with session_factory.session_scope() as session:
            await service.store_user_key(
                user_id=user_id,
                provider="github",
                api_key=github_token,
                session=session
            )
            await session.commit()
        stored_keys["github"] = github_token
    else:
        print("   Skipped (you can add this later)")

    return stored_keys
```

### 3. User Account Creation (15 minutes)

```python
from services.database.models import User
from datetime import datetime

async def create_user_account() -> User:
    """Create user account for multi-user support"""

    print("\n3. User Account")
    print("   Creating your Piper Morgan account...")

    username = input("   Username: ").strip()

    while not username:
        print("   ✗ Username is required")
        username = input("   Username: ").strip()

    email = input("   Email (optional, press Enter to skip): ").strip() or None

    # Create user using existing User model from #228
    user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    async with session_factory.session_scope() as session:
        session.add(user)
        await session.commit()

    print(f"   ✓ Account created: {username}")

    return user
```

### 4. Main Setup Flow (20-30 minutes)

```python
async def run_setup_wizard():
    """Main setup wizard entry point"""

    print("\n" + "="*50)
    print("Welcome to Piper Morgan Alpha!")
    print("="*50)
    print("\nLet's get you set up (takes about 5 minutes)")
    print()

    try:
        # Phase 1: System checks
        checks = await check_system()

        if not all(checks.values()):
            print("\n❌ Setup cannot continue. Please fix the issues above.")
            print("\nTroubleshooting:")

            if not checks["Docker installed"]:
                print("  • Install Docker: https://docs.docker.com/get-docker/")
            if not checks["Python 3.11+"]:
                print("  • Install Python 3.11+: https://www.python.org/downloads/")
            if not checks["Port 8001 available"]:
                print("  • Free up port 8001 or stop other Piper Morgan instances")
            if not checks["Database accessible"]:
                print("  • Ensure database is running: docker-compose up -d db")

            return False

        # Phase 2: Create user first (need user_id for API keys)
        user = await create_user_account()

        # Phase 3: API keys
        api_keys = await collect_and_validate_api_keys(user.id)

        # Phase 4: Success!
        print("\n" + "="*50)
        print("✅ Setup Complete!")
        print("="*50)

        print(f"\nYour account:")
        print(f"  Username: {user.username}")
        if user.email:
            print(f"  Email: {user.email}")

        print(f"\nConfigured API providers:")
        for provider in api_keys.keys():
            print(f"  ✓ {provider}")

        print("\nNext steps:")
        print("  1. Start Piper Morgan: python main.py")
        print("  2. Access at: http://localhost:8001")
        print("  3. Check system status: python main.py status")

        print("\nNeed help?")
        print("  • Documentation: docs/")
        print("  • Issues: https://github.com/mediajunkie/piper-morgan/issues")

        return True

    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        return False
    except Exception as e:
        print(f"\n\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False
```

### 5. CLI Entry Point

**Update `main.py`** (or create appropriate entry point based on Phase 0):

```python
import sys
import asyncio

# At top of main.py or in appropriate location
if __name__ == "__main__":
    # Check for setup command
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        from scripts.setup_wizard import run_setup_wizard
        success = asyncio.run(run_setup_wizard())
        sys.exit(0 if success else 1)

    elif len(sys.argv) > 1 and sys.argv[1] == "status":
        from scripts.status_checker import run_status_check
        asyncio.run(run_status_check())
        sys.exit(0)

    else:
        # Normal Piper Morgan startup
        # [existing main.py logic]
        pass
```

---

## Phase 1B: Status Checker (4 hours → 30 minutes)

Create `scripts/status_checker.py`:

```python
"""System health checker for Piper Morgan"""

import asyncio
from typing import Dict, Any
from datetime import datetime
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService
from sqlalchemy import text

class StatusChecker:
    """Check system health and provide diagnostics"""

    def __init__(self):
        self.session_factory = AsyncSessionFactory()
        self.api_key_service = UserAPIKeyService()

    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity"""
        try:
            async with self.session_factory.session_scope() as session:
                result = await session.execute(text("SELECT version()"))
                version = result.scalar_one()

                # Count users
                user_count = await session.execute(text("SELECT COUNT(*) FROM users"))
                count = user_count.scalar_one()

            return {
                "status": "✓",
                "message": "PostgreSQL connected",
                "details": f"{count} users registered"
            }
        except Exception as e:
            return {
                "status": "✗",
                "message": f"Database error: {str(e)[:100]}",
                "details": None
            }

    async def check_api_keys(self) -> Dict[str, Dict[str, Any]]:
        """Check API key validity for all providers"""

        results = {}

        # Get all users (for alpha, might just be one)
        try:
            async with self.session_factory.session_scope() as session:
                user_result = await session.execute(
                    text("SELECT id, username FROM users LIMIT 1")
                )
                user = user_result.first()

                if not user:
                    return {
                        "status": "⚠",
                        "message": "No users found. Run setup wizard first.",
                        "details": {}
                    }

                user_id = user[0]

                # Check each provider
                for provider in ["openai", "anthropic", "github"]:
                    try:
                        # Retrieve key
                        key_record = await self.api_key_service.retrieve_user_key(
                            user_id, provider, session
                        )

                        if not key_record:
                            results[provider] = {
                                "status": "○",
                                "message": "Not configured"
                            }
                            continue

                        # Validate (only for OpenAI/Anthropic, skip GitHub)
                        if provider in ["openai", "anthropic"]:
                            is_valid = await self.api_key_service.validate_api_key(
                                provider,
                                key_record.encrypted_key_ref  # Gets decrypted key
                            )

                            if is_valid:
                                results[provider] = {
                                    "status": "✓",
                                    "message": "Valid"
                                }
                            else:
                                results[provider] = {
                                    "status": "✗",
                                    "message": "Invalid or expired"
                                }
                        else:
                            # GitHub token (don't validate, expensive)
                            results[provider] = {
                                "status": "✓",
                                "message": "Configured (not validated)"
                            }

                    except Exception as e:
                        results[provider] = {
                            "status": "✗",
                            "message": f"Error: {str(e)[:50]}"
                        }

        except Exception as e:
            return {
                "status": "✗",
                "message": f"Error checking API keys: {e}",
                "details": {}
            }

        return results

    async def check_performance(self) -> Dict[str, Any]:
        """Check basic performance metrics"""
        try:
            start = datetime.now()

            # Quick database query
            async with self.session_factory.session_scope() as session:
                await session.execute(text("SELECT 1"))

            end = datetime.now()
            response_time_ms = (end - start).total_seconds() * 1000

            return {
                "status": "✓" if response_time_ms < 100 else "⚠",
                "message": f"Response time: {response_time_ms:.1f}ms",
                "details": "Good" if response_time_ms < 100 else "Slow"
            }
        except Exception as e:
            return {
                "status": "✗",
                "message": f"Performance check failed: {e}",
                "details": None
            }

async def run_status_check():
    """Main status check entry point"""

    print("\n" + "="*50)
    print("Piper Morgan System Status")
    print("="*50)
    print()

    checker = StatusChecker()

    # Database
    print("Database:")
    db_status = await checker.check_database()
    print(f"  {db_status['status']} {db_status['message']}")
    if db_status['details']:
        print(f"     {db_status['details']}")

    # API Keys
    print("\nAPI Keys:")
    key_status = await checker.check_api_keys()

    if isinstance(key_status, dict) and "status" in key_status:
        # Error case
        print(f"  {key_status['status']} {key_status['message']}")
    else:
        # Provider results
        for provider, status in key_status.items():
            print(f"  {status['status']} {provider}: {status['message']}")

    # Performance
    print("\nPerformance:")
    perf_status = await checker.check_performance()
    print(f"  {perf_status['status']} {perf_status['message']}")

    # Recommendations
    print("\nRecommendations:")

    recommendations = []

    if db_status['status'] == "✗":
        recommendations.append("  • Fix database connectivity (see error above)")

    if isinstance(key_status, dict) and not any(s['status'] == '✓' for s in key_status.values() if isinstance(s, dict)):
        recommendations.append("  • Configure at least one API provider (run: python main.py setup)")

    if perf_status['status'] == "⚠":
        recommendations.append("  • System performance is slow - check database load")

    if not recommendations:
        recommendations.append("  ✓ All systems operational!")

    for rec in recommendations:
        print(rec)

    print()
```

---

## Phase 2: README Updates (30 minutes)

### Update `README.md`

Add quick start section at top:

```markdown
# Piper Morgan - Alpha

Intelligent PM assistant with conversational AI.

## Quick Start

### Option 1: Guided Setup (Recommended for New Users)

```bash
# Clone repository
git clone https://github.com/mediajunkie/piper-morgan.git
cd piper-morgan

# Run interactive setup wizard
python main.py setup
```

The setup wizard will:
1. ✓ Check system requirements
2. ✓ Collect and validate your API keys
3. ✓ Create your user account
4. ✓ Get you ready to use Piper Morgan

Setup takes about 5 minutes.

### Option 2: Manual Setup (Advanced Users)

```bash
# Clone repository
git clone https://github.com/mediajunkie/piper-morgan.git
cd piper-morgan

# Copy config template
cp config/PIPER.user.md.example config/PIPER.user.md

# Edit config file with your API keys
nano config/PIPER.user.md

# Start services
docker-compose up
```

Access Piper Morgan at: http://localhost:8001

## Requirements

- **Docker** - Container runtime
- **Python 3.11+** - Core language
- **API Keys** - At least one of:
  - OpenAI API key (for GPT-4)
  - Anthropic API key (for Claude)

## Commands

```bash
python main.py setup   # Interactive setup wizard (first-time users)
python main.py status  # Check system health
python main.py         # Start Piper Morgan
```

## Getting Help

- **Documentation**: See `docs/` folder
- **Issues**: https://github.com/mediajunkie/piper-morgan/issues
- **Discussions**: https://github.com/mediajunkie/piper-morgan/discussions

## Next Steps After Setup

1. Start Piper Morgan: `python main.py`
2. Open browser: http://localhost:8001
3. Try your first query!
4. Check status anytime: `python main.py status`
```

### Create Troubleshooting Guide

Create `docs/troubleshooting.md`:

```markdown
# Troubleshooting Guide

## Setup Issues

### "Docker is not installed"

**Solution**: Install Docker Desktop:
- macOS: https://docs.docker.com/desktop/mac/install/
- Windows: https://docs.docker.com/desktop/windows/install/
- Linux: https://docs.docker.com/engine/install/

### "Python 3.11+ required"

**Solution**: Install Python:
- Download from: https://www.python.org/downloads/
- Ensure Python 3.11 or newer

### "Port 8001 is not available"

**Solution**:
```bash
# Find what's using port 8001
lsof -i :8001

# Stop existing Piper Morgan instances
docker-compose down
```

### "Database is not accessible"

**Solution**:
```bash
# Start database
docker-compose up -d db

# Wait 10 seconds for startup
sleep 10

# Try setup again
python main.py setup
```

## API Key Issues

### "OpenAI API key is invalid"

**Causes**:
1. Typo in key (should start with `sk-`)
2. Key revoked or expired
3. Network connectivity issues
4. Rate limit exceeded

**Solution**:
1. Double-check key from: https://platform.openai.com/api-keys
2. Test key directly with OpenAI API
3. Check internet connection
4. Wait a few minutes if rate limited

### "Anthropic API key is invalid"

**Causes**:
1. Typo in key (should start with `sk-ant-`)
2. Key revoked or expired
3. Network connectivity issues

**Solution**:
1. Double-check key from: https://console.anthropic.com/
2. Ensure key has Claude access
3. Check internet connection

## Runtime Issues

### "Connection refused" when accessing http://localhost:8001

**Solution**:
```bash
# Check if services are running
docker-compose ps

# Start services
docker-compose up

# Check logs for errors
docker-compose logs web
```

### Slow performance

**Solution**:
```bash
# Check system status
python main.py status

# Restart services
docker-compose restart

# Check Docker resources (Docker Desktop → Settings → Resources)
```

## Still Need Help?

Open an issue: https://github.com/mediajunkie/piper-morgan/issues
```

---

## Testing Requirements

### Manual Testing (PM as User 0)

**Critical Test Flow**:
1. Clone fresh repository
2. Run `python main.py setup`
3. Follow wizard prompts
4. Verify keys stored correctly: `python main.py status`
5. Start Piper Morgan: `python main.py`
6. Access http://localhost:8001
7. Submit first query
8. Verify response

**Test Cases**:
- ✅ Setup with OpenAI only
- ✅ Setup with both OpenAI + Anthropic
- ✅ Setup with invalid key (should retry)
- ✅ Setup cancellation (Ctrl+C)
- ✅ Status check shows correct info
- ✅ Normal startup still works (no regression)

### Automated Testing (If Time Permits)

**DECISION POINT**: Ask PM if automated tests needed or if manual testing is sufficient for Alpha.

If automated tests requested:

```python
# tests/setup/test_setup_wizard.py
import pytest
from scripts.setup_wizard import check_system, check_docker, check_python_version

class TestSystemChecks:
    """Test system requirement checks"""

    @pytest.mark.asyncio
    async def test_check_python_version(self):
        """Test Python version check"""
        result = await check_python_version()
        assert result == True  # We're running Python 3.11+!

    @pytest.mark.asyncio
    async def test_check_docker(self):
        """Test Docker installation check"""
        result = await check_docker()
        # May pass or fail depending on environment
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_check_system(self):
        """Test complete system check"""
        results = await check_system()
        assert isinstance(results, dict)
        assert "Python 3.11+" in results
```

---

## Acceptance Criteria Verification

### Must Have (MVP) ✅

Before marking complete, verify:

- [ ] **Setup wizard runs**: `python main.py setup` executes without errors
- [ ] **System checks work**: Docker, Python, port, database all verified
- [ ] **API key collection**: Prompts for OpenAI (required), Anthropic (optional), GitHub (optional)
- [ ] **Real-time validation**: Invalid keys rejected with helpful messages
- [ ] **Secure storage**: Keys stored via UserAPIKeyService (#228 infrastructure)
- [ ] **User account created**: Uses User model from #228
- [ ] **Status command works**: `python main.py status` shows system health
- [ ] **Health checks accurate**: Database, API keys, performance all checked
- [ ] **README updated**: Quick start instructions for both guided and manual setup
- [ ] **No regressions**: Existing DIY workflow still works
- [ ] **PM testing successful**: PM can complete setup in <5 minutes

### Evidence Required

- [ ] Session log with investigation findings
- [ ] Screenshots/terminal output of setup wizard
- [ ] Screenshots/terminal output of status command
- [ ] Updated README in repository
- [ ] Manual test results from PM
- [ ] GitHub issue updated with completion evidence

---

## Session Log Requirements

**File**: Continue your existing log `dev/2025/10/22/2025-10-22-0930-prog-code-log.md`

**Add new session section**:

```markdown
---

## Session 4: Issue #218 - Alpha User Onboarding (11:47 AM)

**Issue**: #218 CORE-USERS-ONBOARD
**Task**: Setup wizard + health checks for Alpha Wave 2
**Estimated Duration**: 12 hours → Target 2-3 hours

### Phase 0: Infrastructure Investigation (11:47-12:XX)

[Investigation findings...]

### Phase 1A: Setup Wizard Implementation (12:XX-XX:XX)

[Implementation progress...]

### Phase 1B: Status Checker Implementation (XX:XX-XX:XX)

[Implementation progress...]

### Phase 2: Documentation Updates (XX:XX-XX:XX)

[Documentation changes...]

### Testing & Verification (XX:XX-XX:XX)

[Test results...]

### Session Complete (XX:XX PM)

**Duration**: [Actual time]
**Status**: [Complete/Blocked/In Progress]
**Deliverables**:
- [Files created/modified]
- [Test results]
- [Evidence]

**Next**: Sprint A6 COMPLETE! 🎉
```

---

## Critical Notes

### Leverage Existing Infrastructure

**DO NOT REBUILD** these - they exist from Sprint A6:
- ✅ UserAPIKeyService (#228) - Use for API key storage/validation
- ✅ User model (#228) - Use for account creation
- ✅ AsyncSessionFactory (#229) - Use for database access
- ✅ KeychainService (#228) - Automatically used by UserAPIKeyService

### Integration Points

**API Key Validation** (from #228):
```python
# UserAPIKeyService has these methods ready:
await service.validate_api_key(provider, api_key)  # Real validation!
await service.store_user_key(user_id, provider, api_key, session)
await service.retrieve_user_key(user_id, provider, session)
```

**User Creation** (from #228):
```python
# User model is ready:
user = User(
    id=str(uuid.uuid4()),
    username=username,
    email=email,
    created_at=datetime.utcnow()
)
session.add(user)
await session.commit()
```

**Database Access** (from #229):
```python
# AsyncSessionFactory is ready:
from services.database.session_factory import AsyncSessionFactory
session_factory = AsyncSessionFactory()

async with session_factory.session_scope() as session:
    # Use session here
    pass
```

### Error Handling

**User-friendly errors**:
- Clear messages (no stack traces to users)
- Actionable guidance (what to do next)
- Helpful links (documentation, support)

**Examples**:
```python
# Bad
raise Exception("Database connection failed")

# Good
print("✗ Database is not accessible")
print("  Solution: Start database with 'docker-compose up -d db'")
print("  Then wait 10 seconds and try again.")
```

### UX Polish

**Progress indicators**:
```python
print("   Validating...")  # During API call
print("   ✓ Valid")        # Success
print("   ✗ Invalid")      # Failure
```

**Clear sections**:
```python
print("\n2. API Keys")
print("   (Keys are stored securely in your system keychain)")
```

**Success confirmation**:
```python
print("\n" + "="*50)
print("✅ Setup Complete!")
print("="*50)
```

---

## Success Criteria

**Issue #218 is complete when**:

1. ✅ Setup wizard implemented and tested
2. ✅ Status checker implemented and tested
3. ✅ README updated with quick start
4. ✅ PM successfully completes setup in <5 minutes
5. ✅ No regressions in existing DIY workflow
6. ✅ All acceptance criteria verified
7. ✅ GitHub issue updated with evidence
8. ✅ Session log complete

**Then**: Sprint A6 COMPLETE! 🎉

---

## Questions or Blockers?

**STOP conditions**:
- Infrastructure doesn't match assumptions
- Existing services missing expected methods
- Unclear how to integrate with current codebase
- API key validation not working as expected

**If blocked**: Document findings in session log and report to Lead Developer.

---

**Ready to implement! Start with Phase 0 investigation.**

**Target**: Complete by 2:30 PM → Sprint A6 DONE! 🚀

**Good luck, Code!**
