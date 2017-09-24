from mlhoops import config


def game_stats_path(game):
    dirname = '_'.join([str(game.team_one), str(game.team_two),
                        str(game.date_played).replace(' ', '_')])
    return config.PROJECT_ROOT + '/data/' + dirname


def player_stats_path(player):
    dirname = '_'.join([player.name.replace(' ', '-').lower(),
                        str(player.team_id)])
    return config.PROJECT_ROOT + '/data/' + dirname


def team_stats_path(team):
    dirname = '_'.join([team.name.replace(' ', '-').lower(),
                        str(team.season_id)])
    return config.PROJECT_ROOT + '/data/' + dirname
