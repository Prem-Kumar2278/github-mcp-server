"""
Configuration template for VS Code MCP (~/.vscode/mcp.json or workspace .vscode/mcp.json).
"""

VSCODE_CONFIG = {
    "servers": {
        "github-python": {
            "command": "D:\\Python for AI\\github-mcp-server\\.venv\\Scripts\\python.exe",
            "args": [
                "D:\\Python for AI\\github-mcp-server\\server.py"
            ],
            "cwd": "D:\\Python for AI\\github-mcp-server"
        }
    }
}
