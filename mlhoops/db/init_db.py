from datetime import datetime

from alembic import command
from alembic.config import Config

from mlhoops.db import Base, engine, session
from mlhoops.models import Team, Player, Season, Tournament, Game


Base.metadata.reflect(bind=engine)


def drop_db():
    tables = Base.metadata.tables.copy()
    tables.pop('alembic_version')
    Base.metadata.drop_all(tables=list(tables.values()))


def init_db():
    alembic_cfg = Config('alembic.ini')
    command.stamp(alembic_cfg, "head")
    Base.metadata.create_all(engine)


def init_db_data():
    season_data = [{'year': 2016}]
    team_data = [
        {'name': 'Oregon'},
        {'name': 'Oregon State'}
    ]
    game_data = [
        {'date_played': datetime.utcnow(), 'tournament_game': True,
         'home_team_score': 100, 'away_team_score': 52,
         'home_team': team_data[0], 'away_team': team_data[1],
         'season': season_data[0]}
    ]
    player_data = [
        {'name': 'Jordan Bell', 'team_name': 'Oregon'},
        {'name': 'Ronnie Stacy', 'team_name': 'Oregon State'}
    ]
    for season in season_data:
        season = Season(season['year'])
        session().add(season)
        session().flush()

        tournament = Tournament(season.id)
        session().add(tournament)
        session().flush()

        for team in team_data:
            team = Team(team['name'], season.id, tournament.id)
            session().add(team)
            session().flush()

            for player in player_data:
                if player['team_name'] == team.name:
                    player = Player(player['name'], team.id)
                    session().add(player)
                    session().flush()

    # need to commit so we can query team table
    session().commit()

    for game in game_data:
        game['home_team'] = session().query(Team).\
            filter(Team.name == game['home_team']['name']).first().id
        game['away_team'] = session().query(Team).\
            filter(Team.name == game['away_team']['name']).first().id
        game['season'] = session().query(Season).\
            filter(Season.year == game['season']['year']).first().id
        game = Game(**game)
        session().add(game)
        session().flush()

    session().commit()


if __name__ == '__main__':
    drop_db()
    init_db()
    init_db_data()
    session().close()
