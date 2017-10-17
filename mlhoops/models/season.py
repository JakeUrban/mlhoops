from sqlalchemy import Column, Integer

from mlhoops.db import Base


class Season(Base):
    """
    Represents a NCAA basketball season
    """
    __tablename__ = 'seasons'
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False, unique=True)

    def __init__(self, year):
        self.year = year

    def __repr__(self):
        return str(self.__dict__)
