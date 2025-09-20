"""
Pytest configuration and fixtures for the MCP Waifu Chat Server tests.

This module provides shared fixtures and configuration for the test suite:

Fixtures:
- database: Creates and tears down test SQLite database for each test function
- client: Provides FastMCP test client with proper configuration

Configuration:
- Test database isolation with automatic cleanup
- Proper fixture scoping for test independence
- Environment setup for reproducible testing
- Test client configuration for API testing

These fixtures ensure that tests run in isolation with clean state and
proper teardown to prevent test interference.
"""

import os
import sqlite3

import pytest
from starlette.testclient import TestClient # Use Starlette's TestClient for FastMCP

from mcp_waifu_chat.api import app  # Import your FastMCP app
from mcp_waifu_chat.config import Config
from mcp_waifu_chat.db import create_tables


# Override the database file for testing
TEST_DATABASE_FILE = "test_dialogs.db"


@pytest.fixture(scope="function") # Change scope to function for test isolation
def database():
    """Create a test database and tables for each test function."""
    # Ensure the test database file does not exist before each test
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)

    # Create a new config instance pointing to the test DB
    config = Config(database_file=TEST_DATABASE_FILE)
    create_tables(config)  # Use the function to create tables

    yield config  # Provide the config to the test

    # Teardown: Remove the test database file after each test
    # Add a check in case the file wasn't created or was already removed
    if os.path.exists(TEST_DATABASE_FILE):
        # Attempt to close any potential lingering connections (though function scope should handle this)
        # This might not be strictly necessary but can help on some platforms/setups
        try:
            # We don't have the connection object here, so direct removal is the main cleanup
            pass
        finally:
             # Ensure removal even if closing fails (though closing isn't attempted here)
            try:
                os.remove(TEST_DATABASE_FILE)
            except PermissionError:
                 # Handle potential file locking issues if teardown happens too quickly
                 # or if a test didn't close its connection properly (less likely with function scope)
                 print(f"Warning: Could not remove test database {TEST_DATABASE_FILE} during teardown.")


@pytest.fixture
def client(database: Config): # Add type hint for clarity
    """FastMCP app test client fixture."""
    # Assign the function-scoped test config to the app instance for this test
    app.config = database
    # Remove setting testing=True on frozen config
    # Use Starlette's TestClient with the FastMCP ASGI app
    with TestClient(app.sse_app()) as client:
        yield client