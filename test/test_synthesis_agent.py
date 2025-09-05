import pytest
from aiagents.synthesis_agent import synthesis_agent

def test_synthesis_agent_attributes():
    assert synthesis_agent.name == "SynthesisAgent"
    assert isinstance(synthesis_agent.instructions, str)
    assert hasattr(synthesis_agent, "model_settings")
    assert synthesis_agent.model_settings.temperature == 0.3
    assert synthesis_agent.model_settings.max_tokens == 1500
    assert hasattr(synthesis_agent, "handoffs")
    assert len(synthesis_agent.handoffs) == 1

def test_synthesis_agent_handoff():
    handoff_obj = synthesis_agent.handoffs[0]
    assert hasattr(handoff_obj, "agent_name")
    assert handoff_obj.agent_name == "ReportWriterAgent"
    # Check for tool_name_override if present
    if hasattr(handoff_obj, "tool_name_override"):
        assert handoff_obj.tool_name_override == "ReportWriterAgent"