"""Change stats_file column to stats

Revision ID: acdfe84c7fcf
Revises: e29eea5d940e
Create Date: 2017-09-04 09:37:16.665244

"""
from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = 'acdfe84c7fcf'
down_revision = 'e29eea5d940e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('games', 'stats_file')
    op.drop_column('teams', 'stats_file')
    op.drop_column('players', 'stats_file')
    op.add_column('games', Column('stats_path', String(255), nullable=False))
    op.add_column('teams', Column('stats_path', String(255), nullable=False))
    op.add_column('players', Column('stats_path', String(255), nullable=False))


def downgrade():
    op.drop_column('games', 'stats_path')
    op.drop_column('teams', 'stats_path')
    op.drop_column('players', 'stats_path')
    op.add_column('games', Column('stats_file', String(255), nullable=False))
    op.add_column('teams', Column('stats_file', String(255), nullable=False))
    op.add_column('players', Column('stats_file', String(255), nullable=False))
