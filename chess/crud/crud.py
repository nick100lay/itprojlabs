

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.event import listen

from ..models import *


class CRUDError(Exception):
    pass

class CRUD:

    def __init__(self, url):
        self.url = url

    @staticmethod
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def start(self):
        self.engine = create_engine(self.url)
        self.session = Session(self.engine)
        if self.url.startswith("sqlite"):
            listen(self.engine, "connect", self.set_sqlite_pragma)
        Base.metadata.create_all(self.engine)

    def finish(self, drop_all=False):
        self.session.close()
        if drop_all:
            Base.metadata.drop_all(self.engine)
    
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
        self.add_all(map(self.make_player, players))

    def create_matches(self, matches):
        self.add_all(map(self.make_match, matches))
    
    def create_match_results(self, match_results):
        self.add_all(map(self.make_match_result, match_results))
    
    def read_players(self):
        return self.query(Player)
    
    def read_matches(self):
        return self.query(Match)

    def read_match_results(self):
        return self.query(MatchResult)
