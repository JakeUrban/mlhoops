def get_game_stats_file(game):
    return '_'.join([str(game.home_team), str(game.away_team),
                     str(game.date_played)])
