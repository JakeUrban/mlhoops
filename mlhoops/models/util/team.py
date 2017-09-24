from mlhoops import config


def team_stats_path(team):
    dirname = '_'.join([team.name.replace(' ', '-').lower(),
                        str(team.season_id)])
    return config.PROJECT_ROOT + '/data/' + dirname
