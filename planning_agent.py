from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, RunContextWrapper, handoff
from lead_researcher import lead_researcher
from context import UserContext
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=external_client
)

def planning_agent_instructions(cxt: RunContextWrapper[UserContext], agent) -> str:
    special_context = cxt.context
    """Generate dynamic instructions for the Planning Agent based on user context and the query."""
    print(f"Planning Agent received context: {special_context}")
    subscription_tier = special_context.subscription[0] if special_context.subscription else "free"

    return f"""
You are a Research Planning Agent. Your role is to decompose a user's complex query into 3-5 clear, focused sub-questions or research tasks that collectively address the query's core components. Ensure the sub-questions are:
- Specific, actionable, and relevant to the user's interests.
- Tailored to the user's context: 
  - Name: {special_context.name or 'Unknown'}
  - City: {special_context.city or 'Unknown'}
  - Topic: {special_context.topic or 'General'}
- Compliant with the rate limits of the {subscription_tier} subscription tier.

Steps:
1. Analyze the user's query to identify its main themes and objectives.
2. Formulate 3-5 sub-questions that break down the query into manageable, distinct tasks.
3. Pass the generated sub-questions to the Lead Researcher Agent for further processing.
"""


def handoff_to_lead(cxt):
    print("Handoff to lead agent")

planning_agent = Agent(
    name="PlanningAgent",
    instructions=planning_agent_instructions,
    model=llm_model,
#    model_settings=ModelSettings(temperature=0.3, max_tokens=500),
    tools=[],
    handoffs=[
        handoff(
            agent=lead_researcher,
            on_handoff=handoff_to_lead,
            tool_name_override="LeadResearcher"
        )
    ]
)