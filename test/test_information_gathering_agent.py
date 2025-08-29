import pytest
from aiagents.information_gathering_agent import information_gathering_agent

def test_information_gathering_agent_attributes():
    assert information_gathering_agent.name == "InformationGatheringAgent"
    assert hasattr(information_gathering_agent, "instructions")
    assert hasattr(information_gathering_agent, "tools")
    assert hasattr(information_gathering_agent, "handoffs")
    assert information_gathering_agent.model_settings.temperature == 0.3
    assert information_gathering_agent.model_settings.max_tokens == 500

def test_information_gathering_agent_tools():
    tool_names = [tool.name for tool in information_gathering_agent.tools]
    assert "get_more_info_from_user" in tool_names

def test_information_gathering_agent_handoff():
    # Check that the handoff is set to the planning_agent
    assert len(information_gathering_agent.handoffs) == 1
    handoff_obj = information_gathering_agent.handoffs[0]
    assert hasattr(handoff_obj, "agent_name")
    assert handoff_obj.agent_name == "PlanningAgent"
