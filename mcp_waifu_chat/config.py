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
    default_provider: str = Field(
        default="openrouter",
        description="Default provider to use: 'openrouter' or 'gemini'.",
    )
    gemini_model_name: str = Field(
        default="gemini-2.5-pro",
        description="The specific Gemini model to use (e.g., gemini-2.5-pro).",
    )
    openrouter_model_name: str = Field(
        default="deepseek/deepseek-chat-v3-0324:free",
        description="The specific OpenRouter model to use.",
    )

    # Add model_url to config (kept for compatibility)
    model_url: str = Field(default="http://example.com", description="ai model url")

    @classmethod
    def load(cls) -> "Config":
        """
        Loads the configuration from environment variables and/or a .env file,
        then applies dotfile-based overrides for model names and provider precedence.
        """
        cfg = cls()

        # Resolve provider: DEFAULT_PROVIDER env overrides; else keep default 'openrouter'
        env_provider = os.getenv("DEFAULT_PROVIDER")
        if env_provider:
            object.__setattr__(cfg, "default_provider", env_provider.strip())

        # Resolve model names with precedence:
        # OpenRouter: OPENROUTER_MODEL_NAME > ~/.model-openrouter > default
        openrouter_env = os.getenv("OPENROUTER_MODEL_NAME")
        if openrouter_env and openrouter_env.strip():
            object.__setattr__(cfg, "openrouter_model_name", openrouter_env.strip())
        else:
            or_file = _read_single_line_file(Path.home() / ".model-openrouter")
            if or_file:
                object.__setattr__(cfg, "openrouter_model_name", or_file)

        # Gemini: GEMINI_MODEL_NAME > ~/.model-gemini > default
        gem_env = os.getenv("GEMINI_MODEL_NAME")
        if gem_env and gem_env.strip():
            object.__setattr__(cfg, "gemini_model_name", gem_env.strip())
        else:
            gm_file = _read_single_line_file(Path.home() / ".model-gemini")
            if gm_file:
                object.__setattr__(cfg, "gemini_model_name", gm_file)

        return cfg