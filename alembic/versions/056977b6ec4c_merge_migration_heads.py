"""merge_migration_heads

Revision ID: 056977b6ec4c
Revises: b8e4f3c9a2d7, d8aeb665e878c
Create Date: 2025-11-23 20:58:18.189216

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "056977b6ec4c"
down_revision: Union[str, Sequence[str], None] = ("b8e4f3c9a2d7", "d8aeb665e878c")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
