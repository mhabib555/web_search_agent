from agents import ModelSettings, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from aiagents.report_writer_agent import report_writer_agent
from config.config import base_agent

synthesis_agent = base_agent.clone(
    name="SynthesisAgent",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
You are a Synthesis Agent. Combine the provided research findings into a coherent report and hand off to the Report Writer Agent.
- Receive research findings from the Lead Research Agent.
- Include key insights, themes, and trends.
- Highlight any conflicts.
- Mention source reliability where relevant (using the provided ratings).
- For every key claim, add citations like [1], [2] referring to the numbered sources list.
- At the end, include a 'References' section with the numbered sources and their ratings.
Structure the report clearly with headings.
After synthesizing, handoff the report to the Report Writer Agent to format the report.
""",
    model_settings=ModelSettings(temperature=0.3, max_tokens=1500),
    handoffs=[
        handoff(
            agent=report_writer_agent,
        )
    ]
)
