"""
Data models for CypherGPT backend (Player, Round, Score, GameMode).
"""
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass, field

class GameMode(str, Enum):
    PVP = "player_vs_player"
    PVAI = "player_vs_ai"
    FREESTYLE = "freestyle"
    COACH = "ai_coach"

@dataclass
class Score:
    punchline: int = 0
    rhyme: int = 0
    word: int = 0
    total: int = 0
    def compute_total(self):
        self.total = self.punchline + self.rhyme + self.word

@dataclass
class Round:
    number: int
    player_input: str
    ai_input: Optional[str] = None
    score: Score = field(default_factory=Score)
    feedback: Optional[str] = None

@dataclass
class Player:
    name: str
    rounds: List[Round] = field(default_factory=list)

@dataclass
class Game:
    mode: GameMode
    players: List[Player]
    current_round: int = 1
    max_rounds: int = 3
    scoreboard: List[dict] = field(default_factory=list)
