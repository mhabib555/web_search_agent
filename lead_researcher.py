from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, RunContextWrapper, handoff
from synthesis_agent import synthesis_agent
from research_agents import research_agent, source_checker_agent, conflict_detector_agent
from context import UserContext, SUBSCRIPTION_CONFIGS
from config import llm_model 

def lead_researcher_instructions(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    """Generate dynamic instructions for the Lead Research Agent based on user context."""

    print('\nLead', agent.name)

    user_info = special_context.context
    subscription_tier = user_info.subscription[0] if user_info.subscription else "free"
    
    print(SUBSCRIPTION_CONFIGS[subscription_tier])
    return f"""
You are LeadResearcher, a lead research orchestrator assisting {user_info.name} from {user_info.city}, interested in {user_info.topic} with a {subscription_tier} subscription.
Your task is to manage a team of specialist agents to conduct in-depth research on the user's query.
1. Receive sub-queries from the Planning Agent.
2. Assign sub-queries to the Research Agent, adapting search depth based on intent:
   - Use 1–3 results for queries with "summary" or "quick overview".
   - Use 7–10 results for queries with "more details" or "in-depth".
   - Use 5 results for other queries.
3. Pass sources (title, URL, content) from Research Agent to the Source Checker Agent for reliability ratings.
4. Pass findings to the Conflict Detector Agent to identify contradictions.
5. Hand off findings (combine all) to the Synthesis Agent, which will produce a report and hand off to the Report Writer Agent.
6. Return the final report to the user.
Input is sub-queries. Output the final report as a string after coordinating with all agents.
Ensure the research is tailored to the user's interests ({user_info.topic}) and respects the rate limits of the {subscription_tier} subscription.
"""


lead_researcher = Agent(
    name="LeadResearcher",
    instructions=lead_researcher_instructions,
    model=llm_model,
#    model_settings=ModelSettings(temperature=0.3, max_tokens=1500),
    handoffs=[handoff(synthesis_agent)],
    tools=[
        research_agent.as_tool(
            tool_name="research_agent",
            tool_description="Performs web searches using the Tavily API to gather information on a given sub-query, adapting search depth based on intent."
        ),
        source_checker_agent.as_tool(
            tool_name="source_checker_agent",
            tool_description="Evaluates the reliability of sources, rating them as High, Medium, or Low based on domain and content."
        ),
        conflict_detector_agent.as_tool(
            tool_name="conflict_detector_agent",
            tool_description="Analyzes research findings to identify contradictions or conflicts across sub-queries."
        )
    ]
)