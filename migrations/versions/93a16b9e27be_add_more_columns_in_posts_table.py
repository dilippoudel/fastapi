"""add more columns in posts table

Revision ID: 93a16b9e27be
Revises: 350d9efd13bc
Create Date: 2025-02-26 20:04:43.950781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93a16b9e27be'
down_revision: Union[str, None] = '350d9efd13bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE')),
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))

    pass


def downgrade() -> None:
    sa.drop_column('posts', 'published')
    sa.drop_column('posts', 'created_at')
    pass
