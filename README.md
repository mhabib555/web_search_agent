# Deep Research System

This project is a multi-agent research system designed to conduct in-depth research on complex topics using the Gemini API and Tavily API. Built with `openai-agents>=0.2.4`, it employs a team of specialized AI agents that collaborate to process user queries, assign mock user profiles from `fake_data.py`, break down questions, collect data, evaluate sources, detect conflicts, and produce a professional research report. The system uses **agent-as-tool** and **handoff** patterns for coordination, with OpenAI SDK tracing for monitoring.

## Features

- **Multi-Agent Architecture**:
  - **Information Gathering Agent** (`information_gathering_agent.py`): Processes the user query and assigns a random mock user profile from `fake_data.py` (e.g., {"name": "Aisha Khan", "city": "Karachi", "topic": "Python Programming"}). Handles `None` values with defaults: `city="Unknown"`, `topic="General"`. Hands off to the Planning Agent.
  - **Planning Agent** (`planning_agent.py`): Breaks down queries into 3–5 sub-queries and hands off to the Lead Research Agent.
  - **Lead Research Agent** (`lead_researcher.py`): Orchestrates research by running as an agent, calling specialist agents (Research, Source Checker, Conflict Detector) as tools with defined `tool_name` and `tool_description`, and handing off to the Synthesis Agent.
  - **Research Agent** (`research_agents.py`): Gathers information using the Tavily API, adapting search depth.
  - **Source Checker Agent** (`research_agents.py`): Rates source reliability (High, Medium, Low).
  - **Conflict Detector Agent** (`research_agents.py`): Identifies contradictions in findings.
  - **Synthesis Agent** (`synthesis_agent.py`): Combines findings into a report and hands off to the Report Writer.
  - **Report Writer Agent** (`report_writer.py`): Formats the report in Markdown.
- **Agent Coordination**:
  - **Agent-as-Tool**: Lead Research Agent calls Research, Source Checker, and Conflict Detector agents via `Runner.run_streamed` with specified `tool_name` and `tool_description`.
  - **Handoff**: Used for Information Gathering → Planning → Lead Research, and Synthesis → Report Writer.
- **User Personalization**: Uses `UserContext` to tailor research to a mock user’s name, city, and topic from `fake_data.py`.
- **Agent Cloning**: Research, Source Checker, and Conflict Detector agents are cloned from a base agent.
- **Tracing**: Enabled via OpenAI SDK with `OPENAI_API_KEY`, tracking agent actions.
- **Adaptive Web Search**: Adjusts search depth (1–3 results for summaries, 7–10 for in-depth, 5 default) based on query intent.
- **Gemini API Integration**: Uses `gemini-2.5-flash` for language model tasks.
- **Tavily API Integration**: Performs real-time web searches via `tavily-python>=0.7.10`.


## Setup 

### Prerequisites

- Git
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer and virtual environment creator)

You will also need to obtain the following API keys:
- **Gemini API Key**: [Get your key here](https://aistudio.google.com/app/apikey)
- **Tavily API Key**: [Get your key here](https://tavily.com/)
- **OpenAI API Key**: Required for tracing



### Installation Steps

1.  Clone the repository:
    ```bash
    git clone https://github.com/mhabib555/web_search_agent
    cd web_search_agent
    ```

2. Install dependencies and create a virtual environment using `uv`:
    ```bash
    uv sync
    source .venv/bin/activate
    ```

3.  Configure your API keys. Rename `.env.copy` to `.env` and add your keys:
    ```env
    GEMINI_API_KEY="your_gemini_api_key"
    TAVILY_API_KEY="your_tavily_api_key"
    OPENAI_API_KEY=your_openai_api_key
    ```

*Note*: Ensure `fake_data.py` (containing `fake_users`) is in the project directory with the provided structure.


### How to Run

1. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Run the main script:
   ```bash
   uv run deep_research_system.py
   ```

3. Interact with the system:
   - Enter a research query (e.g., "Pros and cons of Agentic AI at work in 2025").
   - Type `exit` to quit.

### Example Usage

1. Run the script:
   ```bash
   uv run deep_research_system.py
   ```

2. Enter a query:
   ```
   Pros and cons of Agentic AI at work in 2025
   ```

3. The system will:
   - Assign a random mock user profile from `fake_data.py` (e.g., Aisha Khan from Karachi, interested in Python Programming) with defaults for `None` values (Information Gathering Agent).
   - Break down the query into sub-queries (Planning Agent).
   - Conduct research using the Lead Research Agent, which calls specialist agents (Research, Source Checker, Conflict Detector) as tools, evaluates sources, detects conflicts, synthesizes findings, and formats a report (Synthesis and Report Writer Agents).
   - Output progress messages and the final report, personalized to the mock user.

## Project Structure

- `deep_research_system.py`: Main script that orchestrates the workflow and invokes the Lead Research Agent.
- `lead_researcher.py`: Defines the Lead Research Agent, which coordinates specialist agents with `as_tool()` calls including `tool_name` and `tool_description`.
- `information_gathering_agent.py`: Assigns mock user info from `fake_data.py` and hands off to Planning Agent.
- `planning_agent.py`: Breaks down queries and hands off to Lead Research Agent.
- `research_agents.py`: Contains Research, Source Checker, and Conflict Detector agents.
- `synthesis_agent.py`: Synthesizes findings and hands off to Report Writer.
- `report_writer.py`: Formats the final report.
- `fake_data.py`: Mock user data for personalization (e.g., Aisha Khan, Karachi, Python Programming).
- `.env`: Stores API keys.
- `requirements.txt`: Lists dependencies (`openai-agents>=0.2.4`, `tavily-python>=0.7.10`).
- `pyproject.toml`: Project metadata and dependencies.

## Agent Coordination

1. **Information Gathering Agent**: Assigns a random mock user profile from `fake_data.py`, handling `None` values, and hands off to Planning Agent.
2. **Planning Agent**: Generates 3–5 sub-queries and hands off to Lead Research Agent.
3. **Lead Research Agent**: Runs as an agent, calling Research, Source Checker, and Conflict Detector agents as tools via `Runner.run_streamed` with defined `tool_name` and `tool_description`, and hands off to Synthesis Agent.
4. **Research Agent**: Performs web searches with adaptive depth.
5. **Source Checker Agent**: Rates source reliability.
6. **Conflict Detector Agent**: Identifies contradictions.
7. **Synthesis Agent**: Combines findings and hands off to Report Writer.
8. **Report Writer Agent**: Formats the report in Markdown.

## Tracing

- Enabled via OpenAI SDK with `OPENAI_API_KEY`.
- Tracks agent actions (e.g., user info assignment, sub-queries, sources, conflicts).

## Example Research Questions

- "Pros and cons of Agentic AI at work in 2025"
- "Future of renewable energy in urban areas"
- "Impact of AI on healthcare diagnostics"

## Notes

- Ensure valid API keys for Gemini, Tavily, and OpenAI.
- `fake_data.py` must be included with the provided `fake_users` structure.
- Extend `report_writer.py` for other output formats (e.g., HTML, PDF) if needed.

## Contributing

Submit issues or pull requests to improve the system. Discuss major changes via issues first.

## License

MIT License