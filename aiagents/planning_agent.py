from agents import RunContextWrapper, ModelSettings, handoff
from aiagents.lead_research_agent import lead_research_agent
from config.context import UserContext, SUBSCRIPTION_CONFIGS
from config.config import base_agent


def planning_agent_instructions(cxt: RunContextWrapper[UserContext], agent) -> str:
    """Generate dynamic instructions for the Planning Agent based on user context and the query."""

    user_info = cxt.context
    subscription_tier = user_info.subscription[0] if user_info.subscription else "free"

    return f"""
You are a Research Planning Agent. Generate sub-questions and hand them off to the Lead Research agent.

Your Job:
1. Analyze the user's query using the provided context (name={user_info.name}, city={user_info.city}, topic={user_info.topic}) to ensure relevance.
2. Generate 3-5 specific sub-questions that will help in gathering comprehensive information related to the user's query.
3. Handoff/Pass these sub-questions to the Lead Research agent in a structured JSON array format.

Additional guidelines:
- Consider API Subscriptions Rate limits: {SUBSCRIPTION_CONFIGS[subscription_tier]}.
"""



planning_agent = base_agent.clone(
    name="PlanningAgent",
    instructions=planning_agent_instructions,
    model_settings=ModelSettings(temperature=0.3, max_tokens=1000),
    tools=[],
    handoffs=[
        handoff(
            agent=lead_research_agent,
        )
    ]
)