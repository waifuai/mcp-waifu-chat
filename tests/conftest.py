import os
import sqlite3

import pytest
from flask.testing import FlaskClient

from mcp_waifu_api.api import app  # Import your Flask app
from mcp_waifu_api.config import Config
from mcp_waifu_api.db import create_tables


# Override the database file for testing
TEST_DATABASE_FILE = "test_dialogs.db"

@pytest.fixture(scope="session")
def database():
    """Create a test database and tables."""
    # Ensure the test database file does not exist
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)

    config = Config(database_file=TEST_DATABASE_FILE)
    create_tables(config)  # Use the function to create tables

    yield config  # Provide the config

    # Teardown: Remove the test database file after the tests
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)


@pytest.fixture
def client(database):
    """Flask app test client fixture."""
    app.config = database
    # Use test config, importantly, the database file
    #app.config.from_object(database)
    app.config.testing = True
    with app.test_client() as client:
        yield client