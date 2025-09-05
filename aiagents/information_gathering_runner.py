import json
import re
from agents import Runner, ItemHelpers
from aiagents.information_gathering_agent import information_gathering_agent
from config.context import UserContext, InformationGatheringAnswer
from config.config import logger
from config.constants import RESET, GREEN, RED, MAGENTA
from utils import RunAgentHooks

async def run_information_gathering_agent(
    query: str,
    user_context: UserContext,
    session
) -> InformationGatheringAnswer:
    """Run the Information Gathering Agent and process its response."""
    print(f"{GREEN}\nRunning Information Gathering Agent...{RESET}")
    response = Runner.run_streamed(
        starting_agent=information_gathering_agent,
        input=query,
        context=user_context,
        max_turns=12,
        hooks=RunAgentHooks(),
        session=session
    )

    info_gathering_result = None
    async for event in response.stream_events():
        if event.type == "run_item_stream_event":
            if event.item.type == "message_output_item":
                try:
                    output_text = ItemHelpers.text_message_output(event.item)
                    
                    # Strip Markdown code block markers and extra whitespace
                    cleaned_output = re.sub(r'```json\s*|\s*```', '', output_text).strip()

                    # Parse JSON string to InformationGatheringAnswer
                    info_gathering_result = InformationGatheringAnswer.model_validate_json(cleaned_output)                    
                except json.JSONDecodeError as e:
                    logger.error("Failed to parse JSON output: %s", str(e))
                    print(f"{RED}Failed to parse JSON output: {str(e)}{RESET}")
                except Exception as e:
                    logger.error("Failed to parse InformationGatheringAgent output: %s", str(e))
                    print(f"{RED}Failed to parse output: {str(e)}{RESET}")
            elif event.item.type == "tool_call_output_item":
                print(f"{MAGENTA}Tool output: {event.item.output}{RESET}")
    
    return info_gathering_result
