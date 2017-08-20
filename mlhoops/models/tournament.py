from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from mlhoops.db import Base


class Tournament(Base):
    """
    Represents a NCAA march madness tournament
    """
    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    champion_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    teams = relationship('Team')

    def __init__(self, season_id, champion_id):
        self.season_id = season_id
        self.champion_id = champion_id
