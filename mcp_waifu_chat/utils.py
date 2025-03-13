import re
from typing import Any, Optional


def get_current_user(headers: dict) -> str:
    """Extracts the 'current-user' from headers, providing a default if not found."""
    return headers.get("current-user", "0_no_current_user_specified")


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