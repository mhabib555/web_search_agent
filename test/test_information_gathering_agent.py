import pytest
from aiagents.information_gathering_agent import information_gathering_agent
from aiagents.information_gathering_runner import run_information_gathering_agent
from config.context import UserContext, InformationGatheringAnswer

def test_information_gathering_agent_attributes():
    """Test the basic attributes of the InformationGatheringAgent."""
    assert information_gathering_agent.name == "InformationGatheringAgent"
    assert hasattr(information_gathering_agent, "instructions")
    assert hasattr(information_gathering_agent, "tools")
    assert hasattr(information_gathering_agent, "handoffs")
    assert information_gathering_agent.model_settings.temperature == 0.3
    assert information_gathering_agent.model_settings.max_tokens == 500

def test_information_gathering_agent_tools():
    """Test that the agent has the correct tools configured."""
    tool_names = [tool.name for tool in information_gathering_agent.tools]
    assert "get_more_info_from_user" in tool_names

@pytest.mark.asyncio
async def test_run_information_gathering_agent():
    """Test running the information gathering agent with complete query."""
    user_context = UserContext(name="Alice", city="Chicago", topic="AI", subscription="free")

    default_query = "How did the adoption of server-side rendering with Laravel improve page load times of websites, concise?"
    result:InformationGatheringAnswer = await run_information_gathering_agent(
        default_query, user_context, session=None
    )

    # --- Flexible assertions depending on what runner returns ---
    assert result is not None

    if isinstance(result, InformationGatheringAnswer):
        assert result.is_information_complete in [True, False]
        assert isinstance(result.data, str)

    else:
        pytest.fail(f"Unexpected return type from run_information_gathering_agent: {type(result)}")
