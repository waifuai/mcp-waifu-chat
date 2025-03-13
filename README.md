# MCP Waifu Chat Server

This project implements a basic MCP (Model Context Protocol) server for a conversational AI "waifu" character. It uses the `mcp` library for Python to handle the protocol details and `FastMCP` for easy server setup.

## Features

*   User management (create, check existence, delete, count)
*   Dialog history storage (get, set, reset)
*   Basic chat functionality (using a mocked AI response)
*   Modular design for easy extension
*   Configuration via environment variables
*   SQLite database for persistence
*   Comprehensive unit tests

## Requirements

*   Python 3.10+
*   `uv`

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd mcp-waifu-chat
    ```

2. Install uv (if not installed)
  With curl:
   ```bash
```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
  Or with powershell:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3.  Create and activate a virtual environment:

    ```bash
    uv venv
    source .venv/bin/activate  # On Linux/macOS
    .\.venv\Scripts\activate  # On Windows
    ```

4.  Install dependencies:

    ```bash
    uv sync --all-extras --dev
    ```

## Configuration

The server uses environment variables for configuration.  You can set these directly in your shell, or use a `.env` file.  An example `.env.example` file is provided:

```
DATABASE_FILE=dialogs.db
DEFAULT_RESPONSE="I'm sorry, I'm having trouble connecting to the AI model."
DEFAULT_GENRE="Fantasy"
FLASK_PORT=5000
```

*   `DATABASE_FILE`: Path to the SQLite database file (default: `dialogs.db`).
*   `DEFAULT_RESPONSE`:  The default response to send when the AI model is unavailable (default: "The AI model is currently unavailable. Please try again later.").
*   `DEFAULT_GENRE`: The default conversation genre (default: "Romance").
*   `FLASK_PORT`:  The port the server will listen on (default: 5000).

Copy `.env.example` to `.env` and customize the values as needed.

## Running the Server

To run the server, use:

```bash
uv run mcp-waifu-chat
```
This runs the `mcp_waifu_chat/api.py` file (since that's where the `FastMCP` instance is defined) and starts up the server.

## Running Tests

To run the unit tests:

```bash
uv run pytest
```

This will execute all tests in the `tests/` directory using `pytest`. The tests include database tests and API endpoint tests.

## API Endpoints

The server provides the following MCP-compliant endpoints (using `FastMCP`'s automatic routing):

### Server Status

*   `/v1/server/status` (GET):  Checks the server status.  Returns `{"status": "ok"}`.  This is a standard MCP endpoint.

### User Management Tools

These are implemented as MCP *tools*.

*   `create_user` (user_id: str): Creates a new user.
*   `check_user` (user_id: str): Checks if a user exists. Returns `{"user_id": str, "exists": bool}`.
*   `delete_user` (user_id: str): Deletes a user.
*  `user_count`: returns the number of users in the database for the current user.

### Dialog Management Tools

*    `reset_dialog` (user_id: str)

### Resources
* `/v1/user/dialog/json/{user_id}`: Dynamic resource to return dialogs as JSON.
* `/v1/user/dialog/str/{user_id}`: Dynamic resource to return dialogs as a string

### Chat Tool

* `chat` (message: str, user_id: str): Sends a chat message and gets a (mocked) response.

## Integrating with an LLM

The current `ai.generate_response` function is a placeholder.  To integrate with a real LLM, you would:

1.  **Choose an LLM API:**  Anthropic Claude, OpenAI, Google Gemini, or a self-hosted model.
2.  **Install the necessary client library:**  e.g., `pip install anthropic` or `pip install openai`.
3.  **Modify `ai.generate_response`:**
    *   Import the client library.
    *   Create a client instance (using your API key from the configuration).
    *   Construct the prompt using the `prompt` argument and any relevant context (like the dialog history, retrieved from the database).
    *   Send the request to the LLM API.
    *   Parse the response and return the generated text.
    *   Add error handling (retries, timeouts, etc.).
    *  Update the dependencies in `pyproject.toml`.

## Deploying to Production

For a production deployment, you should:

1.  **Use a production-ready WSGI server:**  Gunicorn is recommended and included in the `pyproject.toml`.  Example command:

    ```bash
    gunicorn --workers 4 --bind 0.0.0.0:8000 mcp_waifu_chat.api:app
    ```

    This runs the `app` object (our `FastMCP` instance) from `mcp_waifu_chat/api.py` using 4 worker processes, listening on port 8000.  Adjust the number of workers and the port as needed.

2.  **Use a robust database:**  Consider PostgreSQL or MySQL instead of SQLite for higher concurrency and scalability.

3.  **Implement proper logging:** Configure logging to write to files, a centralized logging service, or a monitoring system.

4.  **Secure your server:**  Use HTTPS, implement authentication/authorization, and follow security best practices for web applications.

5.  **Consider a reverse proxy:**  Use a reverse proxy like Nginx or Apache to handle TLS termination, load balancing, and static file serving.

6. **Containerize** Use Docker to simplify deployment.

## Project Structure Explanation

*   **`mcp_waifu_chat/` (Main Package):**
    *   `__init__.py`:  Makes the directory a Python package.
    *   `api.py`:  The core Flask application, route definitions, and request handling logic.  This is where `FastMCP` is used.
    *   `config.py`:  Handles loading and validating configuration settings from environment variables.
    *   `db.py`:  All database interaction logic (creating tables, querying, updating).
    *   `models.py`:  Pydantic models for request/response data validation and serialization.
    *   `utils.py`:  Helper functions, like `dialog_to_json` and `json_to_dialog`.
    *    `ai.py`:  This module is responsible for interacting with the AI model. Currently, it just has a mock function.
*   **`tests/` (Test Suite):**
    *   `conftest.py`:  pytest configuration, including fixtures for the test database and Flask test client.
    *   `test_db.py`:  Unit tests for the `db.py` module.
    *   `test_api.py`:  Unit tests for the API endpoints in `api.py`.
*  **`run.py`:**: Simple file to run the server

This structure promotes modularity, testability, and maintainability. Each module has a specific responsibility, making it easier to understand, modify, and extend the codebase.