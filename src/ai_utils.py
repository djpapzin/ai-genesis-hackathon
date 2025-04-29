"""
AI utilities for rap generation and scoring (OpenAI integration, rhyme analysis)
"""
import openai
import pronouncing
import random

# --- AI Rap Generation ---
def generate_rap(prompt: str, api_key: str) -> str:
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=64,
        temperature=0.9,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

# --- Scoring Logic ---
def score_rap(text: str) -> dict:
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    punchline_score = sum(1 for l in lines if "!" in l or "?" in l or l.endswith("."))
    rhyme_score = _rhyme_density(lines)
    word_score = len(set(text.split())) // 2
    total = punchline_score + rhyme_score + word_score
    return {
        "punchline": punchline_score,
        "rhyme": rhyme_score,
        "word": word_score,
        "total": total
    }

def _rhyme_density(lines):
    # Simple rhyme density: count pairs of lines that rhyme
    rhymes = 0
    for i in range(0, len(lines)-1, 2):
        w1 = lines[i].split()[-1] if lines[i].split() else ""
        w2 = lines[i+1].split()[-1] if lines[i+1].split() else ""
        if w1 and w2 and w2 in pronouncing.rhymes(w1):
            rhymes += 1
    return rhymes
