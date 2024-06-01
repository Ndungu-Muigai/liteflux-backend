"""Modified the image URL string length

Revision ID: 972afd268aac
Revises: 9385d3ef384b
Create Date: 2024-06-01 23:43:02.837323

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '972afd268aac'
down_revision = '9385d3ef384b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('image_url', sa.String(length=250), nullable=False))
    op.drop_column('images', 'image_blob')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('image_blob', postgresql.BYTEA(), autoincrement=False, nullable=False))
    op.drop_column('images', 'image_url')
    # ### end Alembic commands ###