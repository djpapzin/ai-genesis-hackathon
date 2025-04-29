# CypherGPT

CypherGPT is an AI-powered rap battle game show platform that generates, analyzes, and scores rap battles using advanced language models. It supports:

- **Player vs AI** and **Player vs Player** rap battles
- **Tone and persona selection** (e.g., aggressive, witty, "Rap as Eminem")
- **AI Coach** mode for feedback and improvement
- **Freestyle** mode for unscored creative rapping
- **Persistent scoreboard** and round tracking
- **Personalization, rhyme, and punchline analysis**

---

## Quickstart

### 1. Install dependencies
```bash
pip install -r requirements.txt
- **Slang Extraction:** Finds slang words using a predefined slang list.
- **Unique Phrase Extraction:** Identifies repeated or unique words/phrases.
- **Rhyme Scheme Extraction:** Analyzes rhyme patterns and assigns rhyme labels using the pronouncing library.

### Example Usage
```python
from src.personalization import (
    preprocess_text, extract_named_entities, detect_style, extract_themes,
    extract_slang, extract_unique_phrases, extract_rhyme_scheme
)

sample_rap = """Yo, I'm Lil Flex from New York, counting stacks and driving my Benz!
Flex on the beat, flex every week, my ice so cold, my drip so unique!"""

cleaned = preprocess_text(sample_rap)
entities = extract_named_entities(sample_rap)
style = detect_style(sample_rap)
themes = extract_themes(sample_rap)
slang = extract_slang(sample_rap)
unique_phrases = extract_unique_phrases(sample_rap)
rhyme_info = extract_rhyme_scheme(sample_rap)

print("Cleaned:", cleaned)
print("Entities:", entities)
print("Style:", style)
print("Themes:", themes)
print("Slang:", slang)
print("Unique/Repeated Words:", unique_phrases)
print("Rhyme Scheme Info:", rhyme_info)
```

---

*Created for the AI Genesis Hackathon, 2025*
