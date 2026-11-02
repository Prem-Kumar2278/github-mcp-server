from mcp.server.fastmcp import FastMCP

from core.github_client import github_get


def register_repository_tools(mcp: FastMCP):
    """Register GitHub repository-related MCP tools."""

    @mcp.tool()
    def list_my_repositories() -> str:
        """List repositories accessible to the authenticated GitHub account."""

        repositories = github_get(
            "user/repos",
            params={
                "visibility": "all",
                "affiliation": "owner,collaborator,organization_member",
                "per_page": 100,
                "sort": "updated",
            },
        )

        if isinstance(repositories, dict) and "error" in repositories:
            return repositories["error"]

        if isinstance(repositories, dict):
            return "Unexpected response from GitHub API."

        if not isinstance(repositories, list) or not repositories:
            return "No repositories were returned for this account."

        results = []

        for repo in repositories:
            description = repo.get("description") or "No description"

            results.append(
                f"Name: {repo.get('name', 'Unknown')}\n"
                f"Description: {description}\n"
                f"URL: {repo.get('html_url', 'N/A')}\n"
                f"Private: {repo.get('private', False)}"
            )

        return "\n\n".join(results)

    @mcp.tool()
    def get_repository_contents(
        owner: str,
        repo: str,
        path: str = "",
    ) -> str:
        """List files and folders at a path inside a GitHub repository."""

        endpoint = f"repos/{owner}/{repo}/contents/{path}"

        contents = github_get(endpoint)

        if isinstance(contents, dict) and "error" in contents:
            return contents["error"]

        if isinstance(contents, dict):
            contents = [contents]

        if not isinstance(contents, list):
            return "Unexpected response from GitHub API."

        results = []

        for item in contents:
            results.append(
                f"Name: {item.get('name', 'Unknown')}\n"
                f"Type: {item.get('type', 'Unknown')}\n"
                f"Path: {item.get('path', 'Unknown')}"
            )

        return "\n\n".join(results) or "This directory is empty."
