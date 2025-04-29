"""
Basic test for CypherGPT project structure.
"""

def test_import_main():
    try:
        import src.main
    except Exception as e:
        assert False, f"Import failed: {e}"
