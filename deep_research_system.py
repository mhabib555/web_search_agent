import asyncio
import json
from agents import Runner, SQLiteSession, ItemHelpers
from aiagents.information_gathering_agent import information_gathering_agent
from config.context import UserContext
from config.fake_data import fake_users

session = SQLiteSession("deep_research")

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
            # user_input = "Pros and cons of AI for patient diagnosis in 2025"
            if user_input.lower() == 'exit':
                break
            else:
                # Step 1: Run Information Gathering Agent
                print("\nRunning Information Gathering Agent...")
                response = Runner.run_streamed(
                    starting_agent=information_gathering_agent,
                    input=user_input,
                    context=user_context,
                    max_turns=12,
                    session=session
                )
                
                final_report = ""
                last_agent = ""
                async for event in response.stream_events():
                    
                    if event.type == "agent_updated_stream_event":
                        last_agent = event.new_agent.name
                        continue
                    elif event.type == "run_item_stream_event":
                        if event.item.type == "message_output_item":
                            final_report = ItemHelpers.text_message_output(event.item)
                            print(f"\n\n[{last_agent}] Response: {final_report}...")

                        elif event.type == "tool_call_output_item":
                            try:
                                tool_output = json.loads(event.item.output)
                                print(f"Tool output: {tool_output}")
                            except json.JSONDecodeError:
                                print("Failed to parse tool output")
                
                if final_report and last_agent=="ReportWriterAgent":
                        print(f"\n\n\n================================")
                        print(f"\n=== {last_agent} Research Report ===\n")
                        print(final_report)
                        print("\n=== End of Report ===\n")
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())