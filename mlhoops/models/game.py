from sqlalchemy import Column, Integer, ForeignKey, DateTime, String

from mlhoops.db import Base
from mlhoops.models.util import game_stats_path

import pandas as pd


class Game(Base):
    """
    Represents a NCAA basketball game
    """
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    team_one = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team_two = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team_one_score = Column(Integer, nullable=False, default=0)
    team_two_score = Column(Integer, nullable=False, default=0)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    date_played = Column(DateTime, nullable=False)
    stats_path = Column(String(255), nullable=False)
    features = ['Player', 'Minutes Played', 'Field Goals', 'Field Goal Attempts',
                'Field Goal Percentage', '2-Point Field Goals',
                '2-Point Field Goal Attempts',
                '2-Point Field Goal Percentage', '3-Point Field Goals',
                '3-Point Field Goal Attempts',
                '3-Point Field Goal Percentage', 'Free Throws',
                'Free Throw Attempts', 'Free Throw Percentage',
                'Offensive Rebounds', 'Defensive Rebounds', 'Total Rebounds',
                'Assists', 'Steals', 'Blocks', 'Turnovers', 'Personal Fouls',
                'Points']

    def __init__(self, team_one, team_two, season, date_played,
                 team_one_score=0, team_two_score=0, tournament_id=None):
        self.team_one = team_one
        self.team_two = team_two
        self.season_id = season
        self.date_played = date_played
        self.team_one_score = team_one_score
        self.team_two_score = team_two_score
        self.tournament_id = tournament_id
        self.stats_path = game_stats_path(self)

    def dataframe(self):
        d = self.get_data()
        t1_df = pd.DataFrame(d[1], columns=d[0])
        t2_df = pd.DataFrame(d[2], columns=d[0])
        return t1_df, t2_df

    def to_dict(self):
        d = self.__dict__.copy()
        d.pop('_sa_instance_state')
        return d

    def __repr__(self):
        return str(self.to_dict())

    def get_data(self):
        with open(self.stats_path, 'r') as f:
            h_line = f.readline()
            team_one, team_two = [], []
            cur_team = team_one
            for line in f:
                if line == h_line:
                    cur_team = team_two
                    continue
                line = line.split(',')
                cur_team.append([line[0]])
                for x in line[1:]:
                    cur_team[-1].append(float(x)) if x else cur_team[-1].append(None)
            return [self.features, team_one, team_two]
