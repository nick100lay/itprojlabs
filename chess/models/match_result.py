

from sqlalchemy import Column, Integer, SmallInteger, String, ForeignKeyConstraint, CheckConstraint

from . import Base


class MatchResult(Base):
    __tablename__ = "match_results"
    __table_args__ = (
        CheckConstraint("winner >= 0 AND winner <= 2", name="winner_check"),
        ForeignKeyConstraint(["match_id"], ["matches.id"])
    ) 

    match_id = Column(Integer, primary_key=True)
    
    winner = Column(SmallInteger)
    
    WINNER_TIE = 0
    WINNER_FIRST = 1
    WINNER_SECOND = 2