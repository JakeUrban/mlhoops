from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, String

from mlhoops.db.base import Base
from mlhoops.game.util import get_game_stats_file


class Game(Base):
    """
    Represents a NCAA basketball game
    """
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    home_team = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team = Column(Integer, ForeignKey('teams.id'), nullable=False)
    home_team_score = Column(Integer, nullable=False, default=0)
    away_team_score = Column(Integer, nullable=False, default=0)
    season_id = Column(Integer, ForeignKey('seasons.id'), nullable=False)
    tournament_game = Column(Boolean, nullable=False, default=False)
    date_played = Column(DateTime, nullable=False)
    stats_file = Column(String(255), nullable=False)

    def __init__(self, home_team, away_team, season_id, date_played,
                 home_team_score=0, away_team_score=0, tournament_game=False):
        self.home_team = home_team
        self.away_team = away_team
        self.season_id = season_id
        self.date_played = date_played
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.tournament_game = tournament_game
        self.stats_file = get_game_stats_file(self)
