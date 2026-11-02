# GitHub MCP Server

A custom Python-based GitHub Model Context Protocol (MCP) server that allows AI assistants to interact with GitHub through dedicated MCP tools.

Built with the official MCP Python SDK, FastMCP, and the GitHub REST API.

## Features

- Retrieve authenticated GitHub user information.
- List repositories accessible to the authenticated account.
- Browse files and directories inside GitHub repositories.
- Read text files from GitHub repositories.
- Connect AI clients through STDIO transport.
- Configuration templates for Antigravity, Claude, and VS Code.
- Automated tests using pytest.
- GitHub API error handling and environment-based authentication.

## Architecture

```text
github-mcp-server/
│
├── adapters/
│   ├── __init__.py
│   ├── antigravity.py
│   ├── claude_code.py
│   └── vscode.py
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── github_client.py
│
├── tools/
│   ├── __init__.py
│   ├── user_tools.py
│   ├── repository_tools.py
│   └── file_tools.py
│
├── transports/
│   ├── __init__.py
│   └── stdio.py
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_file_tools.py
│   ├── test_github_client.py
│   ├── test_repository_tools.py
│   └── test_user_tools.py
│
├── server.py
├── requirements.txt
├── .env
└── .gitignore
```

## Available MCP Tools

| Tool | Description |
|---|---|
| `get_github_user` | Retrieves the authenticated GitHub username. |
| `list_my_repositories` | Lists repositories accessible to the authenticated account. |
| `get_repository_contents` | Lists files and directories at a repository path. |
| `read_repository_file` | Reads text file content from a repository. |
| `hello_github` | Checks whether the MCP server is working. |

### Tool Parameters

**get_github_user**

No parameters required.

**list_my_repositories**

No parameters required. Requests up to 100 repositories.

**get_repository_contents**

- `owner`: GitHub username or organization.
- `repo`: Repository name.
- `path`: Optional directory path. Defaults to the repository root.

**read_repository_file**

- `owner`: GitHub username or organization.
- `repo`: Repository name.
- `path`: File path inside the repository.

Returns up to 20,000 characters of decoded UTF-8 text.

**hello_github**

No parameters required.

## Technology Stack

- Python 3.13+
- MCP Python SDK
- FastMCP
- GitHub REST API
- HTTPX
- python-dotenv
- pytest
- pytest-cov

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/github-mcp-server.git
cd github-mcp-server
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure GitHub authentication

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token_here
```

Use a GitHub token with the minimum repository permissions required for your use case. Private repository access requires appropriate permissions.

Never commit your `.env` file or expose your token.

## Running the MCP Server

Run the server using:

```bash
python server.py
```

The server uses STDIO transport and waits for messages from an MCP client.

It does not normally print startup messages to the console. This is expected behavior.

For normal MCP client usage, configure the client to launch `server.py` using your virtual environment's Python executable.

## AI Client Configuration

The `adapters/` directory contains configuration templates for different MCP clients.

These templates currently use local Windows paths. Update the paths to match your own project location and Python executable.

### Antigravity

Configuration file:

```text
~/.gemini/config/mcp_config.json
```

Use the configuration structure provided in `adapters/antigravity.py`.

### Claude

The `adapters/claude_code.py` file contains an MCP configuration template.

Check your Claude client's supported configuration format and update the paths before using it.

### VS Code

The `adapters/vscode.py` file contains a configuration template for VS Code MCP configuration.

Update the paths and place the configuration in the appropriate MCP configuration file.

## Running Tests

Run all tests:

```bash
python -m pytest -v
```

Run tests with coverage:

```bash
python -m pytest --cov=core --cov=tools --cov-report=term-missing -v
```

The current project test suite contains 26 tests. The measured `core` and `tools` modules previously achieved 100% statement coverage.

Coverage does not guarantee that every possible runtime scenario has been tested.

## Security Notes

- Store GitHub credentials in `.env`.
- Never commit API tokens or secrets.
- Keep `.env` excluded through `.gitignore`.
- Use the minimum GitHub token permissions necessary.
- Review configuration files before sharing them publicly.

## Current Limitations

- The current tools provide read-only GitHub operations.
- Repository listing requests up to 100 repositories per call.
- File reading is limited to 20,000 characters.
- Only UTF-8 text files with Base64 encoding are supported by the file-reading tool.
- Write operations such as creating or updating files, issues, and pull requests are not currently implemented.

## Future Improvements

- Search GitHub repositories.
- Create and manage GitHub issues.
- Create and update repository files.
- Create pull requests.
- Add additional repository management tools.
- Improve client configuration and portability.
- Expand integration testing.

## License

Choose and add a suitable open-source license before publishing this project.
