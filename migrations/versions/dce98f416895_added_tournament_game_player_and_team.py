"""Added tournament, game, player, and team

Revision ID: dce98f416895
Revises: eee819d697c1
Create Date: 2017-08-13 13:41:47.023724

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime


# revision identifiers, used by Alembic.
revision = 'dce98f416895'
down_revision = 'eee819d697c1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('teams',
        Column('id', Integer, primary_key=True),
        Column('name', String(255), nullable=False, unique=True)
    )
    op.create_table('games',
        Column('id', Integer, primary_key=True),
        Column('home_team', Integer, ForeignKey('teams.id'), nullable=False),
        Column('away_team', Integer, ForeignKey('teams.id'), nullable=False),
        Column('home_team_score', Integer, nullable=False),
        Column('away_team_score', Integer, nullable=False),
        Column('season_id', Integer, ForeignKey('seasons.id'), nullable=False),
        Column('tournament_game', Boolean, nullable=False),
        Column('date_played', DateTime, nullable=False)
    )
    op.create_table('players',
        Column('id', Integer, primary_key=True),
        Column('name', String(255), unique=True, nullable=False),
        Column('team_id', Integer, ForeignKey('teams.id'), nullable=False)
    )
    op.create_table('tournaments',
        Column('id', Integer, primary_key=True),
        Column('season_id', Integer, ForeignKey('seasons.id'), nullable=False)
    )


def downgrade():
    op.drop_table('tournaments')
    op.drop_table('players')
    op.drop_table('games')
    op.drop_table('teams')
