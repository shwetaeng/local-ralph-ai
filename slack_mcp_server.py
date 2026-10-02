# slack_mcp_server.py
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server named "SlackTools"
mcp = FastMCP("SlackTools")

# Mock database simulating Slack workspace messages
MOCK_SLACK_DB = [
    {
        "channel": "dev-team",
        "user": "alice",
        "text": "The database migration script is located at scripts/migrate.py. Run it with --env production."
    },
    {
        "channel": "dev-team",
        "user": "bob",
        "text": "Bug fix update: The auth token header key should be 'X-Auth-Token' instead of 'Authorization'."
    },
    {
        "channel": "general",
        "user": "charlie",
        "text": "Lunch order form is pinned in general."
    }
]

@mcp.tool()
def search_slack_messages(query: str) -> str:
    """Searches Slack channels for messages matching the given query string."""
    results = [
        f"[{msg['channel']}] {msg['user']}: {msg['text']}"
        for msg in MOCK_SLACK_DB
        if query.lower() in msg['text'].lower() or query.lower() in msg['channel'].lower()
    ]
    
    if not results:
        return f"No Slack messages found matching query: '{query}'"
    return "\n".join(results)

if __name__ == "__main__":
    mcp.run(transport='stdio')