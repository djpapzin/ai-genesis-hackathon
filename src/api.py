"""
FastAPI endpoints for CypherGPT backend (MVP: Player vs AI, Scoreboard, Submission)
"""
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional
from models import Game, GameMode, Player, Round, Score
from ai_utils import generate_rap, score_rap
from storage import save_game, load_game
import os

app = FastAPI(title="CypherGPT Backend API")

# --- Pydantic Schemas for API ---
class PlayerInput(BaseModel):
    name: str
    input_text: str
    round_number: int
    mode: GameMode
    tone: str = "aggressive"  # Default tone
    persona: str = None  # e.g., "Eminem", "Tupac", "Shakespeare"
class AIResponse(BaseModel):
    ai_text: str
    score: Score
    feedback: Optional[str] = None

# --- Persistent Game Store ---
games = load_game() or {}

@app.post("/start-game")
def start_game(mode: GameMode, player_names: List[str]):
    players = [Player(name=n) for n in player_names]
    game = Game(mode=mode, players=players)
    games["current"] = game
    save_game(games)
    return {"message": "Game started", "mode": mode, "players": player_names}

@app.post("/submit-rap")
def submit_rap(input: PlayerInput):
    game = games.get("current")
    if not game:
        return {"error": "No game in progress"}
    player = next((p for p in game.players if p.name == input.name), None)
    if not player:
        return {"error": "Player not found"}
    round_obj = Round(number=input.round_number, player_input=input.input_text)
    player.rounds.append(round_obj)
    save_game(games)
    # --- Player vs AI ---
    if game.mode == GameMode.PVAI:
        api_key = os.getenv("OPENAI_API_KEY", "")
        persona_str = f" Respond as if you are {input.persona}." if input.persona else ""
        prompt = (
            f"Write a rap battle response to: {input.input_text}\n"
            f"Use an AABB rhyme scheme. Each line must end with a rhyme. "
            f"Match the tone: {input.tone}.{persona_str} Keep it clever and punchy."
        )
        ai_text = generate_rap(prompt, api_key) if api_key else "[AI key not set]"
        score_dict = score_rap(ai_text)
        score = Score(**{k: score_dict[k] for k in ['punchline','rhyme','word','total']})
        round_obj.ai_input = ai_text
        round_obj.score = score
        round_obj.feedback = f"[Auto feedback: scoring complete, Tone: {input.tone}]"
        return AIResponse(ai_text=ai_text, score=score, feedback=round_obj.feedback)
    # --- Player vs Player ---
    if game.mode == GameMode.PVP:
        score_dict = score_rap(input.input_text)
        score = Score(**{k: score_dict[k] for k in ['punchline','rhyme','word','total']})
        round_obj.score = score
        round_obj.feedback = "[Manual review or future AI feedback]"
        return {"message": "PvP rap submitted and scored", "score": score_dict}
    # --- Freestyle ---
    if game.mode == GameMode.FREESTYLE:
        score_dict = score_rap(input.input_text)
        score = Score(**{k: score_dict[k] for k in ['punchline','rhyme','word','total']})
        round_obj.score = score
        round_obj.feedback = "[Freestyle feedback]"
        return {"message": "Freestyle submitted and scored", "score": score_dict}
    # --- AI Coach ---
    if game.mode == GameMode.COACH:
        api_key = os.getenv("OPENAI_API_KEY", "")
        persona_str = f" Respond as if you are {input.persona}." if input.persona else ""
        prompt = (
            f"Analyze this rap: {input.input_text}\n"
            f"Give feedback on strengths and weaknesses. Match the tone: {input.tone}.{persona_str}"
        )
        feedback = generate_rap(prompt, api_key) if api_key else "[AI key not set]"
        score_dict = score_rap(input.input_text)
        score = Score(**{k: score_dict[k] for k in ['punchline','rhyme','word','total']})
        round_obj.score = score
        round_obj.feedback = feedback
        return {"message": "AI Coach feedback", "score": score_dict, "feedback": round_obj.feedback}
    return {"message": "Rap submitted", "player": input.name}

@app.get("/scoreboard")
def get_scoreboard():
    game = games.get("current")
    if not game:
        return {"error": "No game in progress"}
    board = []
    for player in game.players:
        for rnd in player.rounds:
            board.append({
                "player": player.name,
                "round": rnd.number,
                "input": rnd.player_input,
                "ai_input": rnd.ai_input,
                "score": vars(rnd.score),
                "feedback": rnd.feedback
            })
    return board
