"""Modifies the schema of the products table

Revision ID: 5de2f049bf67
Revises: c9fdde188be2
Create Date: 2024-06-04 21:04:13.202364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de2f049bf67'
down_revision = 'c9fdde188be2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'delivery_address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('delivery_address', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
