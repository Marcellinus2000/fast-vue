"""Add vote table

Revision ID: 6e5e484131bc
Revises: 41786bb38f55
Create Date: 2024-04-09 13:47:42.005777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e5e484131bc'
down_revision: Union[str, None] = '41786bb38f55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes', sa.Column('user_id', sa.Integer(), nullable=False), sa.Column('post_id', sa.Integer(), nullable=False), sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'), sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'), sa.PrimaryKeyConstraint('user_id', 'post_id'))
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass 
