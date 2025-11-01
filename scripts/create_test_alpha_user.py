"""
Quick script to create a test alpha user for development/testing.

This is a simplified version for quick user creation. For production,
use the full setup wizard.
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.database.connection import db
from services.database.models import AlphaUser


async def create_test_user(username: str = "xian", email: str = "xian@test.local"):
    """
    Create a test alpha user.

    Args:
        username: Username for the alpha user
        email: Email for the alpha user
    """
    print("=" * 70)
    print(f"Creating Test Alpha User: {username}")
    print("=" * 70)
    print()

    # Initialize database
    await db.initialize()

    async with await db.get_session() as session:
        try:
            # Check if user already exists
            from sqlalchemy import select

            result = await session.execute(select(AlphaUser).where(AlphaUser.username == username))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"⚠️  User '{username}' already exists")
                print(f"   User ID: {existing_user.id}")
                print(f"   Email: {existing_user.email}")
                print()
                return str(existing_user.id)

            # Create new user
            print(f"Creating user '{username}'...")
            new_user = AlphaUser(
                username=username,
                email=email,
                display_name=username.title(),
                is_active=True,
                is_verified=True,
                alpha_wave=1,  # Wave 1 (internal alpha)
                test_start_date=datetime.now(),
                preferences={},  # Empty preferences, will be populated by migration
                notes=f"Test user created for Issue #280 development",
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            print(f"✅ User created successfully")
            print(f"   User ID: {new_user.id}")
            print(f"   Username: {new_user.username}")
            print(f"   Email: {new_user.email}")
            print(f"   Display Name: {new_user.display_name}")
            print(f"   Alpha Wave: {new_user.alpha_wave}")
            print()

            return str(new_user.id)

        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            import traceback

            traceback.print_exc()
            return None


async def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Create test alpha user")
    parser.add_argument("--username", default="xian", help="Username (default: xian)")
    parser.add_argument(
        "--email", default="xian@test.local", help="Email (default: xian@test.local)"
    )

    args = parser.parse_args()

    result = await create_test_user(args.username, args.email)

    if result:
        print("✅ Ready for migration!")
        print(f"   Run: python scripts/migrate_personal_data_to_xian.py")
        sys.exit(0)
    else:
        print("❌ Failed to create user")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
