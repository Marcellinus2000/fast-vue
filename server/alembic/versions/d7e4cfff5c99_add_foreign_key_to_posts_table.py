"""add foreign key to posts table

Revision ID: d7e4cfff5c99
Revises: 789c24f6c9de
Create Date: 2024-04-09 11:48:17.298780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7e4cfff5c99'
down_revision: Union[str, None] = '789c24f6c9de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'],remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass