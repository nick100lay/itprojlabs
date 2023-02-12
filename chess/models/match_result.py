

from sqlalchemy import Column, Integer, SmallInteger, String, ForeignKeyConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from . import Base


class MatchResult(Base):
    __tablename__ = "match_results"
    __table_args__ = (
        CheckConstraint("winner >= 0 AND winner <= 2", name="winner_check"),
        ForeignKeyConstraint(["match_id"], ["matches.id"])
    ) 

    match_id = Column(Integer, ForeignKey("matches.id"), primary_key=True)
    
    match = relationship("Match", back_populates="result", uselist=False)

    winner = Column(SmallInteger)
    
    WINNER_TIE = 0
    WINNER_FIRST = 1
    WINNER_SECOND = 2