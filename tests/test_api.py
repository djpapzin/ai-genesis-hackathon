"""
Pytest-based API tests for CypherGPT backend.
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from api import app

client = TestClient(app)

def test_start_game_pvai():
    response = client.post("/start-game", json={"mode": "player_vs_ai", "player_names": ["Alice"]})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Game started"
    assert data["mode"] == "player_vs_ai"
    assert "Alice" in data["players"]

def test_submit_rap_pvai():
    client.post("/start-game", json={"mode": "player_vs_ai", "player_names": ["Alice"]})
    response = client.post("/submit-rap", json={"name": "Alice", "input_text": "This is a test rap.", "round_number": 1, "mode": "player_vs_ai"})
    assert response.status_code == 200
    data = response.json()
    assert "ai_text" in data
    assert "score" in data

def test_scoreboard():
    client.post("/start-game", json={"mode": "player_vs_ai", "player_names": ["Alice"]})
    client.post("/submit-rap", json={"name": "Alice", "input_text": "This is a test rap.", "round_number": 1, "mode": "player_vs_ai"})
    response = client.get("/scoreboard")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("player" in row for row in data)

def test_start_game_pvp():
    response = client.post("/start-game", json={"mode": "player_vs_player", "player_names": ["Alice", "Bob"]})
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "player_vs_player"
    assert set(data["players"]) == {"Alice", "Bob"}

def test_submit_rap_pvp():
    client.post("/start-game", json={"mode": "player_vs_player", "player_names": ["Alice", "Bob"]})
    response = client.post("/submit-rap", json={"name": "Alice", "input_text": "Battle rap line!", "round_number": 1, "mode": "player_vs_player"})
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
