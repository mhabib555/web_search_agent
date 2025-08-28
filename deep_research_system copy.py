import os, asyncio, pprint
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, RunContextWrapper, ItemHelpers, function_tool, set_tracing_disabled
# importing web search api
from tavily import TavilyClient
from dataclasses import dataclass
from openai.types.responses import ResponseTextDeltaEvent
from fake_data import fake_users

# Disable tracing for cleaner logs during development
set_tracing_disabled(disabled=True)

# Load environment variables securely
load_dotenv(find_dotenv())
gemini_api_key=os.getenv("GEMINI_API_KEY")
tavily_api_key=os.getenv("TAVILY_API_KEY")

# Ensure API keys are available to prevent runtime errors
if not gemini_api_key or not tavily_api_key:
    raise ValueError("Missing required API keys")


@dataclass
class UserContext:
    """User context to store personal information and preferences.
    
    Attributes:
        name: The user's name.
        city: The user's city (optional).
        topic: The user's preferred topic (optional).
    """
    name: str
    city: str | None = None 
    topic: str | None = None

# Initialize Tavily web search client
tavily_client: TavilyClient = TavilyClient(
    api_key=tavily_api_key
)

# Configure LLM service with Gemini API
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Define LLM model for chat completions
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def web_search(local_context: RunContextWrapper[UserContext], query: str, max_results: int = 5) -> dict:
    """
    Perform a web search using Tavily API and return the results.
    
    Args:
        local_context: Context wrapper containing user information
        query: Search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        Dictionary containing search results
    """
    response = tavily_client.search(query=query, max_results=max_results)
    return response

def dynamic_instructions(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    """Generate dynamic instructions for the agent based on user context."""
    user_info = special_context.context

    return f"""
        You are {agent.name}, a helpful and concise web search expert. 
        You are currently assisting {user_info.name} from {user_info.city} who is interested in {user_info.topic}.

        Your task is to understand user queries and use the web_search tool to find relevant information.
        
        Adapt your search based on the user's intent:
        - If the user asks for a "summary" or a "quick overview", call the `web_search` tool with `max_results` from 1 to 3.
        - If the user asks for "more details" or "in-depth information", call the `web_search` tool with `max_results` from 7 to 10.
        - For all other queries, use the default `max_results=5`.

        Your response should be followed by a summary accordingly to user's intent and followed by a bulleted list of links from the search results.
    """

# Initialize the agent with clear instructions and tools
agent: Agent = Agent(
    name="SearchAssistant",
    instructions=dynamic_instructions,
    model=llm_model,
    model_settings=ModelSettings(temperature=0.1, max_tokens=1000),
    tools=[web_search]
)

# change mock data user profile
def change_user():
    # Allow user to select from mock data
    print("Available Users:")
    for i, user in enumerate(fake_users):
        print(f"[{i}]: {user['name']} (from {user['city']}, likes {user['topic']})")
    
    user_choice = input("Enter the number of the user you want to be (default: 1): ")
    try:
        user_index = int(user_choice) if user_choice else 1
        if not 0 <= user_index < len(fake_users):
            user_index = 1
            print(f"Invalid choice. Defaulting to user {user_index}.")
        return user_index
    except ValueError:
        user_index = 1
        print(f"Invalid input. Defaulting to user {user_index}.")
        return user_index

# set mock data user profile in UserContext
def set_user(user_index: int = 1):
    return UserContext(
        name=fake_users[user_index]['name'], 
        city=fake_users[user_index]['city'], 
        topic=fake_users[user_index]['topic']
    )

async def call_agent():

    user_info = set_user(user_index=1)

    while True:
        try: 
            user_input = input("Enter your query (type exit to exit, type change to change user): ")

            if user_input.lower() == 'exit':
                break  # Exit the loop if the user types 'exit'
            elif user_input.lower() == 'change':
                user_info = set_user(change_user())
            else:
                response = Runner.run_streamed(
                    starting_agent=agent,
                    input=user_input,
                    context=user_info
                )

                print("\n=== Agent's Process ===")
                async for event in response.stream_events():
                    # We'll ignore the raw responses event deltas
                    if event.type == "raw_response_event":
                        continue
                    elif event.type == "agent_updated_stream_event":
                        # print(f"Agent updated: {event.new_agent.name}")
                        continue
                    elif event.type == "run_item_stream_event":
                        # if event.item.type == "tool_call_item":
                        #     print("-- Tool was called")
                        # elif event.item.type == "tool_call_output_item":
                        #     print(f"-- Tool output: {event.item.output}")
                        # el
                        if event.item.type == "message_output_item":
                            print(f"\nAssistant:\n {ItemHelpers.text_message_output(event.item)}")
                        else:
                            pass  # Ignore other event types

                print("=== Process complete ===\n")

        except Exception as e:
            print(f"Error processing query: {e}")    


if __name__ == "__main__":
    asyncio.run(call_agent())
