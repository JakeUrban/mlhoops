def get_game_stats_file(game):
    return '_'.join([str(game.team_one), str(game.team_two),
                     str(game.date_played).replace(' ', '_')])
