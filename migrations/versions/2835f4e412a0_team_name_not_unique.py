"""team name not unique

Revision ID: 2835f4e412a0
Revises: a623956283f2
Create Date: 2017-10-16 21:44:32.006932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2835f4e412a0'
down_revision = 'a623956283f2'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('teams', 'name')
    op.add_column('teams', sa.Column('name', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('teams', 'name')
    op.add_column('teams', sa.Column('name', sa.String(255), unique=True,
                                     nullable=True))
