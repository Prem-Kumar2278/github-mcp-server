
import pytest

from core import config


def test_get_github_token(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")

    result = config.get_github_token()

    assert result == "test-token"


def test_get_github_headers_success(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")

    headers = config.get_github_headers()

    assert headers["Authorization"] == "Bearer test-token"
    assert headers["Accept"] == "application/vnd.github+json"
    assert headers["X-GitHub-Api-Version"] == "2022-11-28"


def test_get_github_headers_missing_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    with pytest.raises(ValueError, match="GITHUB_TOKEN is missing"):
        config.get_github_headers()
