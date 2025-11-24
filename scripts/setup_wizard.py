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

# Check for required dependencies
try:
    import sqlalchemy  # noqa: F401
except ImportError:
    print("\n❌ Error: SQLAlchemy not installed")
    print("\nPlease install dependencies first:")
    print("  pip install -r requirements.txt")
    print("\nOr if using a virtual environment:")
    print("  python3.12 -m venv venv")
    print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("  pip install -r requirements.txt")
    sys.exit(1)


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


async def start_docker_services() -> bool:
    """Start all required Docker services using docker-compose"""
    print("\n🐳 Starting Docker services...")
    print("   (First run may take 5-10 minutes to download images)")

    try:
        # Start services in detached mode (no timeout - image pulls can be slow)
        print("   📦 Pulling and starting containers...")
        process = subprocess.Popen(
            ["docker-compose", "up", "-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for process with longer timeout for image downloads
        try:
            stdout, stderr = process.communicate(timeout=600)  # 10 minutes for first-time pulls
        except subprocess.TimeoutExpired:
            process.kill()
            print("   ✗ Timeout after 10 minutes (likely network issue)")
            return False

        if process.returncode != 0:
            print(f"   ✗ Failed to start services")
            if stderr:
                print(f"   Error: {stderr}")
            return False

        print("   ✓ Containers started")

        # Wait for services to be healthy with progressive checks
        print("   ⏳ Waiting for services to be ready...")
        print("   (This can take 30-60 seconds on first run)")
        print("   ℹ️  Temporal is optional - setup will continue if it's not ready")

        max_attempts = 10  # 10 attempts x 2 seconds = 20 seconds (reduced for alpha)
        for attempt in range(max_attempts):
            await asyncio.sleep(2)

            services_ok = {
                "PostgreSQL": await check_database(),
                "Redis": await check_redis(),
                "ChromaDB": await check_chromadb(),
                "Temporal": await check_temporal(),
            }

            # Check if core services are ready (Temporal is optional)
            core_services_ready = all(services_ok[s] for s in ["PostgreSQL", "Redis", "ChromaDB"])

            if core_services_ready:
                if services_ok["Temporal"]:
                    print("   ✓ All services ready")
                else:
                    print("   ✓ Core services ready (Temporal still starting)")
                return True

            # Show progress every 10 seconds
            if (attempt + 1) % 5 == 0:
                ready = sum(1 for ok in services_ok.values() if ok)
                print(f"   ⏳ {ready}/4 services ready... (attempt {attempt + 1}/{max_attempts})")

        # Final status after timeout
        print("   ⚠  Timeout waiting for all services:")
        for name, ok in services_ok.items():
            status = "✓" if ok else "✗"
            print(f"      {status} {name}")
        print("   Services may still be starting - you can continue and they might work")
        return False

    except FileNotFoundError:
        print("   ✗ docker-compose command not found")
        print("   Please install Docker Compose: https://docs.docker.com/compose/install/")
        return False
    except Exception as e:
        print(f"   ✗ Error starting services: {e}")
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
            # Set SO_REUSEADDR to handle TIME_WAIT state after restart
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", port))
        return True
    except OSError:
        return False


async def check_service_port(host: str, port: int, service_name: str) -> bool:
    """Check if a service is accessible on a specific port"""
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=2.0)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False


async def check_redis() -> bool:
    """Check Redis connectivity"""
    return await check_service_port("localhost", 6379, "Redis")


async def check_chromadb() -> bool:
    """Check ChromaDB connectivity"""
    return await check_service_port("localhost", 8000, "ChromaDB")


async def check_temporal() -> bool:
    """Check Temporal connectivity"""
    return await check_service_port("localhost", 7233, "Temporal")


async def check_database() -> bool:
    """Check PostgreSQL database connectivity"""
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
    """Run all system checks (includes all required Docker services)"""
    print("\n1. System Check")

    checks = {
        "Docker installed": await check_docker(),
        "Python 3.9+": await check_python_version(),
        "Port 8001 available": await check_port_available(),
        "PostgreSQL (5433)": await check_database(),
        "Redis (6379)": await check_redis(),
        "ChromaDB (8000)": await check_chromadb(),
        "Temporal (7233)": await check_temporal(),
    }

    for name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"   {status} {name}")

    return checks


