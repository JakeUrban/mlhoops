from datetime import datetime

from alembic import command
from alembic.config import Config

from mlhoops.db.session import engine, session
from mlhoops.db.base import Base


def drop_db():
    Base.metadata.reflect(engine)
    tables = Base.metadata.tables.copy()
    tables.pop('alembic_version')
    Base.metadata.drop_all(tables=tables.values())


def init_db():
    alembic_cfg = Config('alembic.ini')
    command.stamp(alembic_cfg, "head")
    Base.metadata.create_all(engine)


def init_db_data():
    season_data = [{'year': 2016}]
    team_data = [
        {'name': 'Oregon', 'stats_file': 'oregon.csv'},
        {'name': 'Oregon State', 'state_file': 'oregon_state.csv'}
    ]
    game_data = [
        {'date_played': datetime.utcnow(),
         'stats_file': 'oregon_v_oregon_state.csv', 'home_team_score': 100,
         'away_team_score': 52, 'tournament_game': True}
    ]
    player_data = [
        {'name': 'Jordan Bell', 'team_name': 'Oregon'},
        {'name': 'Ronnie Stacy', 'team_name': 'Oregon State'}
    ]


if __name__ == '__main__':
    drop_db()
    init_db()
    init_db_data()
