"""merge heads before conversation foundation

Revision ID: 7473b4231d5d
Revises: 3659cb18c317, 6m5s5d1t6500
Create Date: 2025-08-07 08:46:01.788994

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7473b4231d5d"
down_revision: Union[str, Sequence[str], None] = ("3659cb18c317", "6m5s5d1t6500")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
