import httpx

from core.config import (
    GITHUB_API_BASE_URL,
    get_github_headers,
)


def github_get(
    endpoint: str,
    params: dict | None = None,
):
    """Send a GET request to the GitHub API."""

    url = f"{GITHUB_API_BASE_URL}/{endpoint.lstrip('/')}"

    try:
        response = httpx.get(
            url,
            headers=get_github_headers(),
            params=params,
            timeout=20.0,
        )

        response.raise_for_status()

        return response.json()

    except ValueError as exc:
        return {"error": str(exc)}

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 401:
            return {"error": "GitHub authentication failed. Check your token."}

        if exc.response.status_code == 404:
            return {"error": "GitHub resource not found."}

        return {
            "error": f"GitHub API error: HTTP {exc.response.status_code}"
        }

    except httpx.RequestError:
        return {"error": "Could not connect to GitHub API."}
