from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from mlhoops.db.base import Base
from mlhoops.team.util import get_team_stats_file


class Team(Base):
    """
    Represents a NCAA basketball team for a particular season
    """
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    stats_file = Column(String(255), nullable=False)
    players = relationship('Player', back_populates='teams')
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))

    def __init__(self, name, season_id, tournament_id=None):
        self.name = name
        self.season_id = season_id
        self.tournament_id = tournament_id
        self.stats_file = get_team_stats_file(self)
