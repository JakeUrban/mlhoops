from mock import MagicMock

from mlhoops.util.game_util import game_stats_path
from mlhoops.util.player_util import player_stats_path
from mlhoops import config
from mlhoops.util.team_util import team_stats_path


def test_team_stats_paths():
    team = MagicMock()
    team.name = 'Test Team'
    team.season_id = 1
    path = team_stats_path(team)
    assert path == config.PROJECT_ROOT + '/data/' + 'test-team_1'


def test_player_stats_paths():
    player = MagicMock()
    player.name = 'Marcus Mariota'
    player.team_id = 1
    path = player_stats_path(player)
    assert path == config.PROJECT_ROOT + '/data/' + 'marcus-mariota_1'


def test_game_stats_path():
    game = MagicMock()
    game.team_one = 1
    game.team_two = 2
    game.date_played = '2017-09-05 8:30:00'
    path = game_stats_path(game)
    assert path == config.PROJECT_ROOT + '/data/' + '1_2_2017-09-05_8:30:00'
