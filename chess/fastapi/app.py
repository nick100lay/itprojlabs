
import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..crud import CRUDProvider
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

crud_provider = CRUDProvider(get_database_url())
crud_provider.init()


@app.get("/players", response_model=List[Player])
def read_players():
    with crud_provider.crud() as crud:
        return serializers.serialize_players(crud.read_players().all())


@app.get("/current-matches", response_model=List[Match])
def read_current_matches():
    with crud_provider.crud() as crud:
        return serializers.serialize_matches(crud.read_current_matches().all())


@app.get("/completed-matches", response_model=List[Match])
def read_completed_matches():
    with crud_provider.crud() as crud:
        return serializers.serialize_matches(crud.read_completed_matches().all())


@app.post("/players", response_model=List[Player])
def create_players(players: List[PlayerForPost]):
    with crud_provider.crud() as crud:
        players = crud.create_players(map(lambda ply: (ply.first_name, ply.second_name), players))
        crud.commit()
        return serializers.serialize_players(players)


@app.post("/current-matches", response_model=List[Match])
def create_current_matches(matches: List[MatchForPost]):
    with crud_provider.crud() as crud:
        matches = crud.create_matches(map(lambda match: (match.first_player_id, match.second_player_id), matches))
        crud.commit()
        return serializers.serialize_matches(matches)


@app.post("/completed-matches", response_model=List[Match])
def create_completed_matches(match_results: List[MatchResultForPost]):
    with crud_provider.crud() as crud:
        match_results = crud.create_match_results(map(lambda result: (result.match_id, result.winner), match_results))
        crud.commit()
        return serializers.serialize_matches(
            map(lambda result: result.match, match_results)
        )

