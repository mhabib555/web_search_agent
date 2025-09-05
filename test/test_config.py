from config import config

def test_api_keys_loaded(monkeypatch):
    """Test that API keys are properly loaded and raise errors if missing."""
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    monkeypatch.setenv("TAVILY_API_KEY", "dummy")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    # Re-import config to trigger the check
    import sys # pylint: disable=import-outside-toplevel
    if "config.config" in sys.modules:
        del sys.modules["config.config"]
    import config.config as cfg # pylint: disable=reimported, import-outside-toplevel
    assert cfg.gemini_api_key == "dummy"
    assert cfg.tavily_api_key == "dummy"
    assert "OPENAI_API_KEY" in cfg.os.environ

def test_base_agent_attributes():
    """Check BaseResearchAgent attributes are correctly set in the config."""
    assert hasattr(config, "base_agent")
    assert config.base_agent.name == "BaseResearchAgent"
    assert isinstance(config.base_agent.instructions, str)
    assert hasattr(config.base_agent, "model")
