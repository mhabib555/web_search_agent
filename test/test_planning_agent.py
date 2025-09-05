import pytest
from aiagents.planning_agent import planning_agent
from aiagents.planning_agent_runner import run_planning_agent
from config.context import UserContext, InformationGatheringAnswer

def test_planning_agent_attributes():
    """Verify PlanningAgent attributes and model settings are correctly configured."""
    assert planning_agent.name == "PlanningAgent"
    assert callable(planning_agent.instructions)
    assert hasattr(planning_agent, "tools")
    assert hasattr(planning_agent, "handoffs")
    assert planning_agent.model_settings.temperature == 0.3
    assert planning_agent.model_settings.max_tokens == 1500

def test_planning_agent_tools_empty():
    """Check that PlanningAgent has an empty tools list."""
    assert isinstance(planning_agent.tools, list)
    assert len(planning_agent.tools) == 0

def test_planning_agent_handoff():
    """Test PlanningAgent handoff configuration and attributes."""
    assert len(planning_agent.handoffs) == 1
    handoff_obj = planning_agent.handoffs[0]
    assert hasattr(handoff_obj, "agent_name")
    assert handoff_obj.agent_name == "LeadResearchAgent"


@pytest.mark.asyncio
async def test_run_planning_agent():
    """Test running the planning agent with query."""
    user_context = UserContext(name="Alice", city="Chicago", topic="AI", subscription="free")

    query: InformationGatheringAnswer = InformationGatheringAnswer(
        is_information_complete=True,
        data="How did the adoption of server-side rendering with Laravel improve page load times of websites, concise"
    )

    result = await run_planning_agent(
        query, user_context, session=None
    )

    assert result is not None
