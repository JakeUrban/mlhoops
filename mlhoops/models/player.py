from sqlalchemy import Column, Integer, String, ForeignKey

from mlhoops.db.base import Base


class Player(Base):
    """
    Represents a NCAA basketball player
    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)

    def __init__(self, name, team_id):
        self.name = name
        self.team_id = team_id
