import pytest
import types
from aiagents.information_gathering_agent import information_gathering_agent
from config.context import UserContext
from config.fake_data import fake_users

def test_imports_and_user_context():
    # Test that the agent and user context can be created without error
    user_index = 1
    user_context = UserContext(
        name=fake_users[user_index]['name'],
        city=fake_users[user_index]['city'],
        topic=fake_users[user_index]['topic'],
        subscription=fake_users[user_index]['subscription']
    )
    assert user_context.name == fake_users[user_index]['name']
    assert user_context.city == fake_users[user_index]['city']
    assert user_context.topic == fake_users[user_index]['topic']
    assert user_context.subscription == fake_users[user_index]['subscription']
    assert information_gathering_agent.name == "InformationGatheringAgent"

def test_main_is_async():
    # Import the main function and check if it's a coroutine
    import deep_research_system
    assert hasattr(deep_research_system, "main")