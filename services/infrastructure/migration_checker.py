"""
Migration Checker Service

Issue #605: Validates that all database migrations have been applied.
Prevents cryptic errors like "column does not exist" during setup.
"""

import asyncio
from typing import List, Optional

import structlog

logger = structlog.get_logger(__name__)


async def check_pending_migrations() -> List[str]:
    """
    Check for pending database migrations.

    Returns:
        List of pending migration revision IDs (empty if all applied)
    """
    try:
        import os

        from sqlalchemy import create_engine, text

        from alembic import command
        from alembic.config import Config
        from alembic.runtime.migration import MigrationContext
        from alembic.script import ScriptDirectory

        # Get database URL from environment
        db_url = os.getenv(
            "DATABASE_URL", "postgresql://piper:piperpass@localhost:5433/piper_morgan"
        )

        # For async drivers, convert to sync for migration check
        if db_url.startswith("postgresql+asyncpg://"):
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

        # Get alembic config
        alembic_cfg = Config("alembic.ini")
        script = ScriptDirectory.from_config(alembic_cfg)

        # Get all available revisions
        revisions = list(script.walk_revisions())
        head_revision = script.get_current_head()

        # Connect to database and check current revision
        engine = create_engine(db_url)

        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            current_revision = context.get_current_revision()

        engine.dispose()

        # If no migrations applied yet, all are pending
        if current_revision is None:
            pending = [rev.revision for rev in revisions]
            logger.info(
                "migration_check_complete",
                current=None,
                head=head_revision,
                pending_count=len(pending),
            )
            return pending

        # If current == head, no pending migrations
        if current_revision == head_revision:
            logger.debug("migration_check_complete", status="up_to_date")
            return []

        # Find pending migrations (everything between current and head)
        pending = []
        found_current = False
        for rev in reversed(list(revisions)):
            if rev.revision == current_revision:
                found_current = True
                continue
            if found_current:
                pending.append(rev.revision)

        logger.info(
            "migration_check_complete",
            current=current_revision,
            head=head_revision,
            pending_count=len(pending),
        )
        return pending

    except ImportError as e:
        # Alembic not installed - skip check
        logger.warning("migration_check_skipped", reason="alembic not installed", error=str(e))
        return []
    except Exception as e:
        # Database not accessible - might be first run
        error_str = str(e).lower()
        if "connect" in error_str or "refused" in error_str:
            # Database not running - let normal startup handle it
            logger.debug("migration_check_skipped", reason="database not accessible")
            return []
        if "alembic_version" in error_str:
            # Issue #609: Table doesn't exist - fresh database, all migrations pending
            # Return all migrations as pending to force user to run alembic upgrade head
            try:
                alembic_cfg = Config("alembic.ini")
                script = ScriptDirectory.from_config(alembic_cfg)
                all_revisions = list(script.walk_revisions())
                pending = [rev.revision for rev in all_revisions]
                logger.info(
                    "migration_check_complete", status="fresh_database", pending_count=len(pending)
                )
                return pending
            except Exception:
                # Can't get revision list - return placeholder to block startup
                logger.warning("migration_check_fresh_db_fallback")
                return ["<fresh database - run alembic upgrade head>"]

        logger.warning("migration_check_error", error=str(e))
        return []


async def get_current_revision() -> Optional[str]:
    """
    Get the current database migration revision.

    Returns:
        Current revision ID or None if not initialized
    """
    try:
        import os

        from sqlalchemy import create_engine

        from alembic.runtime.migration import MigrationContext

        db_url = os.getenv(
            "DATABASE_URL", "postgresql://piper:piperpass@localhost:5433/piper_morgan"
        )

        if db_url.startswith("postgresql+asyncpg://"):
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

        engine = create_engine(db_url)

        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            revision = context.get_current_revision()

        engine.dispose()
        return revision

    except Exception as e:
        logger.warning("get_revision_error", error=str(e))
        return None
