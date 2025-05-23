"""change role column to string

Revision ID: 1161f87094ce
Revises: be754cc30157
Create Date: 2025-05-23 21:30:16.777666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1161f87094ce'
down_revision: Union[str, None] = 'be754cc30157'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'role',
                    existing_type=sa.String(length=50),
                    type_=postgresql.ENUM('admin', 'cook', 'manager', name='userrole'),
                    existing_nullable=False)

def downgrade() -> None:
    op.alter_column('users', 'role',
                    existing_type=postgresql.ENUM('admin', 'cook', 'manager', name='userrole'),
                    type_=sa.String(length=50),
                    existing_nullable=False)
