from agents import Agent, ModelSettings
from config.config import llm_model

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