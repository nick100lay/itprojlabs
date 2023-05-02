
import os
from typing import List

from fastapi import FastAPI

from ..crud import CRUD
from .models import Player, Match, PlayerForPost, MatchForPost, MatchResultForPost
from . import serializers


class NoDatabaseURLError(Exception):
    pass


def get_database_url():
    database_url = os.getenv("DB_URL")
    if database_url is None:
        raise NoDatabaseURLError("DB_URL environment variable is missing.")
    return database_url

app = FastAPI()

crud = CRUD(get_database_url())


@app.get("/players", response_model=List[Player])
@crud.wrapper
def read_players():
    return serializers.serialize_players(crud.read_players().all())


@app.get("/current-matches", response_model=List[Match])
@crud.wrapper
def read_current_matches():
    return serializers.serialize_matches(crud.read_current_matches().all())


@app.get("/completed-matches", response_model=List[Match])
@crud.wrapper
def read_completed_matches():
    return serializers.serialize_matches(crud.read_completed_matches().all())


@app.post("/players", response_model=List[Player])
@crud.wrapper
def create_players(players: List[PlayerForPost]):
    players = crud.create_players(map(lambda ply: (ply.first_name, ply.second_name), players))
    crud.commit()
    return serializers.serialize_players(players)


@app.post("/current-matches", response_model=List[Match])
@crud.wrapper
def create_current_matches(matches: List[MatchForPost]):
    matches = crud.create_matches(map(lambda match: (match.first_player_id, match.second_player_id), matches))
    crud.commit()
    return serializers.serialize_matches(matches)


@app.post("/completed-matches", response_model=List[Match])
@crud.wrapper
def create_completed_matches(match_results: List[MatchResultForPost]):
    match_results = crud.create_match_results(map(lambda result: (result.match_id, result.winner), match_results))
    crud.commit()
    return serializers.serialize_matches(
        map(lambda result: result.match, match_results)
    )

