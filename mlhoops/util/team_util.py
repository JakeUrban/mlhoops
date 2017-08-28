def get_team_stats_file(team):
    return '_'.join([team.name.replace(' ', '-').lower(), str(team.season_id)])
