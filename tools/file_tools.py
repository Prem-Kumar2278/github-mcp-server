import base64

from mcp.server.fastmcp import FastMCP

from core.github_client import github_get


def register_file_tools(mcp: FastMCP):
    """Register GitHub file-related MCP tools."""

    @mcp.tool()
    def read_repository_file(
        owner: str,
        repo: str,
        path: str,
    ) -> str:
        """Read a text file from a GitHub repository."""

        endpoint = f"repos/{owner}/{repo}/contents/{path}"

        data = github_get(endpoint)

        if not isinstance(data, dict):
            return "The requested path is a directory, not a file."

        if "error" in data:
            return data["error"]

        if data.get("type") != "file":
            return "The requested path is not a file."

        if data.get("encoding") != "base64":
            return "Unsupported file encoding."

        try:
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content[:20000]

        except (ValueError, UnicodeDecodeError, KeyError):
            return "Could not decode this file as UTF-8 text."
