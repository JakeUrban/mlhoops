import pytest
from mock import patch, MagicMock
from datetime import datetime
from mlhoops.models import Season, Game, Tournament, Player, Team


empty_mock = MagicMock(return_value='')


@patch('mlhoops.models.team.team_stats_path', new=empty_mock)
@patch('mlhoops.models.game.game_stats_path', new=empty_mock)
@patch('mlhoops.models.player.player_stats_path', new=empty_mock)
def test_models(session):
    num = 1
    season = Season(num)
    session().add(season)
    session().commit()
    assert season.id is not None and season.year is num

    team_one = Team('team_one', season.id, made_tournament=True,
                    bracket='test_bracket', seed=1)
    team_two = Team('team_two', season.id, made_tournament=True,
                    bracket='test_bracket', seed=2)
    session().add(team_one)
    session().add(team_two)
    session().commit()
    assert team_one.id is not None

    tournament = Tournament(season.id, team_one.id)
    session().add(tournament)
    session().commit()
    assert tournament.id is not None

    game = Game(team_one.id, team_two.id, season.id, datetime.utcnow(),
                tournament_id=tournament.id)
    session().add(game)
    session().commit()
    assert game.id is not None

    player = Player('test_player', team_one.id)
    session().add(player)
    session().commit()
    assert player.id is not None


@patch('mlhoops.models.team.team_stats_path', new=empty_mock)
def test_tournament_team(session):
    with pytest.raises(Exception):
        team = Team('team_one', 1, made_tournament=True)
        assert team.id is not None
