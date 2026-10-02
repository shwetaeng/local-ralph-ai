# Local Ralph AI

Local Ralph AI is a small Python command-line agent that sends prompts to an Ollama model and handles its tool calls. Its tools search a built-in sample of Slack-like messages and write generated content to local files.

## Prerequisites

- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running
- The model `qwen2.5-coder:7b` available in Ollama

## Setup

From the repository root, create and activate a virtual environment, then install the two packages imported by the source:

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install ollama mcp
ollama pull qwen2.5-coder:7b
```

On Windows, activate the environment with `venv\Scripts\activate`.

## Configuration

There are no application environment variables or configuration files read by these scripts. The engine uses the model name `qwen2.5-coder:7b` and the Ollama Python client's defaults.

`slack_mcp_server.py` searches a fixed in-memory sample dataset; it does not connect to Slack or use Slack credentials. Searches match a case-insensitive substring in a message's text or channel name.

## Run

Run the agent from the repository root with a prompt:

```sh
python ralph_engine.py "Search the sample messages for the auth token header and write the result to auth_config.py"
```

If no prompt is provided, the engine uses its built-in example prompt. It allows up to five Ollama iterations and prints the tool calls and results. Files written by the `write_local_file` tool are created relative to the process's current working directory.

The MCP server can also be started directly over stdio:

```sh
python slack_mcp_server.py
```

The engine itself imports and calls the server's search function directly rather than launching it as a subprocess.
