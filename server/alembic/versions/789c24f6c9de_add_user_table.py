"""add user table

Revision ID: 789c24f6c9de
Revises: ec80bf0ce3e3
Create Date: 2024-04-09 11:14:04.412872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '789c24f6c9de'
down_revision: Union[str, None] = 'ec80bf0ce3e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
