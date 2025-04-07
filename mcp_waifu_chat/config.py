import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Configuration for the Waifu Chat API."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", frozen=True, extra="ignore"
    )

    database_file: str = Field(
        default="dialogs.db", description="Path to the SQLite database file."
    )
    default_response: str = Field(
        default="The AI model is currently unavailable. Please try again later.",
        description="Default response message when the AI model is unavailable.",
    )
    default_genre: str = Field(
        default="Romance", description="Default genre for conversations."
    )
    flask_port: int = Field(
        default=5000, description="Port number on which the Flask app will run."
    gemini_model_name: str = Field(
        default="gemini-2.0-flash",
        description="The specific Gemini model to use (e.g., gemini-2.0-flash)."
    )
    )
    # Add model_url to config
    model_url: str = Field(default="http://example.com", description="ai model url")

    @classmethod
    def load(cls) -> "Config":
        """Loads the configuration from environment variables and/or a .env file."""
        return cls()