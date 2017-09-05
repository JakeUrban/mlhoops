from mlhoops.scrapers import TournamentScraper, GameScraper, TeamScraper


def get_data(year):
    ts = TournamentScraper()
    gs = GameScraper()
    team_s = TeamScraper()
    game_data, team_data, player_data = [], [], []

    games, teams, final_four, champion = ts.get_tournament_info(year)
    for idx in range(len(games)):
        print(games[idx])
        endpoint = games[idx][-1]
        games[idx] = gs.get_game_info(endpoint, games[idx][:-1])
        game_data.append((games[idx], gs.get_game_stats(endpoint)))
    for team in teams.items():
        print(team)
        wins, losses, stats_table = team_s.get_team_info(team[1][0])
        team_data.append((team, wins, losses, stats_table))
        player_data.append(team_s.get_player_info(team[1][0]))

    return champion, game_data, team_data, player_data
