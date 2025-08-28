from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings
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

report_writer_agent = Agent(
    name="ReportWriterAgent",
    instructions="""
You are a Report Writer Agent. Format the provided synthesized report into a professional Markdown format with clear headings and structure.
Ensure the report is polished and concise.
""",
    model=llm_model,
    model_settings=ModelSettings(temperature=0.3, max_tokens=2000),
    tools=[]
)

def format_report(synthesized_report: str) -> str:
    """Fallback function to format the synthesized report into Markdown."""
    return f"# Research Report\n\n{synthesized_report}"