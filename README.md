# Agentic Web Search Assistant

This project is a simple agent-based web search assistant. It uses the `Agent` framework to dynamically generate a user-specific persona and perform web searches using the Tavily API. The assistant can adapt its search behavior based on user input, like providing a summary or a more detailed response.

### Features

  - **Dynamic Persona**: The assistant's persona is dynamically generated from a `UserContext` which includes a user's name, city, and topic of interest.
  - **Web Search Capability**: The `web_search` function tool integrates the Tavily API to perform real-time web searches.
  - **Adaptive Behavior**: The agent is instructed to analyze user queries for keywords like "deeper" or "summarise" to adjust the number of search results and format the final response.
  - **Streamed Responses**: The assistant's responses are streamed for a more interactive user experience.
  - **Mock Data**: The project includes mock user data for easy testing. You can change the user by modifying the `user_index` variable in the script.


## Setup 

### Prerequisites

- Git
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer and virtual environment creator)

You will also need to obtain the following API keys:
- **Gemini API Key**: [Get your key here](https://aistudio.google.com/app/apikey)
- **Tavily API Key**: [Get your key here](https://tavily.com/)



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
    ```

### How to Run

1.  Make sure your virtual environment is active.
2.  Run the main script:
    ```bash
    uv run main.py
    ```

3.  Interact with the assistant by typing your queries. Type **`exit`** to end the session.
