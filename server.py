from mcp.server.fastmcp import FastMCP

from tools.user_tools import register_user_tools
from tools.repository_tools import register_repository_tools
from tools.file_tools import register_file_tools
from transports.stdio import run_stdio

mcp = FastMCP("GitHub Assistant")


def register_all_tools():
    """Register all GitHub MCP tools."""
    register_user_tools(mcp)
    register_repository_tools(mcp)
    register_file_tools(mcp)


register_all_tools()


@mcp.tool()
def hello_github() -> str:
    """Check whether the GitHub MCP server is working."""
    return "Hello! Your GitHub MCP server is working."


if __name__ == "__main__":
    run_stdio(mcp)
