"""
Simple file-based persistent storage for CypherGPT games (MVP).
"""
import json
from typing import Any

STORE_PATH = "games_store.json"

def save_game(game: Any):
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(game, f, default=lambda o: o.__dict__, indent=2)

def load_game():
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
