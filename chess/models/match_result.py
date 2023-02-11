

from sqlalchemy import Column, SmallInteger, String, ForeignKey, CheckConstraint

from . import Base


class MatchResult(Base):
    __tablename__ = "match_results"

    match_id = Column(Integer, ForeignKey("matches.id"), primary_key=True)
    
    winner = Column(SmallInteger)
    
    WINNER_TIE = 0
    WINNER_FIRST = 1
    WINNER_SECOND = 2

    CheckConstraint("winner >= 0 AND winner <= 2", name="winner_check") 