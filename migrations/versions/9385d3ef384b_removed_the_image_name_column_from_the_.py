"""Removed the image name column from the image database

Revision ID: 9385d3ef384b
Revises: 0cfc394cd05d
Create Date: 2024-05-30 20:52:50.824695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9385d3ef384b'
down_revision = '0cfc394cd05d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'image_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('image_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
