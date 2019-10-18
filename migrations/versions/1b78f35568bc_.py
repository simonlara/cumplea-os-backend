"""empty message

Revision ID: 1b78f35568bc
Revises: 
Create Date: 2019-10-17 18:32:31.808497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b78f35568bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('national_id', sa.Integer(), nullable=True),
    sa.Column('lastName', sa.String(length=80), nullable=True),
    sa.Column('names', sa.String(length=80), nullable=False),
    sa.Column('sex', sa.String(length=3), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('village_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('national_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('persons')
    # ### end Alembic commands ###