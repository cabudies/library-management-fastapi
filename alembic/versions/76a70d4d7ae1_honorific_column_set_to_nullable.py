"""honorific column set to nullable

Revision ID: 76a70d4d7ae1
Revises: 91a714309001
Create Date: 2024-12-07 12:40:29.339423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76a70d4d7ae1'
down_revision = '91a714309001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE users ALTER COLUMN honorific SET NOT NULL")


def downgrade() -> None:
    pass
