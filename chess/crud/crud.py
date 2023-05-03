

from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.event import listen

from ..models import *


class CRUDError(Exception):
    pass


class CRUD:
    
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        self.session.begin()
        return self

    def close(self):
        self.session.close()

    def __exit__(self, ex_type, ex_val, ex_tb):
        self.close()

    @staticmethod
    def make_player(player_t):
        id = None
        if len(player_t) == 2:
            first_name, second_name = player_t 
        else:
            id, first_name, second_name = player_t
        return Player(id=id, first_name=first_name, second_name=second_name)

    @staticmethod
    def make_match(match_t):
        id = None
        if len(match_t) == 2:
            first_player_id, second_player_id = match_t 
        else:
            id, first_player_id, second_player_id = match_t
        return Match(id=id, first_player_id=first_player_id, second_player_id=second_player_id)
    
    def query(self, ent):
        return self.session.query(ent)

    def add_all(self, ent_objs):
        return self.session.add_all(ent_objs)

    @staticmethod
    def make_match_result(match_result_t):
        return MatchResult(match_id=match_result_t[0], winner=match_result_t[1])

    
    def commit(self):
        try:
            self.session.commit()
        except IntegrityError as ex:
            raise CRUDError() from ex


    def create_players(self, players):
        players = list(map(self.make_player, players))
        self.add_all(players)
        return players

    def create_matches(self, matches):
        matches = list(map(self.make_match, matches))
        self.add_all(matches)
        return matches
    
    def create_match_results(self, match_results):
        match_results = list(map(self.make_match_result, match_results))
        self.add_all(match_results)
        return match_results
    
    def read_players(self):
        return self.query(Player)
    
    def read_matches(self):
        return self.query(Match)
    
    def read_current_matches(self):
        return self.query(Match).filter(Match.result == None)
    
    def read_completed_matches(self):
        return self.query(Match).filter(Match.result != None)

    def read_match_results(self):
        return self.query(MatchResult)


class CRUDProvider:

    def __init__(self, url):
        self.url = url

    @staticmethod
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def init(self):
        self.engine = create_engine(self.url)
        if self.url.startswith("sqlite"):
            listen(self.engine, "connect", self.set_sqlite_pragma)
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)

    def dispose(self):    
        self.engine.dispose()
        
    def crud(self):
        return CRUD(Session(self.engine))

