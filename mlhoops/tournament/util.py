from mlhoops.models.tournament import Tournament
from mlhoops.models.game import Game
from mlhoops.models.team import Team
from mlhoops.db import session


class BracketNode():
    """
    A node within the TournamentBracket
    """
    def __init__(self, game):
        self.game = game
        home_team = session().query(Team).get(game.home_team)
        away_team = session().query(Team).get(game.away_team)
        self.winner, self.loser = ((home_team, away_team) if
                                   game.home_team_score > game.away_team_score
                                   else (away_team, home_team))
        self.winner_previous_game = None
        self.loser_previous_game = None


class TournamentBracket():
    """
    A tree structure representing a tournament bracket
    """
    def __init__(self, champion_team, games):
        self.champion = champion_team
        self.root = self.create_bracket(games)

    def create(self, games):
        root = BracketNode(games[0])
        del games[0]
        return self.create_helper(root, games)

    def create_helper(self, cur, games):
        winner_set, loser_set = False, False
        if games:
            for i, g in enumerate(games):
                if winner_set and loser_set:
                    break
                elif g.home_team == cur.winner or g.away_team == cur.winner:
                    del games[i]
                    g = BracketNode(g)
                    cur.winner_previous_game = self.create_helper(g, games)
                    winner_set = True
                elif g.home_team == cur.loser or g.away_team == cur.loser:
                    del games[i]
                    g = BracketNode(g)
                    cur.loser_previous_game = self.create_helper(g, games)
                    loser_set = True
        return cur


def get_bracket(tournament_id):
    tournament = session().query(Tournament).get(tournament_id)
    champion = session().query(Team).get(tournament.champion_id)
    games = session().query(Game)\
                     .filter(Game.tournament_id == tournament.id)\
                     .order_by(Game.date_played).all()
    return TournamentBracket(champion, games)
