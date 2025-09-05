from aiagents.research_agents import research_agent, source_checker_agent, conflict_detector_agent

def test_research_agent_attributes():
    """Verify ResearchAgent attributes and model settings are correctly configured."""
    assert research_agent.name == "ResearchAgent"
    assert isinstance(research_agent.instructions, str)
    assert hasattr(research_agent, "tools")
    assert research_agent.model_settings.temperature == 0.3
    assert research_agent.model_settings.max_tokens == 500

def test_research_agent_tools():
    """Check that ResearchAgent includes the web_search tool."""
    tool_names = [tool.name for tool in research_agent.tools]
    assert "web_search" in tool_names

def test_source_checker_agent_attributes():
    """Verify SourceCheckerAgent attributes and model settings are correctly set."""
    assert source_checker_agent.name == "SourceCheckerAgent"
    assert isinstance(source_checker_agent.instructions, str)
    assert source_checker_agent.model_settings.temperature == 0.2
    assert source_checker_agent.model_settings.max_tokens == 500

def test_conflict_detector_agent_attributes():
    """Verify ConflictDetectorAgent attributes and model settings are correctly set."""
    assert conflict_detector_agent.name == "ConflictDetectorAgent"
    assert isinstance(conflict_detector_agent.instructions, str)
    assert conflict_detector_agent.model_settings.temperature == 0.2
    assert conflict_detector_agent.model_settings.max_tokens == 500
