"""new enum of userrole

Revision ID: bb24a05647a0
Revises: 1e62b9d0cd06
Create Date: 2024-12-07 12:09:01.073459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb24a05647a0'
down_revision = '1e62b9d0cd06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TYPE userrole ADD VALUE 'MANAGER'")
    # op.add_column('users', sa.Column('honorific', sa.Enum('MR', 'MRS', 'MS', name='honorific'), nullable=False))
    # op.execute("ALTER TYPE honorific ADD VALUE 'MS'")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
