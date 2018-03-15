from mlhoops.db import session
from mlhoops.models import Team, Game, Season

from sqlalchemy import or_

import pandas as pd


def season_upto(t, g, num_games=False):
    games = session().query(Game)\
                .filter(Game.date_played < g.date_played,
                        or_(Game.team_one==t.id,
                            Game.team_two==t.id)).all()  # t's games before g

    if not games:  # if this is the first game of the season
        t_season = session().query(Season).filter(Season.id==t.season_id).first()
        last_season_t = session().query(Team).join(Season)\
                            .filter(Team.name==t.name,
                                    Season.year == t_season.year-1).first()
        data = last_season_t.get_data()
        tdf = pd.DataFrame(data[1:], columns=data[0])
        if num_games:
            ng = session().query(Game).join(Season).join(Team)\
                    .filter(Season.year==t_season.year-1,
                            or_(Game.team_one==last_season_t.id,
                                Game.team_two==last_season_t.id)).count()
            return tdf, ng
        return tdf

    t_dict, opp_dict = {}, {}
    features = set(t.features).intersection(set(g.features))  # the features shared between g and t
    for feature in features:  # initializing t and t's opponent's dict
        if 'Percentage' in feature:
            continue  # not calculating percentages yet
        t_dict[feature] = 0
        opp_dict[feature] = 0

    for game in games:  # add up data from each game before g
        t1df, t2df = game.dataframe()  # get pandas df for that game
        team_df, opp_df = (t1df, t2df) if t.id == game.team_one else (t2df, t1df)
        for feature in t_dict:
            t_dict[feature] += sum(team_df[feature])
            opp_dict[feature] += sum(opp_df[feature])

    #  Calculate percentages and averages
    p, fg, ft, pers = '-Point ', 'Field Goal ', 'Free Throw ', 'Percentage'
    fgs, fts, a = 'Field Goals', 'Free Throws', 'Attempts'
    t_dict[fg+pers] = t_dict[fgs]/t_dict[fg+a] if t_dict[fg+a] else 0
    t_dict[ft+pers] = t_dict[fts]/t_dict[ft+a] if t_dict[ft+a] else 0
    t_dict['Points Per Game'] = t_dict['Points']/len(games)
    opp_dict[fg+pers] = opp_dict[fgs]/opp_dict[fg+a] if opp_dict[fg+a] else 0
    opp_dict[ft+pers] = opp_dict[fts]/opp_dict[ft+a] if opp_dict[ft+a] else 0
    opp_dict['Points Per Game'] = opp_dict['Points']/len(games)
    for i in ['2', '3']:
        t_dict[i+p+fg+pers] = t_dict[i+p+fgs]/t_dict[i+p+fg+a] if t_dict[i+p+fg+a] else 0
        opp_dict[i+p+fg+pers] = opp_dict[i+p+fgs]/opp_dict[i+p+fg+a] if opp_dict[i+p+fg+a] else 0

    tdf = pd.DataFrame([t_dict, opp_dict])
    if num_games:
        return tdf, len(games)
    return tdf
