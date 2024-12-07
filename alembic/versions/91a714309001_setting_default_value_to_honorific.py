"""setting default value to honorific

Revision ID: 91a714309001
Revises: 8ea032f44915
Create Date: 2024-12-07 12:38:31.009821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91a714309001'
down_revision = '8ea032f44915'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.execute("ALTER TABLE users ALTER COLUMN honorific SET DEFAULT 'MR'")
    op.execute("UPDATE users SET honorific = 'MR' WHERE honorific IS NULL")


def downgrade() -> None:
    pass
