"""Add created_at and updated_at to contacts

Revision ID: 95e847cce4e3
Revises: c3eb10dff691
Create Date: 2025-05-04 15:53:58.272073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '95e847cce4e3'
down_revision: Union[str, None] = 'c3eb10dff691'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Add updated_at and modify existing columns in contacts."""
    op.add_column('contacts', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.alter_column('contacts', 'phone',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=20),
               nullable=False)
    op.alter_column('contacts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))

def downgrade() -> None:
    """Downgrade schema: Revert changes to contacts table."""
    op.alter_column('contacts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('contacts', 'phone',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=50),
               nullable=True)
    op.drop_column('contacts', 'updated_at')
