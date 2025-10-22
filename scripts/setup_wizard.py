"""
Setup Wizard for Piper Morgan Alpha Onboarding

Interactive CLI wizard to onboard new users with:
- System requirement checks
- API key collection and validation
- User account creation
- Secure keychain storage

Issue #218 CORE-USERS-ONBOARD Phase 1A
"""

import asyncio
import socket
import subprocess
import sys
import uuid
from datetime import datetime
from getpass import getpass
from typing import Any, Dict

# Add parent directory to path for imports
sys.path.insert(0, ".")


async def check_docker() -> bool:
    """Check if Docker is installed and running"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


async def check_python_version() -> bool:
    """Check Python version >= 3.9 (3.11+ recommended)"""
    version = sys.version_info
    if version >= (3, 11):
        return True
    elif version >= (3, 9):
        # Allow 3.9+ with warning
        print("   ⚠ Python 3.9 detected - works but 3.11+ recommended")
        return True
    else:
        return False


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
        from sqlalchemy import text

        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope() as session:
            await session.execute(text("SELECT 1"))

        return True
    except Exception as e:
        print(f"   Database check details: {e}")
        return False


async def check_system() -> Dict[str, bool]:
    """Run all system checks"""
    print("\n1. System Check")

    checks = {
        "Docker installed": await check_docker(),
        "Python 3.9+": await check_python_version(),
        "Port 8001 available": await check_port_available(),
        "Database accessible": await check_database(),
    }

    for name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"   {status} {name}")

    return checks


async def check_for_incomplete_setup() -> Any:
    """
    Check if there's a user with no API keys (incomplete setup).

    Returns:
        User object if incomplete setup found, None otherwise
    """
    from sqlalchemy import select

    from services.database.models import User, UserAPIKey
    from services.database.session_factory import AsyncSessionFactory

    try:
        async with AsyncSessionFactory.session_scope() as session:
            # Find users with no API keys
            result = await session.execute(
                select(User)
                .outerjoin(UserAPIKey)
                .where(UserAPIKey.id.is_(None))
                .order_by(User.created_at.desc())
                .limit(1)
            )
            user = result.scalar_one_or_none()
            return user
    except Exception:
        return None


async def create_user_account() -> Any:
    """Create user account for multi-user support"""
    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory

    print("\n2. User Account")

    # Check for incomplete setup (Issue #218 - Smart Resume)
    existing_user = await check_for_incomplete_setup()

    if existing_user:
        print(f"   Found incomplete setup for: {existing_user.username}")
        if existing_user.email:
            print(f"   Email: {existing_user.email}")

        resume = input("   Resume this setup? (y/n): ").strip().lower()

        if resume == "y":
            print(f"   ✓ Resuming setup for {existing_user.username}")
            return existing_user
        else:
            print("   Starting new setup (existing account will remain)...")
    else:
        print("   Creating your Piper Morgan account...")

    # Try to create user, handle duplicates
    max_attempts = 3
    for attempt in range(max_attempts):
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
            updated_at=datetime.utcnow(),
        )

        try:
            async with AsyncSessionFactory.session_scope() as session:
                session.add(user)
                await session.commit()

            print(f"   ✓ Account created: {username}")
            return user

        except Exception as e:
            error_str = str(e).lower()
            if "duplicate" in error_str or "unique" in error_str:
                if "username" in error_str:
                    print(f"   ✗ Username '{username}' already exists")
                elif "email" in error_str:
                    print(f"   ✗ Email '{email}' already exists")
                else:
                    print("   ✗ Account already exists")

                if attempt < max_attempts - 1:
                    print("   Please try a different username or email")
                else:
                    raise ValueError(
                        "Unable to create account after 3 attempts. Username or email may already exist."
                    )
            else:
                # Some other error
                raise


async def collect_and_validate_api_keys(user_id: str) -> Dict[str, str]:
    """Collect API keys with real-time validation"""
    from services.database.session_factory import AsyncSessionFactory
    from services.security.user_api_key_service import UserAPIKeyService

    print("\n3. API Keys")
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
            # Validate with provider API (uses #228 infrastructure)
            async with AsyncSessionFactory.session_scope() as session:
                # Store the key first
                await service.store_user_key(
                    user_id=user_id,
                    provider="openai",
                    api_key=openai_key,
                    session=session,
                    validate=True,  # This will validate during store
                )
                await session.commit()

            # If we got here, validation succeeded
            print("   ✓ Valid (gpt-4 access confirmed)")
            stored_keys["openai"] = openai_key
            break

        except ValueError as e:
            # Validation failed
            print(f"   ✗ {str(e)}")
            print("   Please check your key and try again.")
        except Exception as e:
            print(f"   ✗ Validation error: {e}")
            print("   Please check your key and try again.")

    # Anthropic (optional)
    print("\n   Anthropic API key (optional, press Enter to skip):")
    anthropic_key = getpass("   Enter key (sk-ant-...): ")

    if anthropic_key:
        print("   Validating...")
        try:
            async with AsyncSessionFactory.session_scope() as session:
                await service.store_user_key(
                    user_id=user_id,
                    provider="anthropic",
                    api_key=anthropic_key,
                    session=session,
                    validate=True,
                )
                await session.commit()

            print("   ✓ Valid (claude-3.5 access confirmed)")
            stored_keys["anthropic"] = anthropic_key

        except ValueError as e:
            print(f"   ✗ {str(e)}. Skipping Anthropic setup.")
        except Exception as e:
            print(f"   ✗ Validation error: {e}. Skipping Anthropic setup.")
    else:
        print("   Skipped (you can add this later)")

    # GitHub (optional)
    print("\n   GitHub token (optional, press Enter to skip):")
    github_token = getpass("   Enter token (ghp_...): ")

    if github_token:
        try:
            async with AsyncSessionFactory.session_scope() as session:
                await service.store_user_key(
                    user_id=user_id,
                    provider="github",
                    api_key=github_token,
                    session=session,
                    validate=False,  # Skip validation for GitHub (expensive)
                )
                await session.commit()

            print("   ✓ GitHub token saved (validation will happen on first use)")
            stored_keys["github"] = github_token
        except Exception as e:
            print(f"   ✗ Error saving GitHub token: {e}. Skipping GitHub setup.")
    else:
        print("   Skipped (you can add this later)")

    return stored_keys


async def run_setup_wizard():
    """Main setup wizard entry point"""

    print("\n" + "=" * 50)
    print("Welcome to Piper Morgan Alpha!")
    print("=" * 50)
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
            if not checks["Python 3.9+"]:
                print("  • Install Python 3.9+: https://www.python.org/downloads/")
                print("  • Recommended: Python 3.11+ for best compatibility")
            if not checks["Port 8001 available"]:
                print("  • Free up port 8001 or stop other Piper Morgan instances")
                print("  • Run: lsof -i :8001 to see what's using the port")
            if not checks["Database accessible"]:
                print("  • Ensure database is running: docker-compose up -d db")
                print("  • Wait 10 seconds for database to start")

            return False

        # Phase 2: Create user first (need user_id for API keys)
        user = await create_user_account()

        # Phase 3: API keys
        api_keys = await collect_and_validate_api_keys(user.id)

        # Phase 4: Success!
        print("\n" + "=" * 50)
        print("✅ Setup Complete!")
        print("=" * 50)

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
        print("  • Documentation: https://pmorgan.tech")
        print("  • Report bugs: https://github.com/mediajunkie/piper-morgan/issues")

        return True

    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        return False
    except Exception as e:
        print(f"\n\n❌ Setup failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Allow running directly
    success = asyncio.run(run_setup_wizard())
    sys.exit(0 if success else 1)
