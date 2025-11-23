"""uuid_migration_issue_262_and_291 [DEPRECATED - REPLACED BY 3-PART MIGRATION]

⚠️  DEPRECATED: This migration has been decomposed into 3 atomic migrations:
- d8aeb665e878a: Drop FK constraints
- d8aeb665e878b: Convert column types to UUID
- d8aeb665e878c: Re-add FK constraints and cleanup

This migration is now a no-op (does nothing) and is kept only for migration history.
New migrations should use the 3-part sequence above.

ORIGINAL INTENT (now handled by 3-part migration):
Complete UUID migration for users table and merge alpha_users.
Resolves Issue #262 (UUID migration) and Issue #291 (token blacklist FK).

Revision ID: d8aeb665e878
Revises: 234aa8ec628c
Create Date: 2025-11-09 13:07:57.730803

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8aeb665e878"
down_revision: Union[str, Sequence[str], None] = "234aa8ec628c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """NO-OP: Functionality replaced by 3-part migration.

    This migration is deprecated and kept only for migration history.
    All functionality is now handled by:
    - d8aeb665e878a: Drop FK constraints
    - d8aeb665e878b: Convert column types to UUID
    - d8aeb665e878c: Re-add FK constraints and cleanup

    For new databases, use the 3-part migration sequence instead.
    """
    print("ℹ️  [DEPRECATED] Migration d8aeb665e878 is a no-op (replaced by 3-part migration)")
    print("   - Use d8aeb665e878a for dropping FK constraints")
    print("   - Use d8aeb665e878b for converting column types")
    print("   - Use d8aeb665e878c for re-adding constraints and cleanup")


def downgrade() -> None:
    """NO-OP: Downgrade handled by individual 3-part migrations.

    Since this is now a no-op, downgrade is also a no-op.
    Downgrade of individual steps is handled by:
    - d8aeb665e878c (downgrade)
    - d8aeb665e878b (downgrade)
    - d8aeb665e878a (downgrade)
    """
    print("ℹ️  [DEPRECATED] Downgrade of d8aeb665e878 is a no-op")
