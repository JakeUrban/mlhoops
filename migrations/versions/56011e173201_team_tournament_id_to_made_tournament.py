"""team tournament_id to made_tournament

Revision ID: 56011e173201
Revises: b630997287b3
Create Date: 2017-08-20 17:27:22.351190

"""
from alembic import op
from sqlalchemy import Boolean, Column, ForeignKey, Integer


# revision identifiers, used by Alembic.
revision = '56011e173201'
down_revision = 'b630997287b3'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('teams_ibfk_2', 'teams', type_='foreignkey')
    op.drop_column('teams', 'tournament_id')
    op.add_column('teams', Column('made_tournament', Boolean))


def downgrade():
    op.drop_column('teams', 'made_tournament')
    op.add_column('teams', Column('tournament_id', Integer,
                                  ForeignKey('tournaments.id')))
