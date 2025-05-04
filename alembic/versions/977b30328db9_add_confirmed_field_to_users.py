"""add confirmed field to users

Revision ID: 977b30328db9
Revises: f544f814eb7b
Create Date: 2025-05-04 20:11:46.709037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '977b30328db9'
down_revision: Union[str, None] = 'f544f814eb7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
