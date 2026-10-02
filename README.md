# Local Ralph AI Agent with Slack MCP

A small Python command-line agent that uses Ollama to choose between two tools: searching a local, in-memory set of sample Slack messages and writing a file in the current working directory. Despite the server's name, the sample implementation does not connect to a real Slack workspace.

## How it works

- `ralph_engine.py` sends the prompt, conversation history, and tool definitions to the local Ollama model `qwen2.5-coder:7b`.
- When the model requests a tool, the engine searches the sample messages by substring or writes the requested file. It repeats this for up to five iterations, unless the model returns a response without a tool call first.
- `slack_mcp_server.py` defines the same sample-message search as a FastMCP tool and can be run as an MCP server over stdio. The engine itself imports and calls the search function directly; it does not connect to the stdio MCP server.

The sample messages are defined in `slack_mcp_server.py`. Searches match the query, case-insensitively, against message text and channel names.

## Prerequisites

- Python 3.10 or later
- [Ollama](https://ollama.com/) installed and running locally
- The `qwen2.5-coder:7b` model downloaded in Ollama

## Setup

From the project directory, create and activate a virtual environment, then install the Python packages used by the two scripts:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install ollama mcp
```

On Windows, activate the environment with:

```powershell
venv\Scripts\activate
```

Start Ollama in another terminal if it is not already running, and download the model:

```bash
ollama serve
ollama pull qwen2.5-coder:7b
```

There are no project-specific environment variables or Slack credentials to configure. The model name is set in `ralph_engine.py` as `MODEL_NAME`.

## Run

Run the agent with a prompt:

```bash
python ralph_engine.py "Find the auth token header guidance and save it to auth_config.py"
```

The prompt is optional. Without one, the engine uses its built-in request about the sample database-migration message:

```bash
python ralph_engine.py
```

The `write_local_file` tool creates parent directories as needed and writes to the path supplied by the model, relative to the current working directory when a relative path is used. Review generated files before using them.

To run the FastMCP server directly over stdio instead:

```bash
python slack_mcp_server.py
```

This starts the server for an MCP client; it is separate from the `ralph_engine.py` execution path described above.
