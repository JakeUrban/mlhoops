from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from mlhoops.db.base import Base


class Team(Base):
    """
    Represents a NCAA basketball team
    """
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    players = relationship('Player', back_populates='teams')

    def __init__(self, name):
        self.name = name
