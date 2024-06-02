"""Added image url to the images table

Revision ID: c9fdde188be2
Revises: 7a6a375f5f28
Create Date: 2024-06-02 16:16:45.342882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9fdde188be2'
down_revision = '7a6a375f5f28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('image_url', sa.String(length=250), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('images', 'image_url')
    # ### end Alembic commands ###
