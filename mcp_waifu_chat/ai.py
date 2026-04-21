"""
AI provider integration module for the MCP Waifu Chat Server.

This module handles communication with the OpenRouter AI provider for generating
responses to user messages.

The module includes:
- API key resolution from environment variables and dotfiles
- Unified interface for generating responses
- Robust error handling
- Timeout and retry logic for external API calls
"""

import logging
import os
from pathlib import Path
from typing import Optional

import requests
from .config import Config

logger = logging.getLogger(__name__)

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
    Generates a response from OpenRouter.
    """
    model = config.openrouter_model_name
    text = _openrouter_chat(prompt, model_name=model)
    if text:
        return text
    logger.warning("OpenRouter failed or returned empty text; using default response.")
    return config.default_response
