"""Add content column

Revision ID: d05c69dd41a1
Revises: 81b979006b38
Create Date: 2025-02-26 19:31:17.866224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd05c69dd41a1'
down_revision: Union[str, None] = '81b979006b38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts', 'content')
    pass
