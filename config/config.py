"""
Configures and initializes core components.
"""

import os
import logging
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel
from tavily import AsyncTavilyClient

# Configure logging for error handling
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    # save errors to a file
    # filename='errors.log'
)
logger = logging.getLogger(__name__)

try:
    # Load environment variables conditionally
    # This ensures it works on both local and CI environments
    if os.getenv('CI') != 'true':
        # Only load the .env file if we are not in a CI environment
        load_dotenv(find_dotenv())

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Validate API keys
    if not gemini_api_key or not tavily_api_key or not openai_api_key:
        raise ValueError("Missing required API keys")

    # Set OpenAI API key for SDK tracing
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Initialize async OpenAI client for Gemini API
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Map model aliases to Gemini model names
    gemini_models: dict[str, str] = {
        "pro-2.5": "gemini-2.5-pro",
        "flash-2.5": "gemini-2.5-flash",
        "flash-2.0": "gemini-2.0-flash",
        "flash-lite-2.0": "gemini-2.0-flash-lite",
    }

    # Verify selected model exists
    SELECTED_MODEL = "flash-2.0"
    SELECTED_LITE_MODEL = "flash-lite-2.0"
    if SELECTED_MODEL not in gemini_models:
        raise KeyError(f"Model {SELECTED_MODEL} not found in gemini_models")
    if SELECTED_LITE_MODEL not in gemini_models:
        raise KeyError(f"Model {SELECTED_LITE_MODEL} not found in gemini_models")

    # Configure language model with Gemini model
    llm_model = OpenAIChatCompletionsModel(
        model=gemini_models[SELECTED_MODEL],
        openai_client=external_client
    )

    # Configure language model with lightweight Gemini model
    llm_lite_model = OpenAIChatCompletionsModel(
        model=gemini_models[SELECTED_LITE_MODEL],
        openai_client=external_client
    )

    # Initialize Tavily client for async web searches
    tavily_client = AsyncTavilyClient(api_key=tavily_api_key)

    # Create base agent for research tasks
    base_agent = Agent(
        name="BaseResearchAgent",
        instructions="You are a base agent for research tasks. This agent will be cloned for specific roles.",
        model=llm_model,
    )


except ValueError as ve:
    logger.error("Configuration error: %s", str(ve))
    raise
except KeyError as ke:
    logger.error("Model selection error: %s", str(ke))
    raise
except Exception as e:
    logger.error("Unexpected error during setup: %s", str(e))
    raise
