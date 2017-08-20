"""tournament_game to id

Revision ID: ba8e2c013873
Revises: b8a355239fcc
Create Date: 2017-08-20 10:59:29.935691

"""
from alembic import op
from sqlalchemy import ForeignKey, Boolean, Column, Integer


# revision identifiers, used by Alembic.
revision = 'ba8e2c013873'
down_revision = 'b8a355239fcc'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('games', 'tournament_game')
    op.add_column('games', Column('tournament_id', Integer,
                                  ForeignKey('tournaments.id')))


def downgrade():
    op.drop_constraint('games_ibfk_4', 'games', type_='foreignkey')
    op.drop_column('games', 'tournament_id')
    op.add_column('games', Column('tournament_game', Boolean, nullable=False))