async def check_for_incomplete_setup() -> Any:
    """
    Check if there's an alpha user with no API keys (incomplete setup).

    Returns:
        AlphaUser object if incomplete setup found, None otherwise
    """
    from sqlalchemy import select

    from services.database.models import User as AlphaUser
    from services.database.models import UserAPIKey
    from services.database.session_factory import AsyncSessionFactory

    try:
        async with AsyncSessionFactory.session_scope() as session:
            # Find alpha users with no API keys (during alpha phase)
            result = await session.execute(
                select(AlphaUser)
                .outerjoin(UserAPIKey, AlphaUser.id == UserAPIKey.user_id)
                .where(UserAPIKey.id.is_(None))
                .order_by(AlphaUser.created_at.desc())
                .limit(1)
            )
            user = result.scalar_one_or_none()
            return user
    except Exception:
        return None


async def create_user_account() -> Any:
    """Create user account with secure password (Issue #297)"""
    from services.auth.password_service import PasswordService
    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory

    print("\n2. User Account Setup")

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
            # Delete incomplete account so user can reclaim the username
            print(f"   Removing incomplete setup for {existing_user.username}...")
            try:
                from sqlalchemy import delete

                async with AsyncSessionFactory.session_scope() as session:
                    # Delete the incomplete user account
                    await session.execute(delete(User).where(User.id == existing_user.id))
                    await session.commit()
                print(f"   ✓ Removed incomplete account")
            except Exception as e:
                print(f"   ⚠️  Could not remove incomplete account: {e}")
                print("   Note: You may need to use a different username")

            print("   Starting new setup...")
    else:
        print("   Creating your alpha tester account...")

    # Try to create alpha user, handle duplicates
    max_attempts = 3
    for attempt in range(max_attempts):
        username = input("   Username: ").strip()

        while not username:
            print("   ✗ Username is required")
            username = input("   Username: ").strip()

        email = input("   Email: ").strip()

        while not email:
            print("   ✗ Email is required")
            email = input("   Email: ").strip()

        # Prompt for password (Issue #297 - Secure password setup)
        print("\n   Create a secure password:")
        password = getpass("   Password (min 8 characters): ")

        while len(password) < 8:
            print("   ✗ Password must be at least 8 characters")
            password = getpass("   Password (min 8 characters): ")

        # Confirm password
        password_confirm = getpass("   Confirm password: ")

        while password != password_confirm:
            print("   ✗ Passwords don't match, please try again")
            password = getpass("   Password (min 8 characters): ")
            password_confirm = getpass("   Confirm password: ")

        # Hash password with bcrypt
        password_service = PasswordService()
        password_hash = password_service.hash_password(password)
        print("   ✓ Password set securely")

        # Create user account (Issue #262 - UUID migration, #297 - Password setup)
        user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=password_hash,
            role="user",
            is_active=True,
            is_verified=True,
            is_alpha=True,  # Alpha tester flag
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

    # Check keychain first (in case wizard was run before)
    print("   Checking keychain for existing key...")
    openai_key = None
    try:
        async with AsyncSessionFactory.session_scope() as session:
            existing_key = await service.retrieve_user_key(session, user_id, "openai")
            if existing_key:
                print("   ✓ Using existing key from keychain")
                stored_keys["openai"] = existing_key
                openai_key = existing_key  # Mark as found
            else:
                print("   ℹ️  No existing key found in keychain")
    except Exception as e:
        print(f"   ℹ️  Keychain check skipped ({type(e).__name__})")
        pass  # Keychain check failed, continue to other methods

    # Check for environment variable if not in keychain
    if not openai_key:
        openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        print("   ℹ️  Using OPENAI_API_KEY from environment")
        print("   Validating...")

        # Store and validate the key from environment
        try:
            async with AsyncSessionFactory.session_scope() as session:
                await service.store_user_key(
                    user_id=user_id,
                    provider="openai",
                    api_key=openai_key,
                    session=session,
                    validate=True,
                )
                await session.commit()

            print("   ✓ Valid (gpt-4 access confirmed)")
            stored_keys["openai"] = openai_key
        except ValueError as e:
            print(f"   ✗ {str(e)}")
            print("   Key from environment is invalid. Please update OPENAI_API_KEY")
            openai_key = None  # Force manual entry
        except Exception as e:
            print(f"   ✗ Validation error: {e}")
            print("   Continuing with manual entry...")
            openai_key = None  # Force manual entry

    # Manual entry loop if env var not set or failed
    while not openai_key:
        openai_key = getpass("   Enter key (sk-...): ")

        if not openai_key:
            print("   ✗ OpenAI key is required")
            print("   💡 Tip: Set OPENAI_API_KEY environment variable to avoid paste issues")
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
            openai_key = None  # Reset to retry
        except Exception as e:
            print(f"   ✗ Validation error: {e}")
            print("   Please check your key and try again.")
            openai_key = None  # Reset to retry

    # Anthropic (optional)
    print("\n   Anthropic API key (optional, press Enter to skip):")

    # Check keychain first
    print("   Checking keychain for existing key...")
    anthropic_key = None
    try:
        async with AsyncSessionFactory.session_scope() as session:
            existing_key = await service.retrieve_user_key(session, user_id, "anthropic")
            if existing_key:
                print("   ✓ Using existing key from keychain")
                stored_keys["anthropic"] = existing_key
                anthropic_key = existing_key  # Mark as found
            else:
                print("   ℹ️  No existing key found in keychain")
    except Exception as e:
        print(f"   ℹ️  Keychain check skipped ({type(e).__name__})")
        pass  # Keychain check failed, continue to other methods

    # Check for environment variable if not in keychain
    if not anthropic_key:
        anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        print("   ℹ️  Using ANTHROPIC_API_KEY from environment")
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
            print(f"   ✗ {str(e)}. Continuing with manual entry...")
            anthropic_key = None  # Force manual entry
        except Exception as e:
            print(f"   ✗ Validation error: {e}. Continuing with manual entry...")
            anthropic_key = None  # Force manual entry

    # Manual entry if env var not set or failed
    if not anthropic_key:
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

    # Check keychain first
    print("   Checking keychain for existing token...")
    github_token = None
    try:
        async with AsyncSessionFactory.session_scope() as session:
            existing_key = await service.retrieve_user_key(session, user_id, "github")
            if existing_key:
                print("   ✓ Using existing token from keychain")
                stored_keys["github"] = existing_key
                github_token = existing_key  # Mark as found
            else:
                print("   ℹ️  No existing token found in keychain")
    except Exception as e:
        print(f"   ℹ️  Keychain check skipped ({type(e).__name__})")
        pass  # Keychain check failed, continue to other methods

    # Check for environment variable if not in keychain
    if not github_token:
        github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        print("   ℹ️  Using GITHUB_TOKEN from environment")
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
            print(f"   ✗ Error saving GitHub token: {e}. Continuing with manual entry...")
            github_token = None  # Force manual entry

    # Manual entry if env var not set or failed
    if not github_token:
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

        # Check if Docker services need to be started
        # Core services (required for setup)
        core_services = [
            "PostgreSQL (5433)",
            "Redis (6379)",
            "ChromaDB (8000)",
        ]
        # Optional services (Temporal can fail without blocking setup)
        optional_services = ["Temporal (7233)"]

        services_down = [k for k in core_services if not checks.get(k, False)]
        optional_down = [k for k in optional_services if not checks.get(k, False)]

        if (services_down or optional_down) and checks.get("Docker installed", False):
            all_down = services_down + optional_down
            print(f"\n⚠️  {len(all_down)} service(s) not running:")
            for service in all_down:
                print(f"   ✗ {service}")

            # Try to start services automatically
            services_started = await start_docker_services()

            if services_started:
                # Re-check services after starting
                checks["PostgreSQL (5433)"] = await check_database()
                checks["Redis (6379)"] = await check_redis()
                checks["ChromaDB (8000)"] = await check_chromadb()
                checks["Temporal (7233)"] = await check_temporal()

                # Update services_down list (only core services)
                services_down = [k for k in core_services if not checks.get(k, False)]
                optional_down = [k for k in optional_services if not checks.get(k, False)]

                if optional_down:
                    print(f"\n   ⚠  Optional service not ready: {', '.join(optional_down)}")
                    print("   (This won't prevent setup from continuing)")

        # Check other requirements (exclude optional services from blocking)
        remaining_issues = {
            k: v
            for k, v in checks.items()
            if not v and k != "Docker installed" and k not in optional_services
        }

        if remaining_issues:
            print("\n❌ Setup cannot continue. Please fix the issues above.")
            print("\nTroubleshooting:")

            if not checks.get("Python 3.9+", True) is False:
                print("  • Install Python 3.9+: https://www.python.org/downloads/")
                print("  • Recommended: Python 3.11+ for best compatibility")
            if not checks.get("Port 8001 available", True) is False:
                print("  • Free up port 8001 or stop other Piper Morgan instances")
                print("  • Run: lsof -i :8001 to see what's using the port")

            # Service-specific troubleshooting
            if services_down:
                print("  • Docker services not running:")
                print("    1. Launch Docker Desktop application (check menu bar icon)")
                print("    2. Wait for Docker to fully start (icon stops animating)")
                print("    3. Try: docker-compose up -d")
                print("    4. Wait 30 seconds for services to start")
                print("    5. Re-run this wizard")
                print("  • After system restart:")
                print("    - Docker Desktop doesn't auto-start by default")
                print("    - You must manually launch it from Applications")

            return False

        # Phase 1.5: Initialize database schema
        print("\n" + "=" * 50)
        print("📊 Database Schema")
        print("=" * 50)
        print("   Checking for existing tables...")

        from services.database.connection import db
        from services.database.models import Base
        from services.database.session_factory import AsyncSessionFactory

        # Check if tables exist by trying a simple query (check alpha_users for alpha phase)
        try:
            async with AsyncSessionFactory.session_scope() as session:
                from sqlalchemy import text

                result = await session.execute(text("SELECT 1 FROM alpha_users LIMIT 1"))
            print("   ✓ Database tables already exist")
        except Exception:
            # Tables don't exist, create them
            print("   Creating database tables...")
            await db.initialize()
            await db.create_tables()
            print("   ✓ Database tables created")

        # Run database migrations to ensure schema is up to date
        print("   Running database migrations...")
        try:
            # Get project root (setup_wizard.py is in scripts/ subdirectory)
            # Note: os is imported at module level (line 14)
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            migration_result = subprocess.run(
                ["alembic", "upgrade", "head"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=project_root,  # Run from project root where alembic.ini lives
            )
            if migration_result.returncode == 0:
                print("   ✓ Database schema up to date")
            else:
                # Show actual error for debugging
                print(f"   ⚠️  Migration had issues:")
                if migration_result.stderr:
                    print(f"      {migration_result.stderr.strip()}")
                if migration_result.stdout:
                    print(f"      {migration_result.stdout.strip()}")
                print("   Continuing setup...")
        except subprocess.TimeoutExpired:
            print("   ⚠️  Migration timeout (taking longer than expected)")
            print("   Continuing setup...")
        except FileNotFoundError:
            print("   ⚠️  Alembic not found in PATH")
            print("   Please run 'alembic upgrade head' manually after setup")
        except Exception as e:
            print(f"   ⚠️  Unexpected error running migrations: {e}")
            print("   Please run 'alembic upgrade head' manually after setup")

        # Phase 2: Create user first (need user_id for API keys)
        user = await create_user_account()

        # Phase 3: API keys
        # Convert UUID to string for UserAPIKey foreign key compatibility
        user_id_str = str(user.id)
        api_keys = await collect_and_validate_api_keys(user_id_str)

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
        print("  1. Set your preferences:")
        print("     source venv/bin/activate")
        print("     python main.py preferences")
        print("  2. Start Piper Morgan:")
        print("     python main.py")
        print("  3. Access at: http://localhost:8001")
        print("  4. Check system status:")
        print("     python main.py status")
        print("\n  💡 Tip: All commands work best from within 'venv/bin/activate'")

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
