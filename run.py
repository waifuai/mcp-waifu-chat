"""
Simple entry point script for running the MCP Waifu Chat Server.

This script imports and runs the FastMCP application from the api module.
It's kept simple for easy deployment and direct execution of the server.

For production deployments, consider using a WSGI/ASGI server like Gunicorn
with the FastMCP app instance from mcp_waifu_chat.api:app
"""

from mcp_waifu_api.api import app

if __name__ == "__main__":
    app.run()