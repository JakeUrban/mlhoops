import pandas as pd


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
