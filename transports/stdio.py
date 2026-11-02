from mcp.server.fastmcp import FastMCP


def run_stdio(mcp: FastMCP):
    """Run the MCP server using STDIO transport."""
    mcp.run(transport="stdio")