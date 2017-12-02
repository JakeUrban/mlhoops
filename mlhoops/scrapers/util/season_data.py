import csv
from sqlalchemy import and_
from mlhoops.scrapers import ScheduleScraper, GameScraper, TeamScraper
from mlhoops.models import Season, Game, Team, Player
from mlhoops.db import session


"""
Need to get team names from game page, no other way
"""


def get_and_insert_data(year, offset=0):
    ss = ScheduleScraper()
    gs = GameScraper()
    ts = TeamScraper()

    season = session().query(Season).filter(Season.year == year).first()
    urls = ss.get_team_urls(year)[offset:]
    exisiting_teams = set([t.name for t in session().query(Team).join(Season).filter(Season.year == year).all()])  # noqa
    already_seen = set()

    for url in urls:
        schedule = ss.get_schedule(url, only_season=True)
        for endpoint in schedule:
            if endpoint in already_seen:
                continue
            g = gs.get_game_info(endpoint, team_urls=True)
            print('{} v. {}'.format(g[0], g[1]))
            new_teams = []
            if g[0] not in exisiting_teams:
                new_teams.append((g[0], g[2]))
            if g[1] not in exisiting_teams:
                new_teams.append((g[1], g[3]))
            for new_team in new_teams:
                print("Creating Team: {}".format(new_team[0]))
                wins, losses, team_opp = ts.get_team_info(new_team[1])
                t = Team(new_team[0], season.id, wins=wins, losses=losses)
                session().add(t)
                session().flush()
                exisiting_teams.add(new_team[0])
                with open(t.stats_path, 'w') as f:
                    csv.writer(f).writerows(team_opp)

                player_info = ts.get_player_info(new_team[1])
                for player in player_info[1].items():
                    print("Player: {}".format(player[0]))
                    p = Player(player[0], t.id)
                    session().add(p)
                    session().flush()
                    with open(p.stats_path, 'w') as f:
                        csv.writer(f).writerow(player[1])

            cond = and_(Team.name == g[0], Season.year == year)
            t_one = session().query(Team).join(Season).filter(cond).first()
            t_two = session().query(Team).join(Season).filter(cond).first()

            cond = and_(Game.date_played == g[6], Game.team_one.in_([t_one.id, t_two.id]))
            if session().query(Game).filter(cond).first():
                print("Game Found")
                continue
            g[4], g[5] = (g[4], g[5]) if t_one.name == g[0] else (g[5], g[4])
            print("Creating Game")
            game = Game(t_one.id, t_two.id, season.id, g[6],
                        team_one_score=g[4], team_two_score=g[5])
            session().add(game)
            session().flush()

            g_stats = gs.get_game_stats(endpoint)
            with open(game.stats_path, 'w') as f:
                csv.writer(f).writerows(g_stats[0])
                csv.writer(f).writerows(g_stats[1])

            already_seen.add(endpoint)

        session().commit()
        offset += 1
        with open('offset.txt', 'w') as f:
            f.write(str(offset))
