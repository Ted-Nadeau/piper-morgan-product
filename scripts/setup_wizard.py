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
import os
import socket
import subprocess
import sys
import uuid
from datetime import datetime
from getpass import getpass
from typing import Any, Dict

# Add parent directory to path for imports
sys.path.insert(0, ".")


def get_platform() -> str:
    """Detect the current platform"""
    import platform

    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"


def check_python312_available() -> bool:
    """Check if python3.12 is available on the system"""
    try:
        result = subprocess.run(
            ["python3.12", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def setup_virtual_environment() -> bool:
    """Set up Python virtual environment with requirements"""
    import os

    print("\n" + "=" * 50)
    print("🔧 Setting Up Virtual Environment")
    print("=" * 50)

    # Clean up old venv
    if os.path.exists("venv"):
        print("\n🧹 Removing old virtual environment...")
        try:
            subprocess.run(["rm", "-rf", "venv"], check=True, timeout=10)
            print("   ✓ Old venv removed")
        except Exception as e:
            print(f"   ⚠ Could not remove old venv: {e}")
            return False

    # Create new venv with python3.12
    print("\n📦 Creating virtual environment with Python 3.12...")
    try:
        subprocess.run(
            ["python3.12", "-m", "venv", "venv"],
            check=True,
            timeout=60,
        )
        print("   ✓ Virtual environment created")
    except Exception as e:
        print(f"   ✗ Failed to create venv: {e}")
        return False

    # Upgrade pip
    print("\n📥 Upgrading pip...")
    try:
        subprocess.run(
            ["venv/bin/pip", "install", "--upgrade", "pip"],
            check=True,
            timeout=60,
        )
        print("   ✓ pip upgraded")
    except Exception as e:
        print(f"   ⚠ pip upgrade had issues: {e}")

    # Install requirements
    print("\n📦 Installing dependencies (this may take 2-3 minutes)...")
    try:
        result = subprocess.run(
            ["venv/bin/pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            print("   ✓ All dependencies installed successfully!")
            return True
        else:
            print(f"   ✗ Installation failed:")
            print(result.stderr[-500:] if result.stderr else "Unknown error")
            return False
    except subprocess.TimeoutExpired:
        print("   ✗ Installation timed out (>5 minutes)")
        return False
    except Exception as e:
        print(f"   ✗ Installation failed: {e}")
        return False


def setup_ssh_key() -> bool:
    """Generate SSH key if missing and guide user to add it to GitHub"""
    import os

    print("\n" + "=" * 50)
    print("🔐 SSH Key Setup")
    print("=" * 50)

    ssh_dir = os.path.expanduser("~/.ssh")
    key_path = os.path.join(ssh_dir, "id_ed25519")

    # Check if key exists
    if os.path.exists(key_path):
        print("\n✓ SSH key already exists at ~/.ssh/id_ed25519")
        print("✓ Skipping SSH key generation")
        return True

    # Generate new key
    print("\n🔑 Generating new SSH key...")
    try:
        # Create .ssh directory if it doesn't exist
        os.makedirs(ssh_dir, mode=0o700, exist_ok=True)

        subprocess.run(
            [
                "ssh-keygen",
                "-t",
                "ed25519",
                "-f",
                key_path,
                "-N",
                "",
                "-C",
                "piper-morgan-alpha",
            ],
            check=True,
            timeout=10,
        )
        print("   ✓ SSH key generated")

        # Read and copy public key
        pub_key_path = key_path + ".pub"
        with open(pub_key_path, "r") as f:
            pub_key = f.read().strip()

        # Copy to clipboard (platform-specific)
        platform = get_platform()
        try:
            if platform == "macos":
                subprocess.run(
                    ["pbcopy"],
                    input=pub_key.encode(),
                    check=True,
                    timeout=5,
                )
                print("   ✓ Public key copied to clipboard")
            elif platform == "windows":
                subprocess.run(
                    ["clip"],
                    input=pub_key.encode(),
                    check=True,
                    timeout=5,
                )
                print("   ✓ Public key copied to clipboard")
            # Linux: no auto-copy, just display
        except Exception as e:
            print(f"   ⚠ Could not copy to clipboard: {e}")

        # Display instructions
        print("\n" + "-" * 50)
        print("📋 Next Steps: Add SSH Key to GitHub")
        print("-" * 50)
        print("\n1. Visit: https://github.com/settings/ssh")
        print("2. Click 'New SSH key'")
        print("3. Give it a title (e.g., 'My Laptop')")
        if platform != "linux":
            print("4. The key is already copied—paste it into the 'Key' field")
        else:
            print("4. Copy and paste this key into the 'Key' field:")
            print("\n" + pub_key + "\n")
        print("5. Click 'Add SSH key'")
        print("\n6. Back in terminal, verify with:")
        print("   ssh -T git@github.com")
        print("   (You may need to type 'yes' when prompted)")

        print("\n" + "-" * 50)
        ready = input("Have you added the SSH key to GitHub? (y/n): ").lower().strip()
        return ready == "y"

    except Exception as e:
        print(f"   ✗ Failed to generate SSH key: {e}")
        return False


async def check_docker() -> bool:
    """Check if Docker is installed and running"""
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


async def guide_docker_installation() -> bool:
    """Guide user through Docker installation with platform-specific instructions"""
    platform = get_platform()

    print("\n" + "=" * 50)
    print("🐳 Docker Installation Guide")
    print("=" * 50)

    print("\nDocker is required for Piper Morgan's database and services.")
    print("Let's get Docker installed on your system.\n")

    if platform == "macos":
        print("📱 macOS Installation:")
        print("1. Visit: https://docs.docker.com/desktop/mac/install/")
        print("2. Download Docker Desktop for Mac")
        print("3. Open the .dmg file and drag Docker to Applications")
        print("4. Launch Docker Desktop from Applications")
        print("5. Wait for Docker to start (whale icon in menu bar)")

    elif platform == "windows":
        print("🪟 Windows Installation:")
        print("1. Visit: https://docs.docker.com/desktop/windows/install/")
        print("2. Download Docker Desktop for Windows")
        print("3. Run the installer and follow the setup wizard")
        print("4. Restart your computer when prompted")
        print("5. Launch Docker Desktop and wait for it to start")

    elif platform == "linux":
        print("🐧 Linux Installation:")
        print("1. Visit: https://docs.docker.com/engine/install/")
        print("2. Choose your Linux distribution")
        print("3. Follow the installation instructions")
        print("4. Start Docker: sudo systemctl start docker")
        print("5. Enable auto-start: sudo systemctl enable docker")

    else:
        print("❓ Unknown Platform:")
        print("1. Visit: https://docs.docker.com/get-docker/")
        print("2. Choose the appropriate installer for your system")
        print("3. Follow the installation instructions")

    print("\n" + "-" * 50)
    print("After installation:")
    print("• Docker Desktop should show a green 'running' status")
    print("• You can test with: docker --version")
    print("• If you see version info, Docker is working!")

    while True:
        print("\n" + "-" * 50)
        choice = input("Have you installed Docker? (y/n/skip): ").lower().strip()

        if choice in ["y", "yes"]:
            # Test Docker installation
            if await check_docker():
                print("✅ Great! Docker is now working.")
                return True
            else:
                print("❌ Docker doesn't seem to be working yet.")
                print("💡 Try:")
                print("   • Make sure Docker Desktop is running")
                print("   • Restart Docker Desktop")
                print("   • Check Docker Desktop status")
                continue

        elif choice in ["n", "no"]:
            print("📝 No problem! Please install Docker and run setup again.")
            print("   Docker is required for Piper Morgan's database.")
            return False

        elif choice == "skip":
            print("⚠️  WARNING: Skipping Docker installation.")
            print("   Some features may not work without Docker.")
            print("   You can install Docker later and re-run setup.")

            confirm = input("Continue without Docker? (y/n): ").lower().strip()
            if confirm in ["y", "yes"]:
                return True
            else:
                continue
        else:
            print("Please enter 'y' (yes), 'n' (no), or 'skip'")
            continue


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
    """Run all system checks (database check works when in venv)"""
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
    print("\nLet's get you set up (takes about 5-10 minutes)")
    print()

    try:
        # Phase 0: Pre-flight checks (Python 3.12, venv, SSH)
        print("\n" + "=" * 50)
        print("🚀 Pre-Flight Checks")
        print("=" * 50)

        # Check Python 3.12
        print("\n1️⃣  Checking for Python 3.12...")
        if not check_python312_available():
            print("   ✗ Python 3.12 not found")
            print(
                "   📥 Please install from: https://www.python.org/downloads/release/python-31210/"
            )
            print("   ⏸  Install Python 3.12.10 and run this wizard again.")
            return False
        print("   ✓ Python 3.12 found")

        # Set up virtual environment (only if not already in one)
        in_venv = hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        )

        if not in_venv:
            print("\n2️⃣  Setting up virtual environment...")
            if not setup_virtual_environment():
                print("   ✗ Failed to set up virtual environment")
                return False

            # Restart wizard in the new venv
            print("\n🔄 Restarting wizard in virtual environment...")
            print("   (This ensures all dependencies are available)")
            venv_python = os.path.join(os.getcwd(), "venv", "bin", "python")
            os.execv(venv_python, [venv_python, "main.py", "setup"])
            # execv doesn't return - the process is replaced
        else:
            print("\n2️⃣  Virtual environment: ✓ Active")

        # Set up SSH (optional but recommended)
        print("\n3️⃣  Setting up SSH key...")
        ssh_ready = setup_ssh_key()
        if not ssh_ready:
            print("   ⚠  SSH setup skipped (you can set this up later manually)")

        # Phase 1: System checks
        print("\n" + "=" * 50)
        print("📋 System Checks")
        print("=" * 50)
        checks = await check_system()

        # Handle Docker installation separately with guided setup
        if not checks["Docker installed"]:
            print("\n🐳 Docker is not installed or not running.")
            docker_success = await guide_docker_installation()
            if not docker_success:
                print("\n❌ Setup cannot continue without Docker.")
                return False
            # Re-check Docker after guided installation
            checks["Docker installed"] = await check_docker()

        # Check other requirements
        remaining_issues = {k: v for k, v in checks.items() if not v and k != "Docker installed"}

        if remaining_issues:
            print("\n❌ Setup cannot continue. Please fix the issues above.")
            print("\nTroubleshooting:")

            if not checks.get("Python 3.9+", True) is False:
                print("  • Install Python 3.9+: https://www.python.org/downloads/")
                print("  • Recommended: Python 3.11+ for best compatibility")
            if not checks.get("Port 8001 available", True) is False:
                print("  • Free up port 8001 or stop other Piper Morgan instances")
                print("  • Run: lsof -i :8001 to see what's using the port")
            if not checks.get("Database accessible", True) is False:
                print("  • Ensure database is running: docker-compose up -d postgres")
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
