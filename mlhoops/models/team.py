from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from mlhoops.db import Base
from mlhoops.models.util import team_stats_path


class Team(Base):
    """
    Represents a NCAA basketball team for a particular season
    """
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    stats_path = Column(String(255), nullable=False)
    made_tournament = Column(Boolean, nullable=False)
    bracket = Column(String(255))
    seed = Column(Integer)
    features = ['Field Goals', 'Field Goal Attempts',
                'Field Goal Percentage', '2-Point Field Goals',
                '2-Point Field Goal Attempts',
                '2-Point Field Goal Percentage', '3-Point Field Goals',
                '3-Point Field Goal Attempts',
                '3-Point Field Goal Percentage', 'Free Throws',
                'Free Throw Attempts', 'Free Throw Percentage',
                'Offensive Rebounds', 'Defensive Rebounds',
                'Total Rebounds', 'Assists', 'Steals', 'Blocks',
                'Turnovers', 'Personal Fouls', 'Points', 'Points Per Game']

    def __init__(self, name, season_id, made_tournament=False, bracket=None,
                 seed=None, wins=0, losses=0):
        self.name = name
        self.season_id = season_id
        self.stats_path = team_stats_path(self)
        self.made_tournament = made_tournament
        self.bracket = bracket
        self.seed = seed
        self.wins = wins
        self.losses = losses
        if made_tournament and not (bracket or seed):
            exp_str = "Must specify bracket and seed with made_tournament"
            raise Exception(exp_str)

    def __repr__(self):
        return str(self.__dict__)

    def get_data(self):
        data = [self.features, [], []]
        with open(self.stats_path, 'r') as f:
            f.readline()
            for x in f.readline().split(','):
                data[1].append(float(x) if x else None)
            for x in f.readline().split(','):
                data[2].append(float(x) if x else None)
            return data

