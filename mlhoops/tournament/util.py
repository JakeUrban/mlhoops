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
        team_one = session().query(Team).get(game.team_one)
        team_two = session().query(Team).get(game.team_two)
        self.winner, self.loser = ((team_one, team_two) if
                                   game.team_one_score > game.team_two_score
                                   else (team_two, team_one))
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
        for i, g in enumerate(games):
            if winner_set and loser_set:
                break
            elif g.team_one == cur.winner or g.team_two == cur.winner:
                del games[i]
                g = BracketNode(g)
                cur.winner_previous_game = self.create_helper(g, games)
                winner_set = True
            elif g.team_one == cur.loser or g.team_two == cur.loser:
                del games[i]
                g = BracketNode(g)
                cur.loser_previous_game = self.create_helper(g, games)
                loser_set = True
        if not (winner_set and loser_set) and games:
            raise Exception("Bracket creation failed")
        else:
            return cur


def get_bracket(tournament_id):
    tournament = session().query(Tournament).get(tournament_id)
    champion = session().query(Team).get(tournament.champion_id)
    games = session().query(Game)\
                     .filter(Game.tournament_id == tournament.id)\
                     .order_by(Game.date_played).all()
    return TournamentBracket(champion, games)
