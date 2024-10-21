"""add content column for post table

Revision ID: c191e0858360
Revises: c7657c6ad341
Create Date: 2024-10-21 06:31:58.510355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c191e0858360'
down_revision: Union[str, None] = 'c7657c6ad341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
