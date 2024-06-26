"""Modified the orders table to match the frontend

Revision ID: 0cfc394cd05d
Revises: 934ca724a1bd
Create Date: 2024-05-29 20:08:15.361662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cfc394cd05d'
down_revision = '934ca724a1bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('county', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('sub_county', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('ward', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('street', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'street')
    op.drop_column('orders', 'ward')
    op.drop_column('orders', 'sub_county')
    op.drop_column('orders', 'county')
    # ### end Alembic commands ###
