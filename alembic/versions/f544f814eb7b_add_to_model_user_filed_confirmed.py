"""add to model User filed confirmed

Revision ID: f544f814eb7b
Revises: bc27b61d3bcd
Create Date: 2025-05-04 20:09:47.315567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f544f814eb7b'
down_revision: Union[str, None] = 'bc27b61d3bcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema: add 'confirmed' column to users."""
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), server_default='false', nullable=False))
    
def downgrade() -> None:
    """Downgrade schema: remove 'confirmed' column from users."""
    op.drop_column('users', 'confirmed')