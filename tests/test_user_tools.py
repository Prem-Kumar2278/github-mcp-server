
from unittest.mock import patch

from mcp.server.fastmcp import FastMCP
from tools.user_tools import register_user_tools


def get_registered_tool():
    mcp = FastMCP("Test Server")
    register_user_tools(mcp)

    return next(
        tool for tool in mcp._tool_manager.list_tools()
        if tool.name == "get_github_user"
    )


def test_get_github_user_success():
    tool = get_registered_tool()

    with patch(
        "tools.user_tools.github_get",
        return_value={"login": "test-user"},
    ):
        result = tool.fn()

    assert "Connected to GitHub successfully!" in result
    assert "Username: test-user" in result


def test_get_github_user_api_error():
    tool = get_registered_tool()

    with patch(
        "tools.user_tools.github_get",
        return_value={"error": "GitHub authentication failed."},
    ):
        result = tool.fn()

    assert result == "GitHub authentication failed."


def test_get_github_user_unexpected_response():
    tool = get_registered_tool()

    with patch(
        "tools.user_tools.github_get",
        return_value={"name": "test-user"},
    ):
        result = tool.fn()

    assert result == "Unexpected response from GitHub API."
