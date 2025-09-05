import asyncio
from aiagents.information_gathering_runner import run_information_gathering_agent
from aiagents.planning_agent_runner import run_planning_agent
from config.context import UserContext
from config.config import logger
from utils import initialize_sqlite_session, get_user_context, get_user_input, display_final_report, save_as_markdown
from config.constants import RESET, GREEN, BLUE, MAGENTA, YELLOW, RED

async def process_query_loop(user_context: UserContext, session):
    """Main loop to handle user queries and agent execution until information is complete."""
    default_query = "How did the adoption of server-side rendering with Laravel improve page load times of websites, concise?"
    
    while True:
        try:
            # Get initial user input
            user_input = get_user_input(default_query, prompt_type="initial")
            if user_input == 'exit':
                print(f"{YELLOW}Exiting query loop.{RESET}")
                break

            # Initialize or update the query with user input
            current_query = user_input

            # Loop until information gathering is complete
            while True:
                info_gathering_result = await run_information_gathering_agent(current_query, user_context, session)
                
                if info_gathering_result and info_gathering_result.is_information_complete:
                    print(f"{GREEN}Information gathering complete. Proceeding to planning phase.{RESET}")
                    final_report, last_agent = await run_planning_agent(info_gathering_result, user_context, session)
                    display_final_report(final_report, last_agent)
                    # Prompt for a new topic
                    user_input = get_user_input(prompt_type="new_topic_or_save")
                    if user_input == 'exit':
                        print(f"{YELLOW}Exiting query loop.{RESET}")
                        break
                    elif user_input == 'save':
                        filename = save_as_markdown(final_report)
                        print(f"{GREEN}Report saved as {filename}{RESET}")
                        user_input = get_user_input(prompt_type="new_topic")
                        if user_input == 'exit':
                            print(f"{YELLOW}Exiting query loop.{RESET}")
                            break
                    # Start a new query
                    current_query = user_input
                else:
                    print(f"{YELLOW}\nInformation gathering incomplete. Please provide additional details.{RESET}")
                    print(info_gathering_result.data)
                    additional_input = get_user_input(prompt_type="additional")
                    if additional_input == 'exit':
                        print(f"{YELLOW}Exiting query loop.{RESET}")
                        return  # Exit the entire loop
                    # Append or combine additional input to the current query
                    current_query = f"{current_query}\nAdditional details: {additional_input}"

        except KeyboardInterrupt:
            logger.info("User interrupted the process")
            print(f"{YELLOW}User interrupted the process{RESET}")
            break
        except Exception as e:
            logger.error(f"Error in query loop: {str(e)}")
            print(f"{RED}Error: {str(e)}{RESET}")
            continue


async def main():
    """Main entry point for the Deep Research System."""
    try:
        # Initialize SQLite session
        session = initialize_sqlite_session("deep_research")
        
        # Select user context
        user_index = 1
        user_context = get_user_context(user_index)
        
        # Run query processing loop
        await process_query_loop(user_context, session)
        
    except IndexError as ie:
        logger.error(f"User context error: {str(ie)}")
        print(f"{RED}Error: {str(ie)}{RESET}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}")
        print(f"{RED}Error: {str(e)}{RESET}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Error running asyncio: {str(e)}")
        print(f"{RED}Error: {str(e)}{RESET}")
        raise