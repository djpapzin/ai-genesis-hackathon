import spacy
import re
from typing import List, Dict
from collections import Counter
from nltk.corpus import stopwords
import nltk
import pronouncing

# Load spaCy English model (make sure to run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

# Download stopwords if not already present
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> str:
    """
    Clean and normalize rap lyrics text.
    - Lowercase
    - Remove special characters (except apostrophes)
    - Remove extra whitespace
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s']", '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_named_entities(text: str) -> List[str]:
    """
    Extract named entities (names, places, brands, etc.) from text using spaCy.
    Returns a list of unique entity strings.
    """
    doc = nlp(text)
    entities = set()
    for ent in doc.ents:
        entities.add(ent.text)
    return list(entities)

def detect_style(text: str) -> str:
    """
    Detect the style of the rap (aggressive, witty, sarcastic, etc.) using keyword-based logic.
    Returns the detected style as a string.
    """
    style_keywords = {
        "aggressive": ["kill", "destroy", "crush", "battle", "war", "beat", "smash", "flex"],
        "witty": ["clever", "smart", "mind", "brain", "joke", "pun", "trick"],
        "sarcastic": ["yeah right", "sure", "as if", "please", "really", "nice try"],
        "boastful": ["best", "king", "queen", "number one", "top", "champion", "win", "rich", "money", "gold"]
    }
    text = text.lower()
    for style, keywords in style_keywords.items():
        for kw in keywords:
            if kw in text:
                return style
    return "neutral"

def extract_themes(text: str) -> List[str]:
    """
    Extract prominent themes from the rap using keyword-based logic.
    Returns a list of detected themes.
    """
    theme_keywords = {
        "money": ["money", "cash", "dollar", "bank", "rich", "stacks", "paid", "wealth", "gold"],
        "power": ["power", "control", "boss", "rule", "king", "queen", "leader"],
        "respect": ["respect", "honor", "fame", "glory", "props"],
        "struggle": ["struggle", "pain", "hard", "fight", "hustle", "grind", "survive"],
        "loyalty": ["loyal", "crew", "team", "family", "brother", "sister", "ride or die"]
    }
    text = text.lower()
    found_themes = set()
    for theme, keywords in theme_keywords.items():
        for kw in keywords:
            if kw in text:
                found_themes.add(theme)
    return list(found_themes)

def extract_slang(text: str) -> List[str]:
    """
    Extract slang words from the rap lyrics using a predefined slang list.
    Returns a list of slang words found in the text.
    """
    slang_list = [
        "ice", "whip", "drip", "flex", "lit", "dope", "crib", "bling", "squad", "fam", "goat", "cap", "no cap", "fire", "bars", "hustle", "grind", "plug", "trap", "banger", "clout"
    ]
    words = set(preprocess_text(text).split())
    found_slang = [word for word in slang_list if word in words]
    return found_slang

def extract_unique_phrases(text: str, min_freq: int = 2) -> List[str]:
    """
    Extract unique/repeated phrases or words from the rap lyrics.
    Returns a list of words/phrases that appear at least min_freq times and are not stopwords.
    """
    words = preprocess_text(text).split()
    filtered_words = [w for w in words if w not in stop_words]
    word_counts = Counter(filtered_words)
    unique = [word for word, count in word_counts.items() if count >= min_freq]
    return unique

def extract_rhyme_scheme(text: str) -> dict:
    """
    Analyze the rap lyrics to determine the rhyme scheme (e.g., AABB, ABAB).
    Returns a dictionary with:
      - 'rhyme_scheme': string (e.g., 'AABB')
      - 'labels': list of rhyme labels per line
      - 'end_words': list of last words per line
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    end_words = [line.split()[-1].lower() for line in lines if line.split()]
    labels = []
    rhyme_map = {}
    current_label = 'A'
    for i, word in enumerate(end_words):
        found = False
        for label, rhyme_word in rhyme_map.items():
            # Check if current word rhymes with any previous rhyme_word
            if set(pronouncing.rhymes(rhyme_word)) & set([word]):
                labels.append(label)
                found = True
                break
        if not found:
            rhyme_map[current_label] = word
            labels.append(current_label)
            current_label = chr(ord(current_label) + 1)
    rhyme_scheme = ''.join(labels)
    return {
        'rhyme_scheme': rhyme_scheme,
        'labels': labels,
        'end_words': end_words
    }

# Example usage
if __name__ == "__main__":
    sample_rap = "Yo, I'm Lil Flex from New York, counting stacks and driving my Benz!\nFlex on the beat, flex every week, my ice so cold, my drip so unique!"
    cleaned = preprocess_text(sample_rap)
    print("Cleaned:", cleaned)
    entities = extract_named_entities(sample_rap)
    print("Entities:", entities)
    style = detect_style(sample_rap)
    print("Style:", style)
    themes = extract_themes(sample_rap)
    print("Themes:", themes)
    slang = extract_slang(sample_rap)
    print("Slang:", slang)
    unique_phrases = extract_unique_phrases(sample_rap)
    print("Unique/Repeated Words:", unique_phrases)
    rhyme_info = extract_rhyme_scheme(sample_rap)
    print("Rhyme Scheme Info:", rhyme_info) 