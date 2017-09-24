from mlhoops import config


def game_stats_path(game):
    dirname = '_'.join([str(game.team_one), str(game.team_two),
                        str(game.date_played).replace(' ', '_')])
    return config.PROJECT_ROOT + '/data/' + dirname
