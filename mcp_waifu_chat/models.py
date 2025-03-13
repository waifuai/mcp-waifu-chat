from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class User(BaseModel):
    """Represents a user."""

    user_id: str = Field(..., description="Unique identifier for the user.")


class UserExists(User):
    """Response model for checking if a user exists."""

    exists: bool = Field(
        ..., description="Indicates whether the user exists (True) or not (False)."
    )


class UserMetadata(User):
    """Response model for getting user metadata."""

    last_modified_datetime: str = Field(
        ..., description="Last modified datetime in ISO 8601 format."
    )
    last_modified_timestamp: int = Field(
        ..., description="Last modified timestamp in seconds since epoch."
    )


class DialogEntry(BaseModel):
    """Represents a single entry in a dialog."""

    index: int = Field(..., description="Index of the dialog entry.")
    name: str = Field(..., description="Name of the speaker (e.g., 'User', 'Waifu').")
    message: str = Field(..., description="The message content.")


class UserDialogJson(User):
    """Response model for getting or setting user dialog in JSON format."""

    dialog: list[DialogEntry] | None = Field(
        None, description="List of dialog entries, or null if no dialog is present."
    )  # Can be None

    @model_validator(mode="before")
    @classmethod
    def none_to_empty_list(cls, data: dict[str, Any]) -> dict[str, Any]:
        """
        sets dialog to [] if not set, also sets default status if not provided.
        """
        if "dialog" not in data:
            data["dialog"] = []
        return data


class UserDialogStr(User):
    """Response model for getting user dialog as a string."""

    dialog: str | None = Field(
        None,
        description="Dialog history as a concatenated string, or null if no dialog "
        "is present.",
    )  # Can be None


class UserCount(BaseModel):
    """Response model for getting the total number of users."""

    user_count: int | None = Field(
        None, description="The total number of users."
    )  # Can be None


class UserList(BaseModel):
    """Response model for getting a page of user IDs."""

    page: int = Field(..., description="The page number (0-indexed).")
    users: list[str] = Field(..., description="List of user IDs on the current page.")


class ServerStatus(BaseModel):
    """Response model for checking server status."""

    status: str = Field(..., description='Server status, should be "ok".')


class ChatRequest(BaseModel):
    """Request model for sending a chat message."""

    model_config = ConfigDict(extra="forbid")  # extra fields should be an error.

    user_id: str = Field(..., description="Unique identifier for the user.")
    message: str = Field(..., description="The chat message sent by the user.")
    username: str | None = Field(None, description="Optional username.")
    from_name: str | None = Field(
        None, description="Optional name of the sender. Defaults to empty string."
    )
    to_name: str | None = Field(
        "Waifu",
        description="Optional name of the recipient. Defaults to 'Waifu'.",
    )
    situation: str | None = Field(
        None,
        description="Optional situation/context for the conversation. Defaults to empty"
        " string.",
    )
    translate_from: str | None = Field(
        "auto",
        description="Source language code for translation (ISO 639-1). Defaults to 'auto'.",
    )
    translate_to: str | None = Field(
        "auto",
        description="Target language code for translation (ISO 639-1). Defaults to 'auto'.",
    )

class ChatResponse(BaseModel):
    """Response model for a chat message."""

    user_id: str = Field(..., description="Unique identifier for the user.")
    response: str = Field(..., description="The AI's response message.")

class ChatFormRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")  # extra fields should be an error.
    message: str = Field(..., description="The chat message to send.")
    user_id: str = Field(..., description="The ID of the user sending the message.")

class ModelUrl(BaseModel):
    model_config = ConfigDict(extra="forbid")
    input: str

class ModelUrlResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model_url_response: str