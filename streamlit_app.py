import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("CypherGPT Demo Frontend")

mode = st.selectbox("Game Mode", ["player_vs_ai", "player_vs_player", "freestyle", "ai_coach"])
name = st.text_input("Your Name", value="Alice")
input_text = st.text_area("Enter your rap verse here")
round_number = st.number_input("Round Number", min_value=1, max_value=10, value=1)
tone = st.selectbox("Tone", ["aggressive", "witty", "sarcastic", "calm", "spiritual"])
persona = st.text_input("Persona (e.g., Eminem, Tupac, Shakespeare)")

if st.button("Start Game"):
    player_names = [name] if mode != "player_vs_player" else [name, "Bob"]
    resp = requests.post(f"{API_URL}/start-game", json={"mode": mode, "player_names": player_names})
    st.write(resp.json())

if st.button("Submit Rap"):
    payload = {
        "name": name,
        "input_text": input_text,
        "round_number": round_number,
        "mode": mode,
        "tone": tone,
        "persona": persona or None,
    }
    resp = requests.post(f"{API_URL}/submit-rap", json=payload)
    st.write(resp.json())

if st.button("Show Scoreboard"):
    resp = requests.get(f"{API_URL}/scoreboard")
    st.write(resp.json())
