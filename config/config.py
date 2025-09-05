# Import required modules
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings
import os
from dotenv import load_dotenv, find_dotenv
from tavily import AsyncTavilyClient
import logging

# Configure logging for error handling
logging.basicConfig(
    level=logging.ERROR, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    # save errors to a file
    # filename='errors.log'
)
logger = logging.getLogger(__name__)

try:
    # Load environment variables from .env file
    if 'COLAB_GPU' in os.environ:  
        print("Running in Google Colab environment")      
    else: 
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
    selected_model = "flash-2.0"
    selected_lite_model = "flash-lite-2.0"
    if selected_model not in gemini_models:
        raise KeyError(f"Model {selected_model} not found in gemini_models")
    if selected_lite_model not in gemini_models:
        raise KeyError(f"Model {selected_lite_model} not found in gemini_models")

    # Configure language model with Gemini model
    llm_model = OpenAIChatCompletionsModel(
        model=gemini_models[selected_model],
        openai_client=external_client
    )

    # Configure language model with lightweight Gemini model
    llm_lite_model = OpenAIChatCompletionsModel(
        model=gemini_models[selected_lite_model],
        openai_client=external_client
    )

    # Initialize Tavily client for async web searches
    tavily_client = AsyncTavilyClient(api_key=tavily_api_key)

    # Create base agent for research tasks
    base_agent = Agent(
        name="BaseResearchAgent",
        instructions="You are a base agent for research tasks. This agent will be cloned for specific roles.",
        model=llm_model,
        # model_settings=ModelSettings(temperature=0.3, max_tokens=500)
    )


except ValueError as ve:
    logger.error(f"Configuration error: {str(ve)}")
    raise
except KeyError as ke:
    logger.error(f"Model selection error: {str(ke)}")
    raise
except Exception as e:
    logger.error(f"Unexpected error during setup: {str(e)}")
    raise