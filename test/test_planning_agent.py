import pytest
from aiagents.planning_agent import planning_agent

def test_planning_agent_attributes():
    assert planning_agent.name == "PlanningAgent"
    assert callable(planning_agent.instructions)
    assert hasattr(planning_agent, "tools")
    assert hasattr(planning_agent, "handoffs")
    assert planning_agent.model_settings.temperature == 0.3
    assert planning_agent.model_settings.max_tokens == 1000

def test_planning_agent_tools_empty():
    assert isinstance(planning_agent.tools, list)
    assert len(planning_agent.tools) == 0

def test_planning_agent_handoff():
    assert len(planning_agent.handoffs) == 1
    handoff_obj = planning_agent.handoffs[0]
    assert hasattr(handoff_obj, "agent_name")
    assert handoff_obj.agent_name == "LeadResearcher"