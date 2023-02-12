

import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.event import listen

from . import *


class ModelsTestCase(unittest.TestCase):

    DEFAULT_DATABASE_URL = "sqlite:///:memory:"

    PLAYERS = sorted((
        (1, "Магнус", "Карлсен"),
        (2, "Гарри", "Каспаров"),
        (3, "Анатолий", "Карпов")
    ), key=lambda p: p[0])

    INVALID_PLAYERS = (
        (1, "A", "B"),
        (2, "C", "Dad"),
        (3, "Cac", "D"),
        (4, "", "")
    )

    MATCHES = sorted((
        (1, 1, 2),
        (2, 1, 3),
        (3, 2, 3)
    ), key=lambda m: m[0])

    INVALID_PLAYERS_MATCHES = (
        (1, 1, 5),
        (2, 5, 1),
        (2, 5, 6)
    )

    SAME_PLAYER_MATCHES = (
        (1, 1, 1),
    )

    MATCH_RESULTS = sorted((
        (1, MatchResult.WINNER_TIE),
        (2, MatchResult.WINNER_FIRST),
        (3, MatchResult.WINNER_SECOND)
    ), key=lambda mr: mr[0])

    INVALID_MATCH_RESULTS = (
        (100, MatchResult.WINNER_TIE),
    )

    SAME_MATCH_RESULTS = (
        (1, MatchResult.WINNER_TIE),
        (1, MatchResult.WINNER_FIRST),
    )

    INVALID_WINNER_MATCH_RESULTS = (
        (1, 10),
    )


    @staticmethod
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def get_database_url(self):
        return os.getenv("TEST_DB_URL", self.DEFAULT_DATABASE_URL)

    def setUp(self):
        db_url = self.get_database_url()
        self.engine = create_engine(db_url)
        self.session = Session(self.engine)
        if db_url.startswith("sqlite"):
            listen(self.engine, "connect", self.set_sqlite_pragma)
        Base.metadata.create_all(self.engine)
    
    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def insert_players(self, players):
        self.session.add_all(
            map(lambda p: Player(id=p[0], first_name=p[1], second_name=p[2]), 
                players)
        )

    def insert_matches(self, matches):
        self.session.add_all(
            map(lambda m: Match(id=m[0], first_player_id=m[1], second_player_id=m[2]), 
                matches)
        )

    def insert_match_results(self, match_results):
        self.session.add_all(
            map(lambda mr: MatchResult(match_id=mr[0], winner=mr[1]), match_results)
        )


    def commit_example_players(self):
        self.insert_players(self.PLAYERS)
        self.session.commit()

    def commit_example_matches(self):
        self.commit_example_players()
        self.insert_matches(self.MATCHES)
        self.session.commit()


    def test_insert_players(self):
        """ Зарегистрировать участников """
        self.commit_example_players()
        players = self.session.query(Player).order_by("id").all()
        self.assertEqual(
            list(map(lambda p: (p.id, p.first_name, p.second_name), 
                players)), 
            self.PLAYERS
        )
    
    def test_insert_invalid_players(self):
        """ Попытаться зарегистрировать участников с неправильными именами """
        self.insert_players(self.INVALID_PLAYERS)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_insert_matches(self):
        """ Зарегистрировать матчи """
        self.commit_example_matches()
        matches = self.session.query(Match).order_by("id").all()
        self.assertEqual(
            list(map(lambda m: (m.id, m.first_player_id, m.second_player_id), 
                matches)), 
            self.MATCHES
        )
    
    def test_insert_invalid_players_matches(self):
        """ Попытаться зарегистрировать матчи с неизвестными игроками """
        self.commit_example_players()
        self.insert_matches(self.INVALID_PLAYERS_MATCHES)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_insert_same_player_matches(self):
        """ Попытаться зарегистрировать матчи с одинаковым первым и вторым игроком """
        self.commit_example_players()
        self.insert_matches(self.SAME_PLAYER_MATCHES)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_insert_match_results(self):
        """ Огласить результаты матча """
        self.commit_example_matches()
        self.insert_match_results(self.MATCH_RESULTS)
        results = self.session.query(MatchResult).order_by("match_id").all()
        self.assertEqual(
            list(map(lambda mr: (mr.match_id, mr.winner), 
                results)), 
            self.MATCH_RESULTS
        )

    def test_insert_invalid_match_results(self):
        """ Попытаться огласить результаты неизвестного матча """
        self.commit_example_matches()
        self.insert_match_results(self.INVALID_MATCH_RESULTS)
        self.assertRaises(IntegrityError, self.session.commit)
    
    def test_insert_same_match_results(self):
        """ Попытаться огласить результаты одного и того же матча дважды """
        self.commit_example_matches()
        self.insert_match_results(self.SAME_MATCH_RESULTS)
        self.assertRaises(IntegrityError, self.session.commit)

    def test_insert_invalid_winner_match_results(self):
        """ Попытаться огласить результаты матча с неправильно указанным победителем """
        self.commit_example_matches()
        self.insert_match_results(self.INVALID_WINNER_MATCH_RESULTS)
        self.assertRaises(IntegrityError, self.session.commit)