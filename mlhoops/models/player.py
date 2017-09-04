from sqlalchemy import Column, Integer, String, ForeignKey

from mlhoops.db import Base
from mlhoops.util.player_util import player_stats_path


class Player(Base):
    """
    Represents a NCAA basketball player for a particular team and season
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    stats_path = Column(String(255), nullable=False)

    def __init__(self, name, team_id):
        self.name = name
        self.team_id = team_id
        self.stats_path = player_stats_path(self)
