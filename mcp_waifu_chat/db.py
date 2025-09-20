"""
Database layer for the MCP Waifu Chat Server.

This module handles all database operations using SQLite with connection pooling
and proper transaction management. It provides:

Database Operations:
- User management (create, check, delete, count, list)
- Dialog storage and retrieval (get, update, reset)
- Metadata tracking (timestamps, modification history)
- Pagination support for large user lists

Features:
- Connection pooling with context managers
- Automatic table creation and schema management
- Comprehensive error handling and logging
- Transaction rollback on failures
- Efficient query optimization
- Timestamp tracking for audit trails

The database schema includes a single 'dialogs' table that stores user conversations
with proper indexing for efficient lookups.
"""

import datetime
import logging
import sqlite3
import time
from contextlib import contextmanager
from typing import Generator

from .config import Config

# Configure logging
logger = logging.getLogger(__name__)


@contextmanager
def get_db_connection(db_file: str) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections with connection pooling."""
    conn = sqlite3.connect(db_file, timeout=10)  # Increased timeout
    conn.row_factory = sqlite3.Row  # Use Row factory for easier access
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"Database error: {e}")  # Log the specific error
        raise  # Re-raise after logging
    finally:
        conn.close()


def create_tables(config: Config) -> None:
    """Creates the necessary tables in the database."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dialogs (
                current_user TEXT NOT NULL,
                user_id TEXT NOT NULL,
                dialog TEXT,
                last_modified_datetime TEXT,
                last_modified_timestamp INTEGER,
                PRIMARY KEY (current_user, user_id)
            )
        """
        )


def get_old_dialog(current_user: str, user_id: str, config: Config) -> str:
    """Retrieves the previous dialog for a given user."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT dialog FROM dialogs WHERE current_user=? AND user_id=?",
            (current_user, user_id),
        )
        result = cursor.fetchone()
        return result["dialog"] if result else ""


def update_user_dialog(
    current_user: str, user_id: str, dialog: str, config: Config
) -> None:
    """Updates the dialog for a given user."""
    last_modified_datetime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    last_modified_timestamp = int(time.time())
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE dialogs SET dialog=?, last_modified_datetime=?, "
            "last_modified_timestamp=? WHERE current_user=? AND user_id=?",
            (
                dialog,
                last_modified_datetime,
                last_modified_timestamp,
                current_user,
                user_id,
            ),
        )


def reset_user_chat(current_user: str, user_id: str, config: Config) -> None:
    """Resets the dialog for a given user to an empty string."""
    update_user_dialog(current_user=current_user, user_id=user_id, dialog="", config=config)


def is_user_id_in_db(current_user: str, user_id: str, config: Config) -> bool:
    """Checks if a user ID exists in the database."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM dialogs WHERE current_user=? AND user_id=?",
            (current_user, user_id),
        )
        return cursor.fetchone() is not None


def add_user_to_db(current_user: str, user_id: str, config: Config) -> None:
    """Adds a new user to the database with an empty dialog."""
    last_modified_datetime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    last_modified_timestamp = int(time.time())
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO dialogs (current_user, user_id, dialog, "
            "last_modified_datetime, last_modified_timestamp) VALUES (?, ?, ?, ?, ?)",
            (current_user, user_id, "", last_modified_datetime, last_modified_timestamp),
        )


def delete_user_from_db(current_user: str, user_id: str, config: Config) -> None:
    """Deletes a user from the database."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM dialogs WHERE current_user=? AND user_id=?",
            (current_user, user_id),
        )


def get_user_count(current_user: str, config: Config) -> int:
    """Gets the total number of users for a given WaifuAPI user."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dialogs WHERE current_user=?", (current_user,))
        result = cursor.fetchone()
        return result[0] if result else 0


def get_all_users(current_user: str, config: Config) -> list[str]:
    """Gets a list of all user IDs for a given WaifuAPI user."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM dialogs WHERE current_user=?", (current_user,))
        return [row["user_id"] for row in cursor.fetchall()]


def get_all_users_paged(current_user: str, page: int, config: Config) -> list[str]:
    """Gets a page of user IDs, ordered by last modified timestamp."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM dialogs WHERE current_user=? "
            "ORDER BY last_modified_timestamp DESC LIMIT ?, 100",
            (current_user, page * 100),
        )
        return [row["user_id"] for row in cursor.fetchall()]


def get_user_dialog(current_user: str, user_id: str, config: Config) -> str:
    """Retrieves the dialog for a given user."""
    return get_old_dialog(
        current_user, user_id, config
    )  # Re-use the existing function


def get_user_last_modified_datetime(current_user: str, user_id: str, config: Config) -> str:
    """Retrieves the last modified datetime for a given user."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT last_modified_datetime FROM dialogs WHERE current_user=? AND user_id=?",
            (current_user, user_id),
        )
        result = cursor.fetchone()
        return result["last_modified_datetime"] if result else ""


def get_user_last_modified_timestamp(
    current_user: str, user_id: str, config: Config
) -> int:
    """Retrieves the last modified timestamp for a given user."""
    with get_db_connection(config.database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT last_modified_timestamp FROM dialogs WHERE current_user=? AND user_id=?",
            (current_user, user_id),
        )
        result = cursor.fetchone()
        return result["last_modified_timestamp"] if result else 0