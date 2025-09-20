"""
FastMCP server implementation for the MCP Waifu Chat Server.

This module defines the main FastMCP application and implements all the MCP tools
and resources for the waifu chat server. It handles:

- Server initialization and configuration
- User management tools (create, check, delete, count)
- Dialog management tools (get, set, reset)
- Chat functionality with AI provider integration
- Request context handling for multi-user support
- Database initialization and connection management

The server uses FastMCP for automatic MCP protocol compliance and provides
a clean, extensible API for waifu character interactions.
"""

import logging

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context
# Remove Request import as it's not needed for tools
# from starlette.requests import Request

from . import ai, config, db, models, utils
from .config import Config

# --- Configuration and Logging ---
app = FastMCP(name="WaifuAPI")  # Use FastMCP!
config = Config.load()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)  # Use __name__ for module-level logging


# --- Database Initialization ---
# Initialize database tables directly after loading config
db.create_tables(config)
app.config = config # Assign config to app *after* potential use in create_tables


# --- Helper Functions (remain largely the same, but now use config)---
# Simplify helper back to expecting request_context (which has meta.headers)
def _get_current_user(request_context) -> str:
    """Helper function to consistently get the current user from request context."""
    headers = getattr(request_context, 'meta', {}).get('headers', {})
    return headers.get("current-user", "0_no_current_user_specified")


# --- User Management (now using FastMCP decorators) ---
@app.tool()
async def create_user(user_id: str, context: Context) -> dict:
    """Creates a new user."""
    current_user = _get_current_user(context.request_context) # Pass request_context
    db.add_user_to_db(current_user, user_id, app.config)
    logger.info(f"Created user: {user_id} for current_user: {current_user}")
    return {"user_id": user_id}


@app.tool()
async def check_user(user_id: str, context: Context) -> dict:
    """Checks if a user exists."""
    current_user = _get_current_user(context.request_context) # Pass request_context
    exists = db.is_user_id_in_db(current_user, user_id, app.config)
    return {"user_id": user_id, "exists": exists}


@app.tool()
async def delete_user(user_id: str, context: Context) -> dict:
    """Deletes a user."""
    current_user = _get_current_user(context.request_context) # Pass request_context
    db.delete_user_from_db(current_user, user_id, app.config)
    logger.info(f"Deleted user: {user_id} for current_user: {current_user}")
    return {"user_id": user_id}


@app.tool()
async def user_count(context: Context) -> dict:
    """Gets the total number of users."""
    current_user = _get_current_user(context.request_context) # Pass request_context
    count = db.get_user_count(current_user, app.config)
    return {"user_count": count}


# --- Dialog Management (also using FastMCP decorators) ---
@app.tool()
async def reset_dialog(user_id: str, context: Context) -> dict:
    """Resets the user's dialog history."""
    current_user = _get_current_user(context.request_context) # Pass request_context
    db.reset_user_chat(current_user, user_id, app.config)
    logger.info(f"Reset dialog for user: {user_id} by current_user: {current_user}")
    return {"user_id": user_id}


# Change from resource to tool to access context/headers
@app.tool()
async def get_dialog_json(user_id: str, context: Context) -> dict: # Changed signature back
    """Gets the user's dialog history as a JSON object."""
    current_user = _get_current_user(context.request_context) # Use context
    dialog_str = db.get_user_dialog(current_user, user_id, app.config)
    dialog_list = utils.dialog_to_json(dialog_str)
    return {"user_id": user_id, "dialog": dialog_list}

# Change from resource to tool to access context/headers
@app.tool()
async def get_dialog_str(user_id: str, context: Context) -> dict: # Changed signature back
    """Gets the user's dialog history as a string."""
    current_user = _get_current_user(context.request_context) # Use context
    dialog_str = db.get_user_dialog(current_user, user_id, app.config)
    return {"user_id": user_id, "dialog": dialog_str}



@app.tool()
async def chat(message: str, user_id: str, context: Context) -> dict:
    """Handles chat message requests (using JSON data)."""
    current_user = _get_current_user(context.request_context) # Pass request_context

    # 1. Get old dialog
    old_dialog = db.get_old_dialog(current_user, user_id, app.config)

    # 2. Construct the prompt including the new message
    prompt_dialog = f'{old_dialog} User said: "{message}" Waifu said: "'

   # 3. Generate the AI response using the constructed prompt
    # Use the actual generate_response function and pass the correct prompt and config
    ai_response = await ai.generate_response(prompt_dialog, app.config)

    # 4. Construct the complete dialog string including the AI's response
    complete_dialog = f'{prompt_dialog}{ai_response}"'

   # 5. Update the database with the complete dialog
    db.update_user_dialog(current_user=current_user, user_id=user_id, dialog=complete_dialog, config=app.config)

   # 6. Return the AI's response
    return {"user_id": user_id, "response": ai_response}
    return {"user_id": user_id, "response": ai_response}