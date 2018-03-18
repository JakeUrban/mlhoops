from mlhoops.db import session
from mlhoops.models import Team, Game, Season

from sqlalchemy import or_


def team_games_before(t, g):
    return session().query(Game)\
                .filter(Game.date_played < g.date_played,
                        or_(Game.team_one == t.id,
                            Game.team_two == t.id))


def last_year(t):
    t_season = session().query(Season).filter(Season.id == t.season_id).first()
    last_year_t = session().query(Team).join(Season)\
        .filter(Team.name == t.name,
                Season.year == t_season.year-1).first()
    return last_year_t


def all_games(year=None):
    q = session().query(Game)
    if year:
        q = q.join(Season).filter(Season.year == year)
    return q.all()


def get_teams(game):
    t1 = session().query(Team).filter(Team.id == game.team_one).first()
    t2 = session().query(Team).filter(Team.id == game.team_two).first()
    return t1, t2


def num_games(team, year=None, season_id=None):
    if (year and season_id) or (not (year or season_id)):
        raise ValueError("Must pass year or season_id")
    q = session().query(Game).join(Season)\
        .filter(or_(Game.team_one == team.id,
                    Game.team_two == team.id))
    if year:
        q = q.filter(Season.year == year)
    if season_id:
        q = q.filter(Season.id == season_id)
    return q.count()
