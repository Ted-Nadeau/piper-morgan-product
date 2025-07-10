# scripts/init_pm009_tables.py
import asyncio
import os
import sys
from uuid import uuid4

from sqlalchemy import func, select

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Only import what we actually use
from services.database.connection import db
from services.database.models import \
    ProjectDB  # DB model for database operations
from services.domain.models import Project  # Domain model for business logic


async def main():
    print("🚀 Starting PM-009 Database Migration")
    print("=" * 50)

    print("🔧 Initializing database connection...")
    await db.initialize()

    print("🏗️ Creating all database tables...")
    await db.create_tables()
    print("✅ All tables created successfully including Project and ProjectIntegration")

    print("🎯 Creating default project...")
    try:
        session = await db.get_session()

        # Check if default already exists
        result = await session.execute(
            select(func.count(ProjectDB.id)).where(ProjectDB.is_default == True)
        )

        if result.scalar() > 0:
            print("✅ Default project already exists")
            return

        # Create default project
        default_project = Project(
            id=str(uuid4()),
            name="Piper Morgan Development",
            description="Default development project",
            is_default=True,
        )

        # Map to DB model before adding
        db_project = ProjectDB.from_domain(default_project)
        session.add(db_project)
        await session.commit()
        print(f"✅ Created default project: {default_project.name}")

    except Exception as e:
        print(f"❌ Error creating default project: {e}")
        raise
    finally:
        await db.close()

    print("✅ PM-009 migration completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
