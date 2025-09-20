"""
Utility functions for the MCP Waifu Chat Server.

This module provides helper functions for data transformation and validation:

Key Functions:
- dialog_to_json(): Converts dialog strings to structured JSON format
- json_to_dialog(): Converts JSON dialog data back to string format

Features:
- Robust parsing of dialog strings with regex pattern matching
- Error handling for malformed data
- JSON serialization/deserialization
- Data validation and sanitization
- Support for empty and malformed input handling

These utilities are used throughout the application for converting between
different dialog data formats and ensuring data consistency.
"""

import re
from typing import Any, Optional


def dialog_to_json(dialog: str) -> list[dict[str, Any]]:
    """Converts a dialog string to a JSON object.

    Handles edge cases like empty strings and missing quotes robustly.

    Args:
        dialog (str): The dialog string.

    Returns:
        list[dict]: A JSON object representing the dialog.
    """
    if not dialog:  # Handle empty dialog string
        return []

    output = []
    # Find all occurrences of the pattern "Name said: "message""
    # This regex is slightly more robust to extra spaces.
    matches = re.findall(r"\s*([^:]+)\s+said:\s*\"([^\"]*)\"", dialog)

    for index, (name, message) in enumerate(matches):
        output.append({"index": index, "name": name.strip(), "message": message.strip()})
    return output


def json_to_dialog(json_obj: dict[str, Any]) -> str:
    """Converts a JSON object representing a dialog to a string.

    Handles potential errors and missing fields gracefully.

    Args:
        json_obj (dict): The JSON object representing the dialog.  Example:
            {"dialog": [{"index": 0, "name": "User", "message": "Hello"}]}


    Returns:
        str: The dialog string, or an empty string if there's an error.
    """
    try:
        dialog: Optional[list[dict[str, Any]]] = json_obj.get("dialog")
        if not dialog:
            return ""  # Handle missing or empty dialog

        dialog_strings = []
        for entry in dialog:
            name = entry.get("name")
            message = entry.get("message")
            if name is not None and message is not None:  # Both must be present
                dialog_strings.append(f'{name} said: "{message}"')

        return " ".join(dialog_strings)
    except (KeyError, TypeError, AttributeError) as e:
        # Handle cases where json_obj is malformed
        return ""