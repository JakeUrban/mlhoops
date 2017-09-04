from mock import patch, MagicMock
from mlhoops.db.init_db import init_db_data
from mlhoops.models import Team, Tournament, Game, Player, Season


empty_mock = MagicMock(return_value='')


@patch('mlhoops.models.team.team_stats_path', new=empty_mock)
@patch('mlhoops.models.game.game_stats_path', new=empty_mock)
@patch('mlhoops.models.player.player_stats_path', new=empty_mock)
@patch('mlhoops.db.init_db.session')
def test_init_db_data(patch_session, test_engine, session):
    patch_session.return_value = session()
    init_db_data(test_engine)
    season = session().query(Season).first()
    teams = session().query(Team).all()
    tournament = session().query(Tournament).first()
    players = session().query(Player).all()
    game = session().query(Game).first()
    for team in teams:
        assert team.season_id == season.id
    ids = [team.id for team in teams]
    assert set(ids) == set([game.team_one, game.team_two])
    assert set(ids) == set([players[0].team_id, players[1].team_id])
    assert tournament.season_id == season.id
