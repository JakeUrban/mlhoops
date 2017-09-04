from datetime import datetime

from alembic import command
from alembic.config import Config

from mlhoops.db import Base, session
from mlhoops.models import Team, Player, Season, Tournament, Game


def drop_db(engine):  # pragma: no cover
    db_str = str(engine.url)
    db_name = "'" + db_str[db_str.rfind('/') + 1:] + "'"
    table_exclusion_str = "('alembic_version')"
    engine.execute("""SET FOREIGN_KEY_CHECKS = 0;
        SET GROUP_CONCAT_MAX_LEN=32768;
        SET @tables = NULL;
        SELECT GROUP_CONCAT('`', table_name, '`') INTO @tables
          FROM information_schema.tables
          WHERE table_schema = {} and table_name not in {};
        SELECT IFNULL(@tables,'dummy') INTO @tables;
        SET @tables = CONCAT('DROP TABLE IF EXISTS ', @tables);
        PREPARE stmt FROM @tables;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        SET FOREIGN_KEY_CHECKS = 1;""".format(db_name, table_exclusion_str))


def init_db(engine):
    alembic_cfg = Config('alembic.ini')
    command.upgrade(alembic_cfg, "head")
    Base.metadata.create_all(engine)


def init_db_data(engine):
    season_data = [{'year': 2016}]
    team_data = [
        {'name': 'Oregon'},
        {'name': 'Oregon State'}
    ]
    game_data = [
        {'date_played': datetime.utcnow(),
         'team_one_score': 100, 'team_two_score': 52,
         'team_one': team_data[0], 'team_two': team_data[1],
         'season': season_data[0]}
    ]
    player_data = [
        {'name': 'Jordan Bell', 'team_name': 'Oregon'},
        {'name': 'Ronnie Stacy', 'team_name': 'Oregon State'}
    ]

    season = Season(season_data[0]['year'])
    session().add(season)
    session().flush()

    for idx, team in enumerate(team_data):
        team = Team(team['name'], season.id, made_tournament=True,
                    bracket='midwest', seed=idx+1)
        session().add(team)
        session().flush()

        for player in player_data:
            if player['team_name'] == team.name:
                player = Player(player['name'], team.id)
                session().add(player)
                session().flush()

    tournament = Tournament(season.id, 1)
    session().add(tournament)
    session().flush()

    # need to commit so we can query team and season tables
    session().commit()

    for game in game_data:
        game['team_one'] = session().query(Team).\
            filter(Team.name == game['team_one']['name']).first().id
        game['team_two'] = session().query(Team).\
            filter(Team.name == game['team_two']['name']).first().id
        season = session().query(Season).\
            filter(Season.year == game['season']['year']).first()
        game['season'] = season.id
        game['tournament_id'] = tournament.id
        game = Game(**game)
        session().add(game)
        session().flush()

    session().commit()


if __name__ == '__main__':
    from mlhoops.db import engine
    Base.metadata.reflect(bind=engine)
    drop_db(engine)
    init_db()
    init_db_data()
    session().close()
