"""added stats_file columns

Revision ID: 9a6b11a72573
Revises: be658ff29719
Create Date: 2017-08-13 17:44:24.982727

"""
from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = '9a6b11a72573'
down_revision = 'be658ff29719'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('games', Column('stats_file', String(255), nullable=False))
    op.add_column('players', Column('stats_file', String(255), nullable=False))
    op.add_column('teams', Column('stats_file', String(255), nullable=False))


def downgrade():
    op.drop_column('teams', 'stats_file')
    op.drop_column('players', 'stats_file')
    op.drop_column('games', 'stats_file')
