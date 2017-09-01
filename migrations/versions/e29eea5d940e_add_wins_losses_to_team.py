"""add_wins_losses_to_team

Revision ID: e29eea5d940e
Revises: d4eeb2d1903b
Create Date: 2017-08-30 19:59:37.509222

"""
from alembic import op
from sqlalchemy import Column, Integer


# revision identifiers, used by Alembic.
revision = 'e29eea5d940e'
down_revision = 'd4eeb2d1903b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('teams', Column('wins', Integer, nullable=False, default=0))
    op.add_column('teams', Column('losses', Integer, nullable=False, default=0))


def downgrade():
    op.drop_column('teams', 'wins')
    op.drop_column('teams', 'losses')
