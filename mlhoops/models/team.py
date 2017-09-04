from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from mlhoops.db import Base
from mlhoops.util.team_util import team_stats_path


class Team(Base):
    """
    Represents a NCAA basketball team for a particular season
    """
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    stats_path = Column(String(255), nullable=False)
    made_tournament = Column(Boolean, nullable=False)
    bracket = Column(String(255))
    seed = Column(Integer)

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
