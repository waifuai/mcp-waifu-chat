import logging

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.context import Context

from . import ai, config, db, models, utils
from .config import Config

# --- Configuration and Logging ---
app = FastMCP(name="WaifuAPI")  # Use FastMCP!
config = Config.load()
app.config = config

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)  # Use __name__ for module-level logging


# --- Database Initialization ---
# We still need to create the tables.  FastMCP doesn't do this for us.
@app.on_startup
async def startup_event():
    db.create_tables(app.config)


# --- Helper Functions (remain largely the same, but now use config)---
def _get_current_user(request):
    """Helper function to consistently get the current user."""
    return request.headers.get("current-user", "0_no_current_user_specified")


# --- User Management (now using FastMCP decorators) ---
@app.tool()
async def create_user(user_id: str, context: Context) -> dict:
    """Creates a new user."""
    current_user = _get_current_user(context.request_context.meta.headers)
    db.add_user_to_db(current_user, user_id, app.config)
    logger.info(f"Created user: {user_id} for current_user: {current_user}")
    return {"user_id": user_id}


@app.tool()
async def check_user(user_id: str, context: Context) -> dict:
    """Checks if a user exists."""
    current_user = _get_current_user(context.request_context.meta.headers)
    exists = db.is_user_id_in_db(current_user, user_id, app.config)
    return {"user_id": user_id, "exists": exists}


@app.tool()
async def delete_user(user_id: str, context: Context) -> dict:
    """Deletes a user."""
    current_user = _get_current_user(context.request_context.meta.headers)
    db.delete_user_from_db(current_user, user_id, app.config)
    logger.info(f"Deleted user: {user_id} for current_user: {current_user}")
    return {"user_id": user_id}


@app.tool()
async def user_count(context: Context) -> dict:
    """Gets the total number of users."""
    current_user = _get_current_user(context.request_context.meta.headers)
    count = db.get_user_count(current_user, app.config)
    return {"user_count": count}


# --- Dialog Management (also using FastMCP decorators) ---
@app.tool()
async def reset_dialog(user_id: str, context: Context) -> dict:
    """Resets the user's dialog history."""
    current_user = _get_current_user(context.request_context.meta.headers)
    db.reset_user_chat(current_user, user_id, app.config)
    logger.info(f"Reset dialog for user: {user_id} by current_user: {current_user}")
    return {"user_id": user_id}


@app.resource(uri="dialog://json/{user_id}")
async def get_dialog_json(user_id: str, context: Context) -> dict:
    """Gets the user's dialog history as a JSON object."""
    current_user = _get_current_user(context.request_context.meta.headers)
    dialog_str = db.get_user_dialog(current_user, user_id, app.config)
    dialog_list = utils.dialog_to_json(dialog_str)
    return {"user_id": user_id, "dialog": dialog_list}

@app.resource(uri="dialog://str/{user_id}")
async def get_dialog_str(user_id: str, context: Context) -> dict:
    current_user = _get_current_user(context.request_context.meta.headers)
    dialog_str = db.get_user_dialog(current_user, user_id, app.config)
    return {"user_id": user_id, "dialog": dialog_str}



@app.tool()
async def chat(message: str, user_id: str, context: Context) -> dict:
    """Handles chat message requests (using JSON data)."""
    current_user = _get_current_user(context.request_context.meta.headers)

     # Get old dialog, append new message, generate response, update dialog
    old_dialog = db.get_old_dialog(current_user, user_id, app.config)

    # Add new input to the database
    dialog = f'{old_dialog} User said: "{message}" Waifu said: "'
    db.update_user_dialog(current_user=current_user, user_id=user_id, dialog=dialog, config=app.config)
    # TODO Use a real LLM
    response = await ai.mock_response("prompt")

    return {"user_id": user_id, "response": response}