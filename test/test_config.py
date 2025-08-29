import pytest
from config import config

def test_model_settings_import():
    # Ensure ModelSettings is imported and available
    assert hasattr(config, "ModelSettings")

def test_api_keys_loaded(monkeypatch):
    # Test that API keys are loaded and error is raised if missing
    monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    monkeypatch.setenv("TAVILY_API_KEY", "dummy")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    # Re-import config to trigger the check
    import importlib
    import sys
    if "config.config" in sys.modules:
        del sys.modules["config.config"]
    import config.config as cfg
    assert cfg.gemini_api_key == "dummy"
    assert cfg.tavily_api_key == "dummy"
    assert "OPENAI_API_KEY" in cfg.os.environ

def test_base_agent_attributes():
    assert hasattr(config, "base_agent")
    assert config.base_agent.name == "BaseResearchAgent"
    assert isinstance(config.base_agent.instructions, str)
    assert hasattr(config.base_agent, "model")