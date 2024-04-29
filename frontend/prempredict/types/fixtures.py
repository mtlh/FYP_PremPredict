from typing import List, Optional, Union

from testing.types.team import competition, referee, team

class score:
    def __init__(self, winner: str, duration: str, fullTime: dict, halfTime: dict):
        self.winner = winner
        self.duration = duration
        self.fullTime = fullTime
        self.halfTime = halfTime

class area:
    def __init__(self, id: int, code: str, flag: str, name: str):
        self.id = id
        self.code = code
        self.flag = flag
        self.name = name

class odds:
    def __init__(self, msg: str):
        self.msg = msg

class season:
    def __init__(self, id: int, winner: Optional[None], endDate: str, startDate: str, currentMatchday: int):
        self.id = id
        self.winner = winner
        self.endDate = endDate
        self.startDate = startDate
        self.currentMatchday = currentMatchday

class match:
    def __init__(self, id: int, area: area, odds: odds, group: Optional[None], score: score, stage: str, season: season, status: str, utcDate: str, awayTeam: team, homeTeam: team, matchday: int, referees: referee, competition: competition, lastUpdated: str):
        self.id = id
        self.area = area
        self.odds = odds
        self.group = group
        self.score = score
        self.stage = stage
        self.season = season
        self.status = status
        self.utcDate = utcDate
        self.awayTeam = awayTeam
        self.homeTeam = homeTeam
        self.matchday = matchday
        self.referees = referees
        self.competition = competition
        self.lastUpdated = lastUpdated

class fixtures:
    def __init__(self, filters: dict, matches: Union[List[dict], List[match]]):
        self.filters = filters
        self.matches = matches
