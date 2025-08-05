import logging
import os
from pathlib import Path

from google import genai
from .config import Config

logger = logging.getLogger(__name__)

# Cache API key to avoid repeated IO
_GEMINI_API_KEY: str | None = None
_CLIENT: genai.Client | None = None


def _read_key_file() -> str | None:
    """Read API key from ~/.api-gemini if present and non-empty."""
    try:
        key_path = Path.home() / ".api-gemini"
        key = key_path.read_text().strip()
        if not key:
            logger.error(f"API key file found at {key_path}, but it is empty.")
            return None
        return key
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.exception(f"Unexpected error while reading ~/.api-gemini: {e}")
        return None


def _get_api_key() -> str | None:
    """Resolve API key with env var precedence, then fallback to ~/.api-gemini."""
    global _GEMINI_API_KEY
    if _GEMINI_API_KEY is not None:
        return _GEMINI_API_KEY

    # Prefer environment variables
    env_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if env_key:
        _GEMINI_API_KEY = env_key.strip()
        return _GEMINI_API_KEY

    # Fallback to file
    file_key = _read_key_file()
    if file_key:
        _GEMINI_API_KEY = file_key
        return _GEMINI_API_KEY

    logger.error("No Gemini API key found in GEMINI_API_KEY/GOOGLE_API_KEY or ~/.api-gemini")
    return None


def _get_client() -> genai.Client | None:
    """Create or return a cached genai.Client."""
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT
    api_key = _get_api_key()
    if not api_key:
        return None
    try:
        _CLIENT = genai.Client(api_key=api_key)
        return _CLIENT
    except Exception as e:
        logger.exception(f"Failed to construct Google GenAI client: {e}")
        return None


async def generate_response(prompt: str, config: Config) -> str:
    """
    Generates a response from the configured Gemini model using google-genai Client.
    """
    client = _get_client()
    if client is None:
        return config.default_response

    try:
        # google-genai Client API
        resp = client.models.generate_content(
            model=config.gemini_model_name,
            contents=prompt,
        )

        # Try to use text property if available
        try:
            text = getattr(resp, "text", None)
        except Exception:
            text = None

        if text:
            return text

        # Defensive fallback if text not available; attempt to extract from candidates
        try:
            candidates = getattr(resp, "candidates", None) or []
            for c in candidates:
                parts = getattr(c, "content", None)
                if parts and hasattr(parts, "parts"):
                    for p in parts.parts:
                        if hasattr(p, "text") and p.text:
                            return p.text
        except Exception:
            pass

        logger.warning("GenAI response did not contain text; returning default response.")
        return config.default_response

    except Exception as e:
        # Broad catch to keep behavior stable across SDK changes
        logger.exception(f"Unexpected error from Google GenAI: {e}")
        return config.default_response