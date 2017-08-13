from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from mlhoops.db.base import Base


class Season(Base):
    """
    Represents a NCAA basketball season
    """
    __tablename__ = 'seasons'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False, unique=True)
    tournament = relationship("Tournament", uselist=False,
                              back_populates='season')

    def __init__(self, year):
        self.year = year
