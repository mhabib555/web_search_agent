from agents import Agent, RunContextWrapper, ModelSettings, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from aiagents.synthesis_agent import synthesis_agent
from aiagents.research_agents import research_agent, source_checker_agent, conflict_detector_agent
from config.context import UserContext
from config.config import base_agent

def lead_research_agent_instructions(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    """Generate dynamic instructions for the Lead Research Agent based on user context."""

    user_info = special_context.context
    subscription_tier = user_info.subscription[0] if user_info.subscription else "free"

    if(subscription_tier == "free"):
        subqueires_limit = 2
        use_results_for_summary = "1-2"
        use_results_for_details = "2-3"
    else:
        subqueires_limit = 5
        use_results_for_summary = "1-3"
        use_results_for_details = "7-10"

    return f"""
{RECOMMENDED_PROMPT_PREFIX}
You are Lead Research Agent, a lead research orchestrator assisting {user_info.name}.
Your task is to manage a team of specialist agents to conduct in-depth research on the user's query. You operate as a backend agent and **must not** produce user-facing language or interact directly with the user. Your output is strictly for internal use by other agents.

Your Job:
1. Receive sub-queries from the Planning Agent.
2. Assign sub-queries to the Research Agent one by one, adapting search depth based on intent:
   - Use {use_results_for_summary} results for queries with "summary" or "quick overview".
   - Use {use_results_for_details} results for queries with "more details" or "in-depth".
   - Use {subqueires_limit} results for other queries.
3. Pass sources (title, URL, content) from Research Agent to the Source Checker Agent for reliability ratings.
4. Pass findings to the Conflict Detector Agent to identify contradictions.
5. Hand off findings (combine all) to the Synthesis Agent, which will produce a report and hand off to the Report Writer Agent.
6. Do NOT produce conversational text, such as "I will ask" or "I will generate," in your output.
"""


lead_research_agent = base_agent.clone(
    name="LeadResearchAgent",
    instructions=lead_research_agent_instructions,
    model_settings=ModelSettings(temperature=0.3),
    handoffs=[handoff(synthesis_agent)],
    tools=[
        research_agent.as_tool(
            tool_name="research_agent",
            tool_description="Performs web searches using the Tavily API to gather information on a given sub-query, adapting search depth based on intent.",
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
