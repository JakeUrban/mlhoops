from sqlalchemy import Column, Integer, String, ForeignKey

from mlhoops.db.session import Base
from mlhoops.player.util import get_player_stats_file


class Player(Base):
    """
    Represents a NCAA basketball player for a particular team and season
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    stats_file = Column(String(255), nullable=False)

    def __init__(self, name, team_id):
        self.name = name
        self.team_id = team_id
        self.stats_file = get_player_stats_file(self)
