"""new column honorific

Revision ID: d9b7b5cf6d5c
Revises: bb24a05647a0
Create Date: 2024-12-07 12:17:29.440753

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'd9b7b5cf6d5c'
down_revision = 'bb24a05647a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('users', sa.Column('honorific', sa.String()))
    # pass
    # op.execute("ALTER TABLE users ADD COLUMN honorific ENUM('MR', 'MRS', 'MS') NOT NULL")
    # ALTER TABLE your_table ADD COLUMN new_enum_column ENUM('value1', 'value2', 'value3')
    # op.add_column('users', sa.Column('honorific', sa.Enum('MR', 'MRS', 'MS', name='honorific'), nullable=False))
    pass
    
    # honorific_status = postgresql.ENUM('MR', 'MRS', 'MS', name='honorific')
    # honorific_status.create(op.get_bind())

    # op.add_column('users', sa.Column('honorific', sa.Enum('MR', 'MRS', 'MS', name='honorific_status'), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'honorific')
    # ### end Alembic commands ###
