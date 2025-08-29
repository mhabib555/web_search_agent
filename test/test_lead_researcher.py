import pytest
from aiagents.lead_researcher import lead_researcher

def test_lead_researcher_attributes():
    assert lead_researcher.name == "LeadResearcher"
    assert callable(lead_researcher.instructions)
    assert hasattr(lead_researcher, "tools")
    assert hasattr(lead_researcher, "handoffs")

def test_lead_researcher_tools():
    tool_names = [tool.name for tool in lead_researcher.tools]
    assert "research_agent" in tool_names
    assert "source_checker_agent" in tool_names
    assert "conflict_detector_agent" in tool_names

def test_lead_researcher_handoff():
    assert len(lead_researcher.handoffs) == 1
    handoff_obj = lead_researcher.handoffs[0]
    assert hasattr(handoff_obj, "agent_name")
    assert handoff_obj.agent_name