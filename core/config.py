from pathlib import Path
import os
from dotenv import load_dotenv

# Ensure .env is always loaded from the project root regardless of working directory
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_API_VERSION = "2022-11-28"


def get_github_token() -> str | None:
    """Return the GitHub token from environment variables."""
    return os.getenv("GITHUB_TOKEN")


def get_github_headers() -> dict:
    """Return common headers for GitHub API requests."""
    token = get_github_token()

    if not token:
        raise ValueError("GITHUB_TOKEN is missing from the .env file.")

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }
