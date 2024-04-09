"""add content column

Revision ID: ec80bf0ce3e3
Revises: 9c97e580607a
Create Date: 2024-04-09 10:58:28.843939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec80bf0ce3e3'
down_revision: Union[str, None] = '9c97e580607a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
