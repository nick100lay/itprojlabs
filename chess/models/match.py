

from sqlalchemy import Column, Integer, String, ForeignKeyConstraint, CheckConstraint

from . import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint("first_player_id <> second_player_id", name="players_check"),
        ForeignKeyConstraint(["first_player_id"], ["players.id"]),
        ForeignKeyConstraint(["second_player_id"], ["players.id"])
    )

    id = Column(Integer, primary_key=True)
    
    first_player_id = Column(Integer, nullable=False)
    second_player_id = Column(Integer, nullable=False)
