"""
AI provider integration module for the MCP Waifu Chat Server.

This module handles communication with external AI providers, currently supporting:
- OpenRouter (default): HTTP-based chat completions API
- Google Gemini: Google GenAI SDK client with fallback support

The module includes:
- API key resolution from environment variables and dotfiles
- Caching mechanisms for clients and credentials
- Unified interface for generating responses
- Robust error handling and fallback mechanisms
- Timeout and retry logic for external API calls
"""

import logging
import os
from pathlib import Path
from typing import Optional

import requests
from google import genai
from .config import Config

logger = logging.getLogger(__name__)

# --- Gemini client cache ---
_GEMINI_API_KEY: Optional[str] = None
_CLIENT: Optional[genai.Client] = None

# --- OpenRouter constants ---
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
_OPENROUTER_API_KEY: Optional[str] = None


def _read_single_line_file(path: Path) -> Optional[str]:
    try:
        if path.is_file():
            content = path.read_text(encoding="utf-8").strip()
            return content if content else None
    except Exception:
        return None
    return None


# ---------------- Gemini helpers ----------------
def _read_gemini_key_file() -> Optional[str]:
    """Read API key from ~/.api-gemini if present and non-empty."""
    return _read_single_line_file(Path.home() / ".api-gemini")


def _get_gemini_api_key() -> Optional[str]:
    """Resolve Gemini API key with env var precedence, then fallback to ~/.api-gemini."""
    global _GEMINI_API_KEY
    if _GEMINI_API_KEY is not None:
        return _GEMINI_API_KEY

    env_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if env_key and env_key.strip():
        _GEMINI_API_KEY = env_key.strip()
        return _GEMINI_API_KEY

    file_key = _read_gemini_key_file()
    if file_key:
        _GEMINI_API_KEY = file_key
        return _GEMINI_API_KEY

    logger.error("No Gemini API key found in GEMINI_API_KEY/GOOGLE_API_KEY or ~/.api-gemini")
    return None


def _get_gemini_client() -> Optional[genai.Client]:
    """Create or return a cached genai.Client."""
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT
    api_key = _get_gemini_api_key()
    if not api_key:
        return None
    try:
        _CLIENT = genai.Client(api_key=api_key)
        return _CLIENT
    except Exception as e:
        logger.exception(f"Failed to construct Google GenAI client: {e}")
        return None


# ---------------- OpenRouter helpers ----------------
def _resolve_openrouter_api_key() -> Optional[str]:
    """OPENROUTER_API_KEY env takes precedence; then ~/.api-openrouter."""
    global _OPENROUTER_API_KEY
    if _OPENROUTER_API_KEY is not None:
        return _OPENROUTER_API_KEY
    env_key = os.getenv("OPENROUTER_API_KEY")
    if env_key and env_key.strip():
        _OPENROUTER_API_KEY = env_key.strip()
        return _OPENROUTER_API_KEY
    file_key = _read_single_line_file(Path.home() / ".api-openrouter")
    if file_key:
        _OPENROUTER_API_KEY = file_key
        return _OPENROUTER_API_KEY
    logger.error("No OpenRouter API key found in OPENROUTER_API_KEY or ~/.api-openrouter")
    return None


def _openrouter_chat(prompt: str, model_name: str, timeout: int = 60) -> Optional[str]:
    api_key = _resolve_openrouter_api_key()
    if not api_key:
        return None

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=timeout)
        if resp.status_code != 200:
            try:
                body = resp.text
            except Exception:
                body = "<unavailable>"
            logger.warning(f"OpenRouter non-200: {resp.status_code}: {body[:500]}")
            return None
        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            return None
        content = (choices[0].get("message", {}).get("content") or "").strip()
        return content or None
    except Exception as e:
        logger.exception(f"OpenRouter request failed: {e}")
        return None


# ---------------- Unified interface ----------------
async def generate_response(prompt: str, config: Config) -> str:
    """
    Generates a response from the selected provider.
    Providers:
      - openrouter: HTTP POST to OpenRouter Chat Completions API
      - gemini: google-genai client call
    """
    provider = (config.default_provider or "openrouter").lower().strip()

    if provider == "openrouter":
        model = config.openrouter_model_name
        text = _openrouter_chat(prompt, model_name=model)
        if text:
            return text
        logger.warning("OpenRouter failed or returned empty text; using default response.")
        return config.default_response

    # Fallback to Gemini
    client = _get_gemini_client()
    if client is None:
        return config.default_response

    try:
        resp = client.models.generate_content(
            model=config.gemini_model_name,
            contents=prompt,
        )
        try:
            text = getattr(resp, "text", None)
        except Exception:
            text = None

        if text:
            return text

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
        logger.exception(f"Unexpected error from Google GenAI: {e}")
        return config.default_response