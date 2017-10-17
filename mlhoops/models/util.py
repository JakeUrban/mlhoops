from mlhoops import config


def game_stats_path(game):
    dirname = '_'.join([str(game.team_one).replace(' ', '-'),
                        str(game.team_two).replace(' ', '-'),
                        str(game.date_played).replace(' ', '_')]) + '.csv'
    return config.PROJECT_ROOT + '/data/stat_files/game_data/' + dirname


def player_stats_path(player):
    dirname = '_'.join([player.name.replace(' ', '-').lower(),
                        str(player.team_id)]) + '.csv'
    return config.PROJECT_ROOT + '/data/stat_files/player_data/' + dirname


def team_stats_path(team):
    dirname = '_'.join([team.name.replace(' ', '-').lower(),
                        str(team.season_id)]) + '.csv'
    return config.PROJECT_ROOT + '/data/stat_files/team_data/' + dirname
