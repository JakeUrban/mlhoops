from sqlalchemy import Column, Integer, String, ForeignKey

from mlhoops.db import Base
from mlhoops.models.util import player_stats_path


class Player(Base):
    """
    Represents a NCAA basketball player for a particular team and season
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    stats_path = Column(String(255), nullable=False)
    features = ['Games', 'Games Started', 'Minutes Played Per Game',
                'Field Goals Per Game', 'Field Goal Attempts Per Game',
                'Field Goal Percentage', '2-Point Field Goals Per Game',
                '2-Point Field Goal Attempts Per Game',
                '2-Point Field Goal Percentage',
                '3-Point Field Goals Per Game',
                '3-Point Field Goal Attempts Per Game',
                '3-Point Field Goal Percentage', 'Free Throws Per Game',
                'Free Throw Attempts Per Game', 'Free Throw Percentage',
                'Offensive Rebounds Per Game', 'Defensive Rebounds Per Game',
                'Total Rebounds Per Game', 'Assists Per Game',
                'Steals Per Game', 'Blocks Per Game', 'Turnovers Per Game',
                'Personal Fouls Per Game', 'Points Per Game']

    def __init__(self, name, team_id):
        self.name = name
        self.team_id = team_id
        self.stats_path = player_stats_path(self)

    def __repr__(self):
        return str(self.__dict__)

    def get_data(self):
        line = open(self.stats_path, 'r').readline().strip('\n').split(',')
        for i, x in enumerate(line):
            line[i] = float(line[i]) if x else None
        return [self.features, line]
