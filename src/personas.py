"""
Module for managing rap battle personas and their characteristics.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel

class PersonaStyle(BaseModel):
    name: str
    description: str
    tone: str
    era: str
    signature_phrases: List[str]
    style_traits: List[str]
    prompt_template: str

class PersonaManager:
    def __init__(self):
        self.personas: Dict[str, PersonaStyle] = {
            "eminem": PersonaStyle(
                name="Eminem",
                description="Technical, aggressive rapper known for complex rhyme schemes and wordplay",
                tone="aggressive",
                era="2000s",
                signature_phrases=["slim shady", "guess who's back", "mom's spaghetti"],
                style_traits=["multi-syllabic rhymes", "rapid-fire delivery", "personal attacks"],
                prompt_template=(
                    "Respond as Eminem with his signature aggressive style, "
                    "complex rhyme patterns, and clever wordplay. "
                    "Include technical multi-syllabic rhymes and quick-witted responses."
                )
            ),
            "tupac": PersonaStyle(
                name="2Pac",
                description="Conscious rapper known for powerful social commentary and emotional depth",
                tone="passionate",
                era="1990s",
                signature_phrases=["thug life", "keep ya head up", "against all odds"],
                style_traits=["social consciousness", "emotional depth", "street poetry"],
                prompt_template=(
                    "Channel 2Pac's passionate delivery style with deep social consciousness. "
                    "Mix street wisdom with poetic expression and emotional depth. "
                    "Include references to struggle and resilience."
                )
            ),
            "kendrick": PersonaStyle(
                name="Kendrick Lamar",
                description="Lyrical storyteller with complex narratives and varied vocal delivery",
                tone="introspective",
                era="2010s",
                signature_phrases=["kung fu kenny", "what's the yams", "i remember you was conflicted"],
                style_traits=["storytelling", "voice modulation", "metaphorical complexity"],
                prompt_template=(
                    "Adopt Kendrick Lamar's introspective storytelling style with complex metaphors. "
                    "Use varied vocal tones and incorporate storytelling elements. "
                    "Mix personal narrative with broader themes."
                )
            ),
            "shakespeare": PersonaStyle(
                name="Shakespeare",
                description="Classical wordsmith adapting Shakespearean style to rap battles",
                tone="eloquent",
                era="Classical",
                signature_phrases=["thou art", "wherefore", "methinks"],
                style_traits=["iambic pentameter", "classical references", "elaborate metaphors"],
                prompt_template=(
                    "Write in Shakespearean style adapted for rap battles. "
                    "Use classical language, elaborate metaphors, and references to mythology. "
                    "Maintain iambic rhythm while delivering clever insults."
                )
            )
        }
    
    def get_persona(self, name: str) -> Optional[PersonaStyle]:
        """Get a persona by name (case-insensitive)."""
        return self.personas.get(name.lower())
    
    def list_personas(self) -> List[str]:
        """Get a list of available persona names."""
        return list(self.personas.keys())
    
    def get_prompt_for_battle(self, persona_name: str, opponent_text: str, context: Dict) -> str:
        """Generate a battle prompt for the selected persona."""
        persona = self.get_persona(persona_name.lower())
        if not persona:
            raise ValueError(f"Persona '{persona_name}' not found")
            
        prompt = f"{persona.prompt_template}\n\n"
        prompt += f"Opponent's text: {opponent_text}\n"
        
        if context.get('round_number'):
            prompt += f"Round: {context['round_number']}\n"
        
        if context.get('battle_context'):
            prompt += f"Battle context: {context['battle_context']}\n"
            
        return prompt 