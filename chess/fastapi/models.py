

from typing import Optional

from pydantic import BaseModel, Field, validator

from ..crud import MatchResult as MatchResultEnum


class Player(BaseModel):
    id: str
    first_name: str = Field(alias="firstName", min_length=2, max_length=20)
    second_name: str = Field(alias="secondName", min_length=2, max_length=20)


class PlayerForPost(BaseModel):
    first_name: str = Field(alias="firstName", min_length=2, max_length=20)
    second_name: str = Field(alias="secondName", min_length=2, max_length=20)


class MatchResult(BaseModel):
    winner: Optional[Player]


class MatchResultForPost(BaseModel):
    match_id: str
    winner: int 

    @validator("winner")
    def validate_winner(cls, winner):
        if winner not in (MatchResultEnum.WINNER_TIE, MatchResultEnum.WINNER_FIRST, MatchResultEnum.WINNER_SECOND):
            raise ValueError("wrong winner value given")
        return winner


class Match(BaseModel):
    id: str
    
    first_player: Player = Field(alias="firstPlayer")
    second_player: Player = Field(alias="secondPlayer")

    result: Optional[MatchResult]


class MatchForPost(BaseModel):
    first_player_id: str
    second_player_id: str
