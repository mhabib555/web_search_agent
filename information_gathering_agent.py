from agents import ModelSettings, function_tool, handoff
from planning_agent import planning_agent
from config import base_agent

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


    
information_gathering_agent = base_agent.clone(
    name="InformationGatheringAgent",
    instructions=f"""
You are a Information Gathering Agent. Your task is to process the user's query that cover the main aspects.
If you cannot fully process the query due to missing information, call the tool `get_more_info_from_user` to gather additional details.
Return to Planning Agent with a JSON array of strings, for example: ["query 1", "query 2"].
After generating queries, hand off to the Planning Agent    
""",

    model_settings=ModelSettings(temperature=0.3, max_tokens=500),
    tools=[get_more_info_from_user],
    handoffs=[
        handoff(
            agent=planning_agent,
        )
    ]
)