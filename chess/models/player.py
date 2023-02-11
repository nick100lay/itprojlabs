

from sqlalchemy import Column, Integer, String, CheckConstraint

from . import Base


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    second_name = Column(String(20), nullable=False)

    CheckConstraint("LENGTH(first_name) >= 2 AND LENGTH(second_name) >= 2", name="min_name_len_check")
