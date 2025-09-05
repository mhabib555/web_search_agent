from aiagents.report_writer_agent import report_writer_agent, format_report

def test_report_writer_agent_attributes():
    """Verify ReportWriterAgent attributes and model settings are correctly set."""
    assert report_writer_agent.name == "ReportWriterAgent"
    assert isinstance(report_writer_agent.instructions, str)
    assert hasattr(report_writer_agent, "model")
    assert hasattr(report_writer_agent, "model_settings")
    assert report_writer_agent.model_settings.temperature == 0.3
    assert report_writer_agent.model_settings.max_tokens == 2000

def test_report_writer_agent_tools():
    """Check that ReportWriterAgent has an empty tools list."""
    assert isinstance(report_writer_agent.tools, list)
    assert len(report_writer_agent.tools) == 0

def test_format_report():
    """Test that format_report function formats input summary correctly."""
    sample = "This is a summary of findings."
    result = format_report(sample)
    assert result.startswith("# Research Report")
