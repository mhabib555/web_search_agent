from agents import ModelSettings, RunContextWrapper, function_tool
from config.context import UserContext, SUBSCRIPTION_CONFIGS
from config.config import base_agent,tavily_client


@function_tool
async def web_search(query: str, max_results: int = 5) -> dict:
    """
    Perform a web search using Tavily API and return the results.
    
    Args:
        local_context: Context wrapper containing user information
        query: Search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Dictionary containing search results
    """
    response = await tavily_client.search(query=query, max_results=max_results)
    return response


# Research Agent
research_agent = base_agent.clone(
    name="ResearchAgent",
    instructions="""
You are a Research Agent tasked with gathering information using the Tavily API.
1. Receive a sub-query as input and the user context.
2. Determine search depth based on intent:
   - Use 1–3 results for queries with "summary" or "quick overview".
   - Use 7–10 results for queries with "more details" or "in-depth".
   - Use 5 results for other queries.
3. Perform a web search using the Tavily API with rate limiting based on the user's subscription tier.
4. Return must be a JSON object with the sub-query and search results (title, URL, content).
Output format: {"query": "sub-query", "results": [{"title": "...", "url": "...", "content": "..."}, ...]}
""",
    model_settings=ModelSettings(temperature=0.3, max_tokens=500),
    tools=[web_search]
)

# Source Checker Agent
source_checker_agent = base_agent.clone(
    name="SourceCheckerAgent",
    instructions="""
You are a Source Checker Agent tasked with evaluating the reliability of sources.
1. Receive a JSON array of sources (title, URL, content).
2. Rate each source as High, Medium, or Low reliability based on domain and content quality.
3. Return a JSON array with sources and their reliability ratings.
Output format: [{"title": "...", "url": "...", "content": "...", "reliability": "High/Medium/Low"}, ...]
""",
    model_settings=ModelSettings(temperature=0.2, max_tokens=500)
)

# Conflict Detector Agent
conflict_detector_agent = base_agent.clone(
    name="ConflictDetectorAgent",
    instructions="""
You are a Conflict Detector Agent tasked with identifying contradictions in research findings.
1. Receive research findings (sub-query, results).
2. Analyze results for contradictions across sub-queries.
3. Return a JSON object with identified conflicts or a message indicating no conflicts.
Output format: {"conflicts": [{"sub_query_1": "...", "sub_query_2": "...", "conflict": "..."}] or "message": "No conflicts detected"}
""",
    model_settings=ModelSettings(temperature=0.2, max_tokens=500)
)
