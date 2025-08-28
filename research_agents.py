import os
import asyncio
import json
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, RunContextWrapper, function_tool
from tavily import AsyncTavilyClient
from typing import Dict, Any
from context import UserContext, SUBSCRIPTION_CONFIGS
from ratelimit import limits, sleep_and_retry

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not gemini_api_key or not tavily_api_key:
    raise ValueError("Missing required API keys")

# Initialize Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Initialize Tavily client
tavily_client = AsyncTavilyClient(api_key=tavily_api_key)

# Define Gemini model
llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=external_client
)

@function_tool
async def web_search(local_context: RunContextWrapper[UserContext], query: str, max_results: int = 5) -> dict:
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

# Base agent for cloning
base_research_agent = Agent(
    name="BaseResearchAgent",
    instructions="You are a base agent for research tasks. This agent will be cloned for specific roles.",
    model=llm_model,
    # model_settings=ModelSettings(temperature=0.3, max_tokens=500)
)

# Research Agent
research_agent = base_research_agent.clone(
    name="ResearchAgent",
    instructions="""
You are a Research Agent tasked with gathering information using the Tavily API.
1. Receive a sub-query as input and the user context.
2. Determine search depth based on intent:
   - Use 1–3 results for queries with "summary" or "quick overview".
   - Use 7–10 results for queries with "more details" or "in-depth".
   - Use 5 results for other queries.
3. Perform a web search using the Tavily API with rate limiting based on the user's subscription tier.
4. Return a JSON object with the sub-query and search results (title, URL, content) back to Lead Reseacher Agent.
Output format: {"query": "sub-query", "results": [{"title": "...", "url": "...", "content": "..."}, ...]}
""",
    # model_settings=ModelSettings(temperature=0.3, max_tokens=500),
    tools=[web_search]
)

# Source Checker Agent
source_checker_agent = base_research_agent.clone(
    name="SourceCheckerAgent",
    instructions="""
You are a Source Checker Agent tasked with evaluating the reliability of sources.
1. Receive a JSON array of sources (title, URL, content).
2. Rate each source as High, Medium, or Low reliability based on domain and content quality.
3. Return a JSON array with sources and their reliability ratings back to Lead Reseacher Agent.
Output format: [{"title": "...", "url": "...", "content": "...", "reliability": "High/Medium/Low"}, ...]
""",
    # model_settings=ModelSettings(temperature=0.2, max_tokens=500)
)

# Conflict Detector Agent
conflict_detector_agent = base_research_agent.clone(
    name="ConflictDetectorAgent",
    instructions="""
You are a Conflict Detector Agent tasked with identifying contradictions in research findings.
1. Receive research findings (sub-query, results).
2. Analyze results for contradictions across sub-queries.
3. Return a JSON object with identified conflicts or a message indicating no conflicts back to Lead Reseacher Agent.
Output format: {"conflicts": [{"sub_query_1": "...", "sub_query_2": "...", "conflict": "..."}] or "message": "No conflicts detected"}
""",
    # model_settings=ModelSettings(temperature=0.2, max_tokens=500)
)

