# ralph_engine.py
import json
import os
import sys
import subprocess
import ollama

MODEL_NAME = "qwen2.5-coder:7b"

# Tool definition passed to local LLM matching MCP Slack tool schema
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_slack_messages",
            "description": "Searches Slack channels for relevant code specifications, instructions, or bug reports.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword or topic"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_local_file",
            "description": "Writes generated code or context to a local file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Relative file path"},
                    "content": {"type": "string", "description": "Text or code content to write"}
                },
                "required": ["filepath", "content"]
            }
        }
    }
]

def execute_slack_mcp(query: str) -> str:
    """Invokes the MCP server via subprocess using stdio JSON-RPC simulation."""
    # Direct execution of the Python function for simplicity in standalone CLI
    from slack_mcp_server import search_slack_messages
    return search_slack_messages(query)

def write_local_file(filepath: str, content: str) -> str:
    """Executes local disk file write tool."""
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
    return f"Successfully wrote file to {filepath}"

def run_tool(name: str, args: dict) -> str:
    """Routes function calls to local tool handlers."""
    if name == "search_slack_messages":
        return execute_slack_mcp(args.get("query", ""))
    elif name == "write_local_file":
        return write_local_file(args.get("filepath", ""), args.get("content", ""))
    return f"Unknown tool: {name}"

def run_ralph_loop(user_prompt: str, max_iterations: int = 5):
    """Core Ralph Execution Loop"""
    print(f"\n🚀 [Ralph Agent Started] Goal: {user_prompt}\n" + "="*60)
    
    messages = [
        {"role": "system", "content": "You are Ralph, an autonomous AI coding agent. You use available tools to query context (like Slack) and generate required local code files. Always complete tasks end-to-end."},
        {"role": "user", "content": user_prompt}
    ]

    for iteration in range(1, max_iterations + 1):
        print(f"\n🔄 --- Ralph Loop Iteration {iteration}/{max_iterations} ---")
        
        # Call Local LLM via Ollama API
        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS
        )
        
        response_message = response["message"]
        messages.append(response_message)

        # Check if model wants to call tools
        tool_calls = response_message.get("tool_calls")
        if tool_calls:
            for tool_call in tool_calls:
                func_name = tool_call["function"]["name"]
                func_args = tool_call["function"]["arguments"]
                
                print(f"🛠️  [Agent Tool Call]: {func_name}({func_args})")
                
                # Run the actual tool
                tool_output = run_tool(func_name, func_args)
                print(f"📥 [Tool Result]:\n{tool_output}")

                # Feed tool output back into the message context
                messages.append({
                    "role": "tool",
                    "content": tool_output
                })
        else:
            # No tool call means agent has completed its task
            print("\n✅ [Ralph Agent Task Finished]:")
            print(response_message["content"])
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Find details from Slack about database migration and generate a python script to run it."
    
    run_ralph_loop(query)