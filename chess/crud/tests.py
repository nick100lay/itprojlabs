

import os
import unittest

from . import CRUD, CRUDError, MatchResult


class CRUDTestCase(unittest.TestCase):

    DEFAULT_DATABASE_URL = "sqlite:///:memory:"

    PLAYERS = sorted((
        (1, "Магнус", "Карлсен"),
        (2, "Гарри", "Каспаров"),
        (3, "Анатолий", "Карпов")
    ), key=lambda p: p[0])

    INVALID_PLAYERS = (
        ("A", "B"),
        ("C", "Dad"),
        ("Cac", "D"),
        ("", "")
    )

    MATCHES = sorted((
        (1, 1, 2),
        (2, 1, 3),
        (3, 2, 3)
    ), key=lambda m: m[0])

    INVALID_PLAYERS_MATCHES = (
        (1, 5),
        (5, 1),
        (5, 6)
    )

    SAME_PLAYER_MATCHES = (
        (1, 1),
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

    def get_database_url(self):
        return os.getenv("TEST_DB_URL", self.DEFAULT_DATABASE_URL)

    def setUp(self):
        self.crud = CRUD(self.get_database_url())
        self.crud.start()
    
    def tearDown(self):
        self.crud.finish(drop_all=True)


    def commit_example_players(self):
        self.crud.create_players(self.PLAYERS)
        self.crud.commit()

    def commit_example_matches(self):
        self.commit_example_players()
        self.crud.create_matches(self.MATCHES)
        self.crud.commit()

    def assert_crud_commit_error(self):
        self.assertRaises(CRUDError, self.crud.commit)


    def test_create_players(self):
        """ Зарегистрировать участников """
        self.commit_example_players()
        players = self.crud.read_players().order_by("id").all()
        self.assertEqual(
            list(map(lambda p: (p.id, p.first_name, p.second_name), 
                players)), 
            self.PLAYERS
        )
    
    def test_create_invalid_players(self):
        """ Попытаться зарегистрировать участников с неправильными именами """
        self.crud.create_players(self.INVALID_PLAYERS)
        self.assert_crud_commit_error()

    def test_create_matches(self):
        """ Зарегистрировать матчи """
        self.commit_example_matches()
        matches = self.crud.read_matches().order_by("id").all()
        self.assertEqual(
            list(map(lambda m: (m.id, m.first_player_id, m.second_player_id), 
                matches)), 
            self.MATCHES
        )
    
    def test_create_invalid_players_matches(self):
        """ Попытаться зарегистрировать матчи с неизвестными игроками """
        self.commit_example_players()
        self.crud.create_matches(self.INVALID_PLAYERS_MATCHES)
        self.assert_crud_commit_error()

    def test_create_same_player_matches(self):
        """ Попытаться зарегистрировать матчи с одинаковым первым и вторым игроком """
        self.commit_example_players()
        self.crud.create_matches(self.SAME_PLAYER_MATCHES)
        self.assert_crud_commit_error()

    def test_create_match_results(self):
        """ Огласить результаты матча """
        self.commit_example_matches()
        self.crud.create_match_results(self.MATCH_RESULTS)
        self.crud.commit()
        results = self.crud.read_match_results().order_by("match_id").all()
        self.assertEqual(
            list(map(lambda mr: (mr.match_id, mr.winner), 
                results)), 
            self.MATCH_RESULTS
        )

    def test_create_invalid_match_results(self):
        """ Попытаться огласить результаты неизвестного матча """
        self.commit_example_matches()
        self.crud.create_match_results(self.INVALID_MATCH_RESULTS)
        self.assert_crud_commit_error()
    
    def test_create_same_match_results(self):
        """ Попытаться огласить результаты одного и того же матча дважды """
        self.commit_example_matches()
        self.crud.create_match_results(self.SAME_MATCH_RESULTS)
        self.assert_crud_commit_error()

    def test_create_invalid_winner_match_results(self):
        """ Попытаться огласить результаты матча с неправильно указанным победителем """
        self.commit_example_matches()
        self.crud.create_match_results(self.INVALID_WINNER_MATCH_RESULTS)
        self.assert_crud_commit_error()