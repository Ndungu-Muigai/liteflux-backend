"""Modified the orders schema

Revision ID: 077f437ca25b
Revises: fac76161c5df
Create Date: 2024-06-06 21:27:05.433751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '077f437ca25b'
down_revision = 'fac76161c5df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('order_id', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'orders', ['order_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='unique')
    op.drop_column('orders', 'order_id')
    # ### end Alembic commands ###