def get_player_stats_file(player):
    return '_'.join([player.name.replace(' ', '-').lower(),
                     str(player.team_id)])
