from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, RunContextWrapper, handoff
from lead_researcher import lead_researcher
from context import UserContext, SUBSCRIPTION_CONFIGS
from dotenv import load_dotenv, find_dotenv
from config import llm_model


def planning_agent_instructions(cxt: RunContextWrapper[UserContext], agent) -> str:
    """Generate dynamic instructions for the Planning Agent based on user context and the query."""

    user_info = cxt.context
    subscription_tier = user_info.subscription[0] if user_info.subscription else "free"

    return f"""
You are a Research Planning Agent. Your task is to break down the user's complex question into 3-5 specific sub-questions or research tasks that cover the main aspects and hand off these sub-questions to the Lead Researcher.

Follow these steps:
1. Analyze the user's query using the provided context (name, city, topic) to ensure relevance.
2. Generate 3-5 specific sub-questions or research tasks as a JSON array of strings (e.g., ["sub-question 1", "sub-question 2"]).
3. Do not output the JSON array directly to the user.
4. Hand off the generated sub-questions to the Lead Researcher Agent using the provided handoff mechanism.
5. Ensure the streaming loop is maintained and does not break during processing or handoff.

Additional guidelines:
- Use the user context to tailor sub-questions to the user's interests.
- API Subscriptions config: {SUBSCRIPTION_CONFIGS[subscription_tier]}.
- Do not terminate the process prematurely; always complete the handoff to the Lead Researcher.
"""
# Use the user context (name, city, topic) to ensure sub-questions are relevant to the user's interests.

# You are a Research Planning Agent. Your task is to break down the user's complex question into 3-5 specific sub-questions or research tasks that cover the main aspects and hand off to the Lead Researcher.
# Return to Lead Researcher Agent with a JSON array of strings, for example: ["sub-question 1", "sub-question 2"]. Don't output to the user directly.
# After generating sub-queries, hand off to the Lead Researcher Agent.
# API Subscriptions config are {SUBSCRIPTION_CONFIGS[subscription_tier]}



def handoff_to_lead(cxt):
    print("Handoff to lead agent")

planning_agent = Agent(
    name="PlanningAgent",
    instructions=planning_agent_instructions,
    model=llm_model,
    model_settings=ModelSettings(temperature=0.3, max_tokens=500),
    tools=[],
    handoffs=[
        handoff(
            agent=lead_researcher,
            on_handoff=handoff_to_lead,
        )
    ]
)