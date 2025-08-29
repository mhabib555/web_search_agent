from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings
import os
from dotenv import load_dotenv, find_dotenv
from tavily import AsyncTavilyClient

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Enable OpenAI SDK tracing
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if not gemini_api_key or not tavily_api_key or not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Missing required API keys")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Initialize Tavily client
tavily_client = AsyncTavilyClient(api_key=tavily_api_key)

# Base agent for cloning
base_agent = Agent(
    name="BaseResearchAgent",
    instructions="You are a base agent for research tasks. This agent will be cloned for specific roles.",
    model=llm_model,
    # model_settings=ModelSettings(temperature=0.3, max_tokens=500)
)
