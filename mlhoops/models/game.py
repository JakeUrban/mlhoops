from sqlalchemy import Column, Integer, ForeignKey, DateTime, String

from mlhoops.db import Base
from mlhoops.models.util.game import game_stats_path


class Game(Base):
    """
    Represents a NCAA basketball game
    """
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    team_one = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team_two = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team_one_score = Column(Integer, nullable=False, default=0)
    team_two_score = Column(Integer, nullable=False, default=0)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    date_played = Column(DateTime, nullable=False)
    stats_path = Column(String(255), nullable=False)

    def __init__(self, team_one, team_two, season, date_played,
                 team_one_score=0, team_two_score=0, tournament_id=None):
        self.team_one = team_one
        self.team_two = team_two
        self.season_id = season
        self.date_played = date_played
        self.team_one_score = team_one_score
        self.team_two_score = team_two_score
        self.tournament_id = tournament_id
        self.stats_path = game_stats_path(self)
