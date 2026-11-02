
from unittest.mock import patch

from mcp.server.fastmcp import FastMCP
from tools.repository_tools import register_repository_tools


def get_registered_tools():
    mcp = FastMCP("Test Server")
    register_repository_tools(mcp)

    return {
        tool.name: tool
        for tool in mcp._tool_manager.list_tools()
    }


def test_list_my_repositories_success():
    tools = get_registered_tools()

    mock_repositories = [
        {
            "name": "project-one",
            "description": "AI project",
            "html_url": "https://github.com/test/project-one",
            "private": False,
        }
    ]

    with patch(
        "tools.repository_tools.github_get",
        return_value=mock_repositories,
    ):
        result = tools["list_my_repositories"].fn()

    assert "project-one" in result
    assert "AI project" in result


def test_list_my_repositories_api_error():
    tools = get_registered_tools()

    with patch(
        "tools.repository_tools.github_get",
        return_value={"error": "GitHub API failed."},
    ):
        result = tools["list_my_repositories"].fn()

    assert result == "GitHub API failed."


def test_list_my_repositories_empty():
    tools = get_registered_tools()

    with patch(
        "tools.repository_tools.github_get",
        return_value=[],
    ):
        result = tools["list_my_repositories"].fn()

    assert result == "No repositories were returned for this account."


def test_get_repository_contents_success():
    tools = get_registered_tools()

    mock_contents = [
        {
            "name": "README.md",
            "type": "file",
            "path": "README.md",
        }
    ]

    with patch(
        "tools.repository_tools.github_get",
        return_value=mock_contents,
    ):
        result = tools["get_repository_contents"].fn(
            "test-user", "test-repo"
        )

    assert "README.md" in result
    assert "file" in result


def test_get_repository_contents_api_error():
    tools = get_registered_tools()

    with patch(
        "tools.repository_tools.github_get",
        return_value={"error": "Repository not found."},
    ):
        result = tools["get_repository_contents"].fn(
            "test-user", "missing-repo"
        )

    assert result == "Repository not found."


def test_list_my_repositories_unexpected_response():
    tools = get_registered_tools()

    with patch(
        "tools.repository_tools.github_get",
        return_value={"message": "Unexpected response"},
    ):
        result = tools["list_my_repositories"].fn()

    assert result == "Unexpected response from GitHub API."


def test_get_repository_contents_single_file():
    tools = get_registered_tools()

    with patch(
        "tools.repository_tools.github_get",
        return_value={
            "name": "README.md",
            "type": "file",
            "path": "README.md",
        },
    ):
        result = tools["get_repository_contents"].fn(
            "test-user", "test-repo"
        )

    assert "README.md" in result
    assert "file" in result



def test_get_repository_contents_unexpected_response():
    tools = get_registered_tools()

    with patch(
        "tools.repository_tools.github_get",
        return_value="Unexpected data",
    ):
        result = tools["get_repository_contents"].fn(
            "test-user", "test-repo"
        )

    assert result == "Unexpected response from GitHub API."
