"""Add new columns to posts table

Revision ID: 5e1844c17c31
Revises: d7e4cfff5c99
Create Date: 2024-04-09 12:01:47.308503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e1844c17c31'
down_revision: Union[str, None] = 'd7e4cfff5c99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','content')
    op.drop_column('posts','created_at')
    pass
