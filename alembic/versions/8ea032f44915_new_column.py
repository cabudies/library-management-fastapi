"""new column

Revision ID: 8ea032f44915
Revises: d9b7b5cf6d5c
Create Date: 2024-12-07 12:34:16.857676

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8ea032f44915'
down_revision = 'd9b7b5cf6d5c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    honorific_status = postgresql.ENUM('MR', 'MRS', 'MS', name='honorific')
    honorific_status.create(op.get_bind())

    op.add_column('users', sa.Column('honorific', honorific_status, nullable=True))


def downgrade() -> None:
    pass
