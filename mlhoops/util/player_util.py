from mlhoops import config


def player_stats_path(player):
    dirname = '_'.join([player.name.replace(' ', '-').lower(),
                        str(player.team_id)])
    return config.PROJECT_ROOT + '/data/' + dirname
