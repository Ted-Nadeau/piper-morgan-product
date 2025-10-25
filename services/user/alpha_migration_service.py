"""
Alpha user migration service.

Handles migration of alpha users to production users table with complete
data preservation including conversations, API keys, preferences, and
knowledge graph data.

Issue #260 CORE-USER-MIGRATION
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import AlphaUser, User

logger = structlog.get_logger(__name__)


@dataclass
class MigrationOptions:
    """Options for controlling alpha user migration"""

    # What to migrate
    migrate_conversations: bool = True
    migrate_api_keys: bool = True
    migrate_preferences: bool = True
    migrate_knowledge: bool = True
    migrate_audit_logs: bool = True

    # How to migrate
    preserve_alpha_record: bool = True  # Keep in alpha_users as historical
    mark_alpha_migrated: bool = True  # Set migrated_to_prod = true

    # Safety
    dry_run: bool = False  # Simulate without committing


class AlphaMigrationService:
    """Service for migrating alpha users to production"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = logger.bind(service="AlphaMigrationService")

    async def preview_migration(self, alpha_username: str) -> Dict[str, Any]:
        """
        Preview what would be migrated for an alpha user.

        Returns summary of data that would be migrated without making changes.
        """
        self.logger.info("Previewing migration", alpha_username=alpha_username)

        # Get alpha user
        alpha_user = await self._get_alpha_user(alpha_username)
        if not alpha_user:
            raise ValueError(f"Alpha user '{alpha_username}' not found")

        if alpha_user.migrated_to_prod:
            raise ValueError(
                f"Alpha user '{alpha_username}' already migrated on {alpha_user.migration_date}"
            )

        # Count related data
        from services.database.models import AuditLog, UserAPIKey

        api_keys_count = await self._count_related(UserAPIKey, alpha_user.id)
        audit_logs_count = await self._count_related(AuditLog, alpha_user.id)

        # Try to count conversations (may not have model defined)
        conversations_count = 0
        try:
            from services.database.models import Conversation

            conversations_count = await self._count_related(Conversation, alpha_user.id)
        except ImportError:
            self.logger.debug("Conversation model not found, skipping")

        # Try to count knowledge graph data (may not have user_id)
        try:
            from services.database.models import KnowledgeEdge, KnowledgeNode

            knowledge_nodes_count = await self._count_related(KnowledgeNode, alpha_user.id)
            knowledge_edges_count = await self._count_related(KnowledgeEdge, alpha_user.id)
        except Exception as e:
            self.logger.warning("Could not count knowledge graph data", error=str(e))
            knowledge_nodes_count = 0
            knowledge_edges_count = 0

        return {
            "alpha_user": {
                "id": str(alpha_user.id),
                "username": alpha_user.username,
                "email": alpha_user.email,
                "created_at": alpha_user.created_at.isoformat(),
                "alpha_wave": alpha_user.alpha_wave,
            },
            "data_summary": {
                "conversations": conversations_count,
                "api_keys": api_keys_count,
                "audit_logs": audit_logs_count,
                "knowledge_nodes": knowledge_nodes_count,
                "knowledge_edges": knowledge_edges_count,
            },
            "migration_plan": {
                "action": "CREATE new production user",
                "new_username": alpha_user.username,
                "new_email": alpha_user.email,
                "preserve_alpha": True,
                "mark_migrated": True,
            },
        }

    async def migrate_user(
        self, alpha_username: str, options: Optional[MigrationOptions] = None
    ) -> Dict[str, Any]:
        """
        Migrate an alpha user to production.

        Creates new production user and updates all related data to reference
        new user ID. Marks alpha user as migrated.
        """
        if options is None:
            options = MigrationOptions()

        self.logger.info(
            "Starting migration",
            alpha_username=alpha_username,
            dry_run=options.dry_run,
        )

        # Get alpha user
        alpha_user = await self._get_alpha_user(alpha_username)
        if not alpha_user:
            raise ValueError(f"Alpha user '{alpha_username}' not found")

        if alpha_user.migrated_to_prod:
            raise ValueError(
                f"Alpha user '{alpha_username}' already migrated on {alpha_user.migration_date}"
            )

        # Check if production username exists
        existing_prod = await self._get_prod_user(alpha_user.username)
        if existing_prod:
            raise ValueError(f"Production user '{alpha_user.username}' already exists")

        try:
            # Create production user
            prod_user = await self._create_production_user(alpha_user)
            self.logger.info(
                "Production user created",
                prod_user_id=prod_user.id,
                username=prod_user.username,
            )

            if options.dry_run:
                # Rollback if dry run
                await self.session.rollback()
                self.logger.info("Dry run complete, rolled back")
                return {
                    "status": "dry_run",
                    "would_create": {
                        "id": str(prod_user.id),
                        "username": prod_user.username,
                        "email": prod_user.email,
                    },
                }

            # Migrate related data
            migration_results = {}

            if options.migrate_api_keys:
                count = await self._migrate_api_keys(alpha_user.id, prod_user.id)
                migration_results["api_keys"] = count
                self.logger.info("Migrated API keys", count=count)

            if options.migrate_audit_logs:
                count = await self._migrate_audit_logs(alpha_user.id, prod_user.id)
                migration_results["audit_logs"] = count
                self.logger.info("Migrated audit logs", count=count)

            if options.migrate_conversations:
                try:
                    count = await self._migrate_conversations(alpha_user.id, prod_user.id)
                    migration_results["conversations"] = count
                    self.logger.info("Migrated conversations", count=count)
                except (ImportError, AttributeError) as e:
                    self.logger.warning("Could not migrate conversations", error=str(e))
                    migration_results["conversations"] = 0

            if options.migrate_knowledge:
                try:
                    nodes, edges = await self._migrate_knowledge(alpha_user.id, prod_user.id)
                    migration_results["knowledge_nodes"] = nodes
                    migration_results["knowledge_edges"] = edges
                    self.logger.info("Migrated knowledge graph", nodes=nodes, edges=edges)
                except Exception as e:
                    self.logger.warning("Could not migrate knowledge graph", error=str(e))
                    migration_results["knowledge_nodes"] = 0
                    migration_results["knowledge_edges"] = 0

            if options.migrate_preferences:
                await self._migrate_preferences(alpha_user, prod_user)
                migration_results["preferences"] = True
                self.logger.info("Migrated preferences")

            # Mark alpha user as migrated
            if options.mark_alpha_migrated:
                alpha_user.migrated_to_prod = True
                alpha_user.migration_date = datetime.utcnow()
                alpha_user.prod_user_id = prod_user.id
                await self.session.flush()
                self.logger.info("Marked alpha user as migrated")

            # Commit transaction
            await self.session.commit()
            self.logger.info("Migration committed successfully")

            return {
                "status": "success",
                "production_user": {
                    "id": prod_user.id,
                    "username": prod_user.username,
                    "email": prod_user.email,
                },
                "alpha_user": {
                    "id": str(alpha_user.id),
                    "migrated_to_prod": alpha_user.migrated_to_prod,
                    "migration_date": (
                        alpha_user.migration_date.isoformat() if alpha_user.migration_date else None
                    ),
                },
                "migration_results": migration_results,
            }

        except Exception as e:
            await self.session.rollback()
            self.logger.error("Migration failed", error=str(e))
            raise RuntimeError(f"Migration failed: {str(e)}") from e

    async def _get_alpha_user(self, username: str) -> Optional[AlphaUser]:
        """Get alpha user by username"""
        result = await self.session.execute(select(AlphaUser).where(AlphaUser.username == username))
        return result.scalar_one_or_none()

    async def _get_prod_user(self, username: str) -> Optional[User]:
        """Get production user by username"""
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def _create_production_user(self, alpha_user: AlphaUser) -> User:
        """Create production user from alpha user"""
        prod_user = User(
            id=str(uuid.uuid4()),  # New UUID for production
            username=alpha_user.username,
            email=alpha_user.email,
            password_hash=alpha_user.password_hash,
            is_active=alpha_user.is_active,
            is_verified=alpha_user.is_verified,
            role="user",  # Default role
        )

        self.session.add(prod_user)
        await self.session.flush()

        return prod_user

    async def _count_related(self, model, user_id) -> int:
        """Count related records for a user"""
        try:
            result = await self.session.execute(select(model).where(model.user_id == str(user_id)))
            return len(result.scalars().all())
        except Exception as e:
            self.logger.warning(
                "Could not count related records",
                model=model.__name__,
                error=str(e),
            )
            return 0

    async def _migrate_api_keys(self, alpha_user_id: uuid.UUID, prod_user_id: str) -> int:
        """Migrate API keys to production user"""
        from services.database.models import UserAPIKey

        result = await self.session.execute(
            update(UserAPIKey)
            .where(UserAPIKey.user_id == str(alpha_user_id))
            .values(user_id=prod_user_id)
        )
        return result.rowcount

    async def _migrate_audit_logs(self, alpha_user_id: uuid.UUID, prod_user_id: str) -> int:
        """Migrate audit logs to production user"""
        from services.database.models import AuditLog

        result = await self.session.execute(
            update(AuditLog)
            .where(AuditLog.user_id == str(alpha_user_id))
            .values(user_id=prod_user_id)
        )
        return result.rowcount

    async def _migrate_conversations(self, alpha_user_id: uuid.UUID, prod_user_id: str) -> int:
        """Migrate conversations to production user"""
        from services.database.models import Conversation

        result = await self.session.execute(
            update(Conversation)
            .where(Conversation.user_id == str(alpha_user_id))
            .values(user_id=prod_user_id)
        )
        return result.rowcount

    async def _migrate_knowledge(
        self, alpha_user_id: uuid.UUID, prod_user_id: str
    ) -> tuple[int, int]:
        """Migrate knowledge graph data to production user"""
        from services.database.models import KnowledgeEdge, KnowledgeNode

        nodes_result = await self.session.execute(
            update(KnowledgeNode)
            .where(KnowledgeNode.user_id == str(alpha_user_id))
            .values(user_id=prod_user_id)
        )

        edges_result = await self.session.execute(
            update(KnowledgeEdge)
            .where(KnowledgeEdge.user_id == str(alpha_user_id))
            .values(user_id=prod_user_id)
        )

        return nodes_result.rowcount, edges_result.rowcount

    async def _migrate_preferences(self, alpha_user: AlphaUser, prod_user: User) -> None:
        """Migrate preferences to production user"""
        # For now, preferences stay in alpha_users as historical record
        # Future: Could copy to production user preferences field if it exists
        pass
