import pytest
from aiagents.report_writer import report_writer_agent, format_report

def test_report_writer_agent_attributes():
    assert report_writer_agent.name == "ReportWriterAgent"
    assert isinstance(report_writer_agent.instructions, str)
    assert hasattr(report_writer_agent, "model")
    assert hasattr(report_writer_agent, "model_settings")
    assert report_writer_agent.model_settings.temperature == 0.3
    assert report_writer_agent.model_settings.max_tokens == 2000

def test_report_writer_agent_tools():
    assert isinstance(report_writer_agent.tools, list)
    assert len(report_writer_agent.tools) == 0

def test_format_report():
    sample = "This is a summary of findings."
    result = format_report(sample)
    assert result.startswith("# Research Report")