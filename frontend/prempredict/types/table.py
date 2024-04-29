from typing import List, Optional

from testing.types.team import team

class standings:
    def __init__(self, type: str, group: Optional[None], stage: str, table: List[dict]):
        self.type = type
        self.group = group
        self.stage = stage
        self.table = [standingstablerow(**row_data) for row_data in table]

class standingstablerow:
    def __init__(self, won: int, draw: int, form: Optional[None], lost: int, team: team, points: int, goalsFor: int, position: int, playedGames: int, goalsAgainst: int, goalDifference: int):
        self.won = won
        self.draw = draw
        self.form = form
        self.lost = lost
        self.team = team
        self.points = points
        self.goalsFor = goalsFor
        self.position = position
        self.playedGames = playedGames
        self.goalsAgainst = goalsAgainst
        self.goalDifference = goalDifference