from sqlalchemy import Column, Integer, String, ForeignKey

from mlhoops.db.base import Base


class Player(Base):
    """
    Represents a NCAA basketball player for a particular team and season
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    stats_file = Column(String(255), nullable=False)

    def __init__(self, name, team_id, stats_file):
        self.name = name
        self.team_id = team_id
        self.stats_file = stats_file
