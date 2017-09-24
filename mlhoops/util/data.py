import csv
from mlhoops.scrapers import TournamentScraper, GameScraper, TeamScraper
from mlhoops.models import Season, Tournament, Game, Team, Player
from mlhoops.models.util.game import game_stats_path
from mlhoops.models.util.team import team_stats_path
from mlhoops.models.util.player import player_stats_path
from mlhoops.db import session


def get_and_insert_data(year):
    ts = TournamentScraper()
    gs = GameScraper()
    team_s = TeamScraper()

    games, teams, final_four, champion = ts.get_tournament_info(year)

    season = Season(year)
    session().add(season)
    session().flush()

    tournament = Tournament(season.id)
    session().add(tournament)
    session().flush()

    for team in teams.items():
        print(team)
        wins, losses, stats_table = team_s.get_team_info(team[1][0])
        print(stats_table)

        t = Team(team[0], season.id, made_tournament=True, bracket=team[1][2],
                 seed=team[1][1], wins=wins, losses=losses)
        session().add(t)
        session().flush()

        if t.name == champion:
            print("champion: " + str(champion))
            tournament.champion_id = t.id
            session().flush()

        player_info = team_s.get_player_info(team[1][0])
        print(player_info[0])
        for player in player_info[1].items():
            print(player)
            session().add(Player(player[0], t.id))
            session().flush()

    for idx in range(len(games)):
        g = gs.get_game_info(games[idx][-1], games[idx][:-1])
        print(g)
        session().add(Game(g[0], g[1], season.id, g[4], team_one_score=g[2],
                           team_two_score=g[3], tournament_id=tournament.id))
        session().flush()

        g_stats = gs.get_game_stats(games[idx][-1])
        print(g_stats)
