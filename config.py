from agents import AsyncOpenAI, OpenAIChatCompletionsModel
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


gemini_api_key = os.getenv("GEMINI_API_KEY")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-lite",
    openai_client=external_client
)

# Initialize Tavily client
tavily_client = AsyncTavilyClient(api_key=tavily_api_key)
