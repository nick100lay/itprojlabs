

from sqlalchemy import Column, Integer, String, ForeignKeyConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from . import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint("first_player_id <> second_player_id", name="players_check"),
        ForeignKeyConstraint(["first_player_id"], ["players.id"]),
        ForeignKeyConstraint(["second_player_id"], ["players.id"])
    )

    id = Column(Integer, primary_key=True)
    
    first_player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    second_player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    first_player = relationship("Player", uselist=False, foreign_keys=[first_player_id])
    second_player = relationship("Player", uselist=False, foreign_keys=[second_player_id])

    result = relationship("MatchResult", back_populates="match", uselist=False)
