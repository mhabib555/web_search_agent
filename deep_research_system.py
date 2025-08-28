import os
import asyncio
import json
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, RunContextWrapper, ItemHelpers, set_tracing_disabled
from information_gathering_agent import information_gathering_agent
from context import UserContext
from dataclasses import dataclass
from fake_data import fake_users

# Enable OpenAI SDK tracing
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
set_tracing_disabled(disabled=False)

# Load environment variables
load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not gemini_api_key or not tavily_api_key or not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Missing required API keys")

async def main():
    
    user_index = 1
    user_context = UserContext(
        name=fake_users[user_index]['name'], 
        city=fake_users[user_index]['city'], 
        topic=fake_users[user_index]['topic'],
        subscription=fake_users[user_index]['subscription']
    )
    
    
    while True:
        try:
            user_input = input("Enter your research query (type 'exit' to quit): ").strip()
            # user_input = "Pros and cons of AI"
            if user_input.lower() == 'exit':
                break
            else:
                # Step 1: Run Information Gathering Agent
                print("Running Information Gathering Agent...")
                response = Runner.run_streamed(
                    starting_agent=information_gathering_agent,
                    input=user_input,
                    context=user_context
                )
                
                final_report = ""
                async for event in response.stream_events():
                    if event.type == "run_item_stream_event":
                        if event.item.type == "message_output_item":
                            final_report = ItemHelpers.text_message_output(event.item)
                            print(f"Final report generated: {final_report[:100]}...")
                        elif event.type == "tool_call_output_item":
                            try:
                                tool_output = json.loads(event.item.output)
                                print(f"Tool output: {tool_output}")
                            except json.JSONDecodeError:
                                print("Failed to parse tool output")
                
                if final_report:
                    print("\n=== Research Report ===\n")
                    print(final_report)
                    print("\n=== End of Report ===\n")
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())