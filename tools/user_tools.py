from mcp.server.fastmcp import FastMCP

from core.github_client import github_get


def register_user_tools(mcp: FastMCP):
    """Register GitHub user-related MCP tools."""

    @mcp.tool()
    def get_github_user() -> str:
        """Get the authenticated GitHub account's username."""

        user = github_get("user")

        if isinstance(user, dict) and "error" in user:
            return user["error"]

        if not isinstance(user, dict) or "login" not in user:
            return "Unexpected response from GitHub API."

        return (
            "Connected to GitHub successfully!\n"
            f"Username: {user['login']}"
        )
