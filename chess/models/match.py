

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint

from . import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    
    first_player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    second_player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    CheckConstraint("first_player_id <> second_player_id", name="players_check")
