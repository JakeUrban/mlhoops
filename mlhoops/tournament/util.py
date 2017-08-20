from mlhoops.models.tournament import Tournament
from mlhoops.db import session


def get_tree(tournament_id):
    games = session().query(Game).filter(Game.tournament_id == tournament_id)
