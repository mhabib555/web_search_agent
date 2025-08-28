from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, handoff
from report_writer import report_writer_agent
from dataclasses import dataclass
import os
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

synthesis_agent = Agent(
    name="SynthesisAgent",
    instructions="""
You are a Synthesis Agent. Combine the provided research findings into a coherent report.
- Include key insights, themes, and trends.
- Highlight any conflicts.
- Mention source reliability where relevant (using the provided ratings).
- For every key claim, add citations like [1], [2] referring to the numbered sources list.
- At the end, include a 'References' section with the numbered sources and their ratings.
Structure the report clearly with headings.
After synthesizing, hand off the report to the Report Writer Agent to format the report.
""",
    model=llm_model,
    # model_settings=ModelSettings(temperature=0.3, max_tokens=1500),
    handoffs=[
        handoff(
            agent=report_writer_agent,
            tool_name_override="ReportWriterAgent"
        )
    ]
)