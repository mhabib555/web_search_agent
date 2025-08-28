from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, function_tool, handoff
from planning_agent import planning_agent
from fake_data import fake_users
from context import UserContext
from dataclasses import dataclass
import os
import json
import random
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=external_client
)

@function_tool
def get_more_info_from_user( query : str ) -> str:
    print(query)
    return input(query).strip()



    
information_gathering_agent = Agent(
    name="InformationGatheringAgent",
    instructions="""
You are an Information Gathering Agent. Your task is to process the user's query and handoff the processed query to the planning agent for further processing.   

Your job:
1. Receive the user's query.
2. Process the query.
3. If you cannot fully process the query due to missing information, call the tool `get_more_info_from_user` to gather additional details.
4. Hand off the query to the Planning Agent.
""",
    model=llm_model,
    # model_settings=ModelSettings(temperature=0.3, max_tokens=500),
    tools=[get_more_info_from_user],
    handoffs=[
        handoff(
            agent=planning_agent,
        )
    ]
)