"""merge heads for action_humanizations

Revision ID: 3659cb18c317
Revises: 8ef0aa7cbc90, 96a50c4771aa
Create Date: 2025-07-13 12:57:07.519163

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3659cb18c317"
down_revision: Union[str, Sequence[str], None] = ("8ef0aa7cbc90", "96a50c4771aa")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
