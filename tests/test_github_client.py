
from unittest.mock import Mock, patch
from core import github_client
import httpx
import pytest


def test_github_get_success():
    mock_response = Mock()
    mock_response.json.return_value = {"login": "test-user"}

    with patch.object(
        github_client,
        "get_github_headers",
        return_value={"Authorization": "Bearer test"},
    ), patch.object(
        github_client.httpx,
        "get",
        return_value=mock_response,
    ) as mock_get:

        result = github_client.github_get("user")

    assert result == {"login": "test-user"}
    mock_get.assert_called_once()


def test_github_get_missing_token():
    with patch.object(
        github_client,
        "get_github_headers",
        side_effect=ValueError("GITHUB_TOKEN is missing"),
    ):
        result = github_client.github_get("user")

    assert result == {"error": "GITHUB_TOKEN is missing"}


def test_github_get_connection_error():
    with patch.object(
        github_client,
        "get_github_headers",
        return_value={"Authorization": "Bearer test"},
    ), patch.object(
        github_client.httpx,
        "get",
        side_effect=github_client.httpx.RequestError("Connection failed"),
    ):
        result = github_client.github_get("user")

    assert result == {"error": "Could not connect to GitHub API."}


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (401, "GitHub authentication failed. Check your token."),
        (404, "GitHub resource not found."),
        (500, "GitHub API error: HTTP 500"),
    ],
)
def test_github_get_http_errors(status_code, expected):
    mock_response = Mock()
    mock_response.status_code = status_code

    error = httpx.HTTPStatusError(
        "HTTP error",
        request=Mock(),
        response=mock_response,
    )

    mock_response.raise_for_status.side_effect = error

    with patch.object(
        github_client,
        "get_github_headers",
        return_value={"Authorization": "Bearer test"},
    ), patch.object(
        github_client.httpx,
        "get",
        return_value=mock_response,
    ):
        result = github_client.github_get("user")

    assert result == {"error": expected}
