"""Added season_id to team and defaults to game

Revision ID: be658ff29719
Revises: dce98f416895
Create Date: 2017-08-13 17:17:13.539142

"""
from alembic import op
from sqlalchemy import Column, Integer, ForeignKey


# revision identifiers, used by Alembic.
revision = 'be658ff29719'
down_revision = 'dce98f416895'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'teams',
        Column('season_id',
               Integer,
               ForeignKey('seasons.id'),
               nullable=False)
    )


def downgrade():
    op.drop_constraint('teams_ibfk_1', 'teams', type_='foreignkey')
    op.drop_column('teams', 'season_id')
