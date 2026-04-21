"""
Configuration management for the MCP Waifu Chat Server.

This module provides a comprehensive configuration system using Pydantic BaseSettings
with support for multiple configuration sources and priority-based loading:

Configuration Sources (in order of priority):
1. Environment variables
2. .env file
3. Dotfiles in user home directory (~/.model-openrouter, ~/.api-openrouter)
4. Default values

Features:
- Type-safe configuration with Pydantic validation
- Environment variable and .env file support
- Dotfile-based API key and model name resolution
- Model name resolution with multiple precedence levels
- Frozen configuration to prevent runtime modifications
"""

import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _read_single_line_file(path: Path) -> str | None:
    try:
        if path.is_file():
            content = path.read_text(encoding="utf-8").strip()
            return content if content else None
    except Exception:
        return None
    return None


class Config(BaseSettings):
    """Configuration for the Waifu Chat API."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", frozen=True, extra="ignore"
    )

    # Core app settings
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
    )

    # Provider and model settings
    openrouter_model_name: str = Field(
        default="openrouter/free",
        description="The specific OpenRouter model to use.",
    )

    # Add model_url to config (kept for compatibility)
    model_url: str = Field(default="http://example.com", description="ai model url")

    @classmethod
    def load(cls) -> "Config":
        """
        Loads the configuration from environment variables and/or a .env file,
        then applies dotfile-based overrides for model names.
        """
        cfg = cls()

        # Resolve model names with precedence:
        # OPENROUTER_MODEL_NAME > ~/.model-openrouter > default
        openrouter_env = os.getenv("OPENROUTER_MODEL_NAME")
        if openrouter_env and openrouter_env.strip():
            object.__setattr__(cfg, "openrouter_model_name", openrouter_env.strip())
        else:
            or_file = _read_single_line_file(Path.home() / ".model-openrouter")
            if or_file:
                object.__setattr__(cfg, "openrouter_model_name", or_file)

        return cfg
