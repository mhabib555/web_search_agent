from agents import Runner, ItemHelpers
from config.context import UserContext, InformationGatheringAnswer
from config.constants import RESET, GREEN
from utils import RunAgentHooks
from aiagents.planning_agent import planning_agent


async def run_planning_agent(
    info_gathering_result: InformationGatheringAnswer,
    user_context: UserContext,
    session
) -> tuple[str, str]:
    """Run the Planning Agent and process its response."""
    print(f"{GREEN}\nInformation gathering complete. Running Planning Agent...{RESET}")
    planning_response = Runner.run_streamed(
        starting_agent=planning_agent,
        input=info_gathering_result.data,
        context=user_context,
        max_turns=12,
        hooks=RunAgentHooks(),
        session=session
    )

    final_report = ""
    last_agent = ""
    async for event in planning_response.stream_events():
        if event.type == "agent_updated_stream_event":
            last_agent = event.new_agent.name
            continue
        if event.type == "run_item_stream_event":
            if event.item.type == "message_output_item":
                final_report = ItemHelpers.text_message_output(event.item)
                # print(f"{BLUE}\n[{last_agent}] Response: {final_report}...{RESET}")
            elif event.item.type == "tool_call_output_item":
                pass
                # print(f"{MAGENTA}Tool output: {event.item.output}{RESET}")

    return final_report, last_agent
