
import base64
from unittest.mock import patch

from mcp.server.fastmcp import FastMCP
from tools.file_tools import register_file_tools


def get_read_file_tool():
    mcp = FastMCP("Test Server")
    register_file_tools(mcp)

    return next(
        tool for tool in mcp._tool_manager.list_tools()
        if tool.name == "read_repository_file"
    )


def test_read_repository_file_success():
    tool = get_read_file_tool()
    encoded_content = base64.b64encode(
        b"Hello GitHub MCP Server"
    ).decode("utf-8")

    with patch(
        "tools.file_tools.github_get",
        return_value={
            "type": "file",
            "encoding": "base64",
            "content": encoded_content,
        },
    ):
        result = tool.fn("test-user", "test-repo", "README.md")

    assert result == "Hello GitHub MCP Server"


def test_read_repository_file_api_error():
    tool = get_read_file_tool()

    with patch(
        "tools.file_tools.github_get",
        return_value={"error": "GitHub resource not found."},
    ):
        result = tool.fn("test-user", "test-repo", "missing.txt")

    assert result == "GitHub resource not found."


def test_read_repository_file_directory():
    tool = get_read_file_tool()

    with patch(
        "tools.file_tools.github_get",
        return_value=[
            {"name": "README.md", "type": "file"}
        ],
    ):
        result = tool.fn("test-user", "test-repo", "docs")

    assert result == "The requested path is a directory, not a file."


def test_read_repository_file_unsupported_encoding():
    tool = get_read_file_tool()

    with patch(
        "tools.file_tools.github_get",
        return_value={
            "type": "file",
            "encoding": "utf-8",
            "content": "Hello",
        },
    ):
        result = tool.fn("test-user", "test-repo", "README.md")

    assert result == "Unsupported file encoding."


def test_read_repository_file_invalid_content():
    tool = get_read_file_tool()

    with patch(
        "tools.file_tools.github_get",
        return_value={
            "type": "file",
            "encoding": "base64",
        },
    ):
        result = tool.fn("test-user", "test-repo", "README.md")

    assert result == "Could not decode this file as UTF-8 text."


def test_read_repository_file_not_a_file():
    tool = get_read_file_tool()

    with patch(
        "tools.file_tools.github_get",
        return_value={"type": "dir"},
    ):
        result = tool.fn("test-user", "test-repo", "docs")

    assert result == "The requested path is not a file."
