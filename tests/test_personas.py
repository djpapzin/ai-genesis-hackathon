"""
Tests for the personas module.
"""
import pytest
from src.personas import PersonaManager, PersonaStyle

def test_persona_manager_initialization():
    manager = PersonaManager()
    assert len(manager.personas) > 0
    assert "eminem" in manager.personas
    assert "tupac" in manager.personas
    assert "kendrick" in manager.personas
    assert "shakespeare" in manager.personas

def test_get_persona():
    manager = PersonaManager()
    eminem = manager.get_persona("eminem")
    assert isinstance(eminem, PersonaStyle)
    assert eminem.name == "Eminem"
    assert eminem.tone == "aggressive"
    
    # Test case insensitivity
    eminem_upper = manager.get_persona("EMINEM")
    assert eminem_upper == eminem
    
    # Test non-existent persona
    assert manager.get_persona("nonexistent") is None

def test_list_personas():
    manager = PersonaManager()
    personas = manager.list_personas()
    assert isinstance(personas, list)
    assert "eminem" in personas
    assert "tupac" in personas
    assert len(personas) == 4

def test_get_prompt_for_battle():
    manager = PersonaManager()
    context = {
        "round_number": 1,
        "battle_context": "Championship finals"
    }
    prompt = manager.get_prompt_for_battle("eminem", "You can't rap", context)
    
    # Check if prompt contains all necessary elements
    assert "Eminem" in prompt
    assert "You can't rap" in prompt
    assert "Round: 1" in prompt
    assert "Championship finals" in prompt
    
    # Test with invalid persona
    with pytest.raises(ValueError, match="Persona 'invalid' not found"):
        manager.get_prompt_for_battle("invalid", "test", {}) 