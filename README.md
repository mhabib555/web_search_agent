# Agentic Web Search Assistant

This project is a simple agent-based web search assistant. It uses the `Agent` framework to dynamically generate a user-specific persona and perform web searches using the Tavily API. The assistant can adapt its search behavior based on user input, like providing a summary or a more detailed response.

### Features

  - **Dynamic Persona**: The assistant's persona is dynamically generated based on a provided `UserContext` which includes a user's name, city, and topic of interest. This allows for a more personalized interaction.
  - **Web Search Capability**: The `web_search` function tool integrates the Tavily API to perform real-time web searches.
  - **Streamed Responses**: The assistant's responses are streamed, allowing for a more interactive user experience.
  - **Adaptive Behavior**: The agent is instructed to analyze user queries for keywords like "deeper" or "summarise" to adjust the number of search results and format the final response accordingly.

## Setup steps

### Requirements

Install git and uv if not installed

Before running the project, you need to have the following API keys:

  - **Gemini API Key**: For the language model.
  - **Tavily API Key**: For the web search functionality.

Store these keys in a `.env` file in the project's root directory:

```env
GEMINI_API_KEY="your_gemini_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

### How to Run

1.  Clone the repository:

    ```bash
    git clone https://github.com/mhabib555/websearch-agent
    cd websearch-agent
    ```

2. Install the necessary dependencies from pyproject.toml

    ```bash
    uv sync
    ```

2.  Ensure your `.env` file is configured with the required API keys.

3.  Run the main script from your terminal:

    ```bash
    python your_script_name.py
    ```

4.  Interact with the assistant by typing your queries. Type **`exit`** to end the session.