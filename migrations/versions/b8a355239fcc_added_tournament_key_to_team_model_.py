"""Added tournament key to team model, added inverse relationship

Revision ID: b8a355239fcc
Revises: 9a6b11a72573
Create Date: 2017-08-15 01:03:19.775716

"""
from alembic import op
from sqlalchemy import Column, ForeignKey, Integer


# revision identifiers, used by Alembic.
revision = 'b8a355239fcc'
down_revision = '9a6b11a72573'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'teams',
        Column('tournament_id',
               Integer,
               ForeignKey('tournaments.id'),
               nullable=True))


def downgrade():
    op.drop_constraint('teams_ibfk_2', 'teams', type_='foreignkey')
    op.drop_column('teams', 'tournament_id')
