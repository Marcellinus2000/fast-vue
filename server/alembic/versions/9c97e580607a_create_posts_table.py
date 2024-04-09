"""create posts table

Revision ID: 9c97e580607a
Revises: 
Create Date: 2024-04-09 10:49:48.397907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c97e580607a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String, nullable=False)) 
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
