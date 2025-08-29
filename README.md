# Deep Research System

A multi-agent AI system for in-depth research on complex topics, leveraging Gemini and Tavily APIs. The system uses a team of specialized agents that collaborate to process user queries, personalize research, break down questions, collect and evaluate information, detect conflicts, and generate a professional research report. Coordination is achieved through agent-as-tool and handoff patterns, with full tracing

## Features

- **Multi-Agent Workflow**: Specialized agents handle each step—user info assignment, query breakdown, research, source checking, conflict detection, synthesis, and report writing.
- **Agent Coordination**: Modular design using agent-as-tool and handoff patterns for traceable collaboration.
- **Personalization**: Research is tailored to a mock user’s name, city, and topic.
- **Adaptive Web Search**: Dynamically adjusts search depth based on query intent.
- **Tracing & Transparency**: All agent actions are tracked via the OpenAI SDK.
- **Modern Integrations**: Supports Gemini API for language tasks and Tavily API for real-time


## Setup 

### Prerequisites

- Git
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer and virtual environment creator)

You will also need to obtain the following API keys:
- **Gemini API Key**: [Get your key here](https://aistudio.google.com/app/apikey)
- **Tavily API Key**: [Get your key here](https://tavily.com/)
- **OpenAI API Key**: [Get your key here](https://platform.openai.com/api-keys)



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
   - Assign a mock user profile from `fake_data.py` (user_index=1)
   - Get user query (Information Gathering Agent).
   - Break down the query into sub-queries (Planning Agent).
   - Conduct research using the Lead Research Agent, which calls specialist agents (Research, Source Checker, Conflict Detector) as tools, evaluates sources, detects conflicts, synthesizes findings, and formats a report (Synthesis and Report Writer Agents).
   - Output progress messages and the final report, personalized to the mock user.


## Project Structure

```
web_search_agent/
│
├── deep_research_system.py        # Main script: orchestrates the workflow
│
├── aiagents/
│   ├── information_gathering_agent.py  # Assigns mock user info, hands off to Planning
│   ├── planning_agent.py               # Breaks down queries, hands off to Lead Research
│   ├── lead_researcher.py              # Coordinates specialist agents as tools
│   ├── research_agents.py              # Research, Source Checker, Conflict Detector
│   ├── synthesis_agent.py              # Synthesizes findings, hands off to Report Writer
│   └── report_writer.py                # Formats the final report
│
├── config/
│   ├── config.py                       # Loads API keys, initializes clients
│   ├── context.py                      # User context dataclasses
│   └── fake_data.py                    # Mock user data for personalization
│
├── .env                # API keys (not committed)
├── .env.copy           # Env template
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project metadata
└── .gitignore          # Git ignore
```

## Agent Coordination

1. **Information Gathering Agent**: Gather user query and process it.
2. **Planning Agent**: Breaks down the query into sub-queries and passes them to the Lead Research Agent.
3. **Lead Research Agent**: Orchestrates research by calling specialist agents (Research, Source Checker, Conflict Detector) as tools, then hands off to the Synthesis Agent.
4. **Specialist Agents**:  
   - **Research Agent**: Performs adaptive web searches.  
   - **Source Checker Agent**: Rates source reliability.  
   - **Conflict Detector Agent**: Finds contradictions.
5. **Synthesis Agent**: Combines findings and hands off to the Report Writer.
6. **Report Writer Agent**: Formats the final Markdown report.


## Tracing

- Enabled via OpenAI SDK with `OPENAI_API_KEY`.
- Tracks agent actions (e.g., user info assignment, sub-queries, sources, conflicts).

## Example Research Questions

- "Pros and cons of Agentic AI at work in 2025"
- "Future of renewable energy in urban areas"
- "Impact of AI on healthcare diagnostics"

## Notes

- Ensure valid API keys for Gemini, Tavily, and OpenAI.

## Contributing

Submit issues or pull requests to improve the system. Discuss major changes via issues first.

## License

MIT License