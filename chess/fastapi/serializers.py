

from ..crud import MatchResult as MatchResultEnum


def serialize_player(ply):
    return {
        "id": str(ply.id), 
        "firstName": ply.first_name, 
        "secondName": ply.second_name
    }

def serialize_players(players):
    return list(map(serialize_player, players))

def serialize_match_result(result):
    winners = {
        MatchResultEnum.WINNER_TIE: None, 
        MatchResultEnum.WINNER_FIRST: serialize_player(result.match.first_player), 
        MatchResultEnum.WINNER_SECOND: serialize_player(result.match.second_player) 
    }
    return { 
        "winner": winners[result.winner]
    }

def serialize_match(match):
    return {
        "id": str(match.id), 
        "firstPlayer": serialize_player(match.first_player), 
        "secondPlayer": serialize_player(match.second_player),
        "result": serialize_match_result(match.result) if match.result is not None else None,
    }

def serialize_matches(matches):
    return list(map(serialize_match, matches))


