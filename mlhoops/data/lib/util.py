from mlhoops.db.queries import (team_games_before, last_year,
                                all_games, get_teams, num_games)
import pandas as pd

from tqdm import tqdm


def reformat_team_data(tdf, num_games):
    p, fg, ft, pers = '-Point ', 'Field Goal ', 'Free Throw ', 'Percentage'
    fgs, fts, a, pg = 'Field Goals', 'Free Throws', 'Attempts', ' Per Game'

    tdf = tdf.drop(columns=[fg+a, fgs, fg+pers])
    tdf[fts+pg] = tdf[fts]/num_games
    tdf = tdf.drop(columns=[ft+a, fts, ft+pers])
    for i in ['2', '3']:
        tdf[i+p+fgs+pg] = tdf[i+p+fgs]/num_games
        tdf = tdf.drop(columns=[i+p+fg+a, i+p+fgs, i+p+fg+pers])

    tdf = tdf.drop(columns=['Total Rebounds', 'Points Per Game', 'Points'])

    for feature in tdf.columns:
        if pg not in feature and pers not in feature:
            tdf[feature+pg] = tdf[feature]/num_games
            tdf = tdf.drop(columns=[feature])

    return tdf


def season_upto(t, g):
    games = team_games_before(t, g).all()

    if not games:  # if this is the first game of the season
        last_season_t = last_year(t)
        data = last_season_t.get_data()
        tdf = pd.DataFrame(data[1:], columns=data[0])
        return tdf

    features = set(t.features).intersection(set(g.features))
    team_d, opp_d = {}, {}
    for feature in features:
        if 'Percentage' in feature:
            continue
        team_d[feature] = 0
        opp_d[feature] = 0

    for game in games:  # add up data from each game before g
        t1df, t2df = game.dataframe()  # get pandas df for that game
        team_df, opp_df = (t1df, t2df) if t.id == game.team_one else (t2df, t1df)
        for feature in team_d:
            team_d[feature] += sum(team_df[feature])
            opp_d[feature] += sum(opp_df[feature])

    #  Calculate percentages and averages
    p, fg, ft, pers = '-Point ', 'Field Goal ', 'Free Throw ', 'Percentage'
    fgs, fts, a = 'Field Goals', 'Free Throws', 'Attempts'
    team_d[fg+pers] = team_d[fgs]/team_d[fg+a] if team_d[fg+a] else 0
    team_d[ft+pers] = team_d[fts]/team_d[ft+a] if team_d[ft+a] else 0
    team_d['Points Per Game'] = team_d['Points']/len(games)
    opp_d[fg+pers] = opp_d[fgs]/opp_d[fg+a] if opp_d[fg+a] else 0
    opp_d[ft+pers] = opp_d[fts]/opp_d[ft+a] if opp_d[ft+a] else 0
    opp_d['Points Per Game'] = opp_d['Points']/len(games)
    for i in ['2', '3']:
        team_d[i+p+fg+pers] = team_d[i+p+fgs]/team_d[i+p+fg+a] if team_d[i+p+fg+a] else 0
        opp_d[i+p+fg+pers] = opp_d[i+p+fgs]/opp_d[i+p+fg+a] if opp_d[i+p+fg+a] else 0

    return pd.DataFrame([team_d, opp_d])


def games_dataset(year, head=None):
    games = all_games(year)
    df = pd.DataFrame()
    for game in tqdm(games[:head]):
        t1, t2 = get_teams(game)
        t1_games_before = team_games_before(t1, game).count()
        if not t1_games_before:
            lyt1 = last_year(t1)
            t1_games_before = num_games(lyt1, season_id=lyt1.season_id)
        t2_games_before = team_games_before(t2, game).count()
        if not t2_games_before:
            lyt2 = last_year(t2)
            t2_games_before = num_games(lyt2, season_id=lyt2.season_id)
        t1df = reformat_team_data(season_upto(t1, game), t1_games_before).drop(1)
        t2df = reformat_team_data(season_upto(t2, game), t2_games_before).drop(1)
        game_df = t1df - t2df
        game_df.index = [game.id]
        game_dict = game.to_dict()
        for feature in ['team_one', 'team_two', 'team_one_score',
                        'team_two_score', 'date_played']:
            game_df[feature] = game_dict[feature]
        game_df['tournament'] = 1 if game_dict['tournament_id'] else 0
        game_df['t1_games_before'] = t1_games_before
        game_df['t2_games_before'] = t2_games_before
        df = df.append(game_df)
    return df
