from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, function_tool, tool,  handoff
from planning_agent import planning_agent
from config import llm_model
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

@function_tool
def get_more_info_from_user(question: str) -> str:
    """
    Tool to ask the user for more information when needed.
    
    Args:
        question (str): The question to ask the user for clarification.
    
    Returns:
        str: The user's response or a default if no input provided.
    """
    print(f"\nLLM needs clarification: {question}")
    try:
        user_input = input("\nEnter your response (or press Enter to skip): ")
        return user_input if user_input.strip() else "Unknown"
    except Exception as e:
        print(f"Error getting user input: {e}")
        return "Unknown"


    
information_gathering_agent = Agent(
    name="InformationGatheringAgent",
    instructions=f"""
You are an Information Gathering Agent. Your task is to process the user's query and hand it off to the Planning Agent for further processing. Follow these steps:

1. Receive and analyze the user's query.
2. If the query is clear and complete, process it into a JSON array of strings (e.g., ["query 1", "query 2"]) and hand it off to the Planning Agent.
3. If the query is unclear or missing critical information, call the `get_more_info_from_user` tool to ask the user for clarification. Do not break the streaming loop; continue processing after receiving the response.
4. Incorporate the user's response from the tool into the query and repeat the analysis if necessary.
5. Once the query is fully processed, hand it off to the Planning Agent using the provided handoff mechanism.

Ensure you:
- Always use the `get_more_info_from_user` tool when clarification is needed.
- Maintain the streaming loop and do not terminate prematurely.
- Return the processed query as a JSON array of strings.
""",
# You are a Information Gathering Agent. Your task is to process the user's query that cover the main aspects.
# If you cannot fully process the query due to missing information, call the tool `get_more_info_from_user` to gather additional details.
# Return to Planning Agent with a JSON array of strings, for example: ["query 1", "query 2"].
# After generating queries, hand off to the Planning Agent    





    model=llm_model,
    model_settings=ModelSettings(temperature=0.3, max_tokens=500),
    tools=[get_more_info_from_user],
    handoffs=[
        handoff(
            agent=planning_agent,
        )
    ]
)