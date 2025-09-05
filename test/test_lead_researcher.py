from aiagents.lead_research_agent import lead_research_agent

def test_lead_research_agent_attributes():
    """Verify attributes of LeadResearchAgent are correctly set."""
    assert lead_research_agent.name == "LeadResearchAgent"
    assert callable(lead_research_agent.instructions)
    assert hasattr(lead_research_agent, "tools")
    assert hasattr(lead_research_agent, "handoffs")

def test_lead_research_agent_tools():
    """Check if LeadResearchAgent has expected tools in its toolset."""
    tool_names = [tool.name for tool in lead_research_agent.tools]
    assert "research_agent" in tool_names
    assert "source_checker_agent" in tool_names
    assert "conflict_detector_agent" in tool_names

def test_lead_research_agent_handoff():
    """Test LeadResearchAgent handoff configuration and attributes."""
    assert len(lead_research_agent.handoffs) == 1
    handoff_obj = lead_research_agent.handoffs[0]
    assert hasattr(handoff_obj, "agent_name")
    assert handoff_obj.agent_name
