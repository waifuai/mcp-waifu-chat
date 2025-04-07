<![CDATA[import logging
import os
from pathlib import Path
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions # For specific Google API errors

from .config import Config
# Removed unused import: from .utils import dialog_to_json

logger = logging.getLogger(__name__)

# Store the API key globally after reading it once to avoid repeated file access
_GEMINI_API_KEY = None

def _get_api_key() -> str | None:
    """Reads the Gemini API key from ~/.api-gemini."""
    global _GEMINI_API_KEY
    if _GEMINI_API_KEY is not None:
        return _GEMINI_API_KEY

    try:
        api_key_path = Path.home() / ".api-gemini"
        _GEMINI_API_KEY = api_key_path.read_text().strip()
        if not _GEMINI_API_KEY:
             logger.error(f"API key file found at {api_key_path}, but it is empty.")
             _GEMINI_API_KEY = None # Ensure it's None if empty
        return _GEMINI_API_KEY
    except FileNotFoundError:
        logger.error(f"Gemini API key file not found at ~/.api-gemini")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred while reading the API key: {e}")
        return None


async def generate_response(prompt: str, config: Config) -> str:
    """
    Generates a response from the configured Gemini model.

    Args:
        prompt: The prompt to send to the AI model.
        config: The application configuration containing the model name.

    Returns:
        The AI model's response, or a default error message if the model is unavailable
        or an error occurs.
    """
    api_key = _get_api_key()
    if not api_key:
        # Error already logged in _get_api_key
        return config.default_response

    try:
        # Configure the genai library (safe to call multiple times)
        genai.configure(api_key=api_key)

        # Initialize the model specified in the config
        model = genai.GenerativeModel(config.gemini_model_name)

        # Generate content (synchronous call, FastMCP should handle threading)
        # Consider adding safety settings if needed:
        # safety_settings = [
        #     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        #     # ... other categories
        # ]
        # response = model.generate_content(prompt, safety_settings=safety_settings)
        response = model.generate_content(prompt)

        # Check for blocked prompt or other generation issues
        if response.prompt_feedback.block_reason:
            logger.warning(
                f"Gemini prompt blocked for user. Reason: {response.prompt_feedback.block_reason}"
            )
            # Consider returning a more specific message or just the default
            return f"My safety filters blocked the prompt. Reason: {response.prompt_feedback.block_reason}"

        if not response.candidates or response.candidates[0].finish_reason != 'STOP':
             finish_reason = response.candidates[0].finish_reason if response.candidates else "UNKNOWN"
             logger.warning(
                 f"Gemini generation finished unexpectedly. Reason: {finish_reason}"
             )
             # Decide if this warrants the default response or returning partial text if available
             # return config.default_response # Option 1: Default response
             try:
                 # Option 2: Try to return text even if finish reason wasn't STOP
                 return response.text
             except ValueError: # Handle case where response.text is not available
                 logger.error("Could not extract text from Gemini response despite unexpected finish reason.")
                 return config.default_response


        # Successfully generated text
        return response.text

    except google_exceptions.PermissionDenied as e:
         logger.error(f"Gemini API permission denied. Check API key and model access: {e}")
         return config.default_response
    except google_exceptions.ResourceExhausted as e:
        logger.error(f"Gemini API quota exceeded: {e}")
        return "The AI model is currently overloaded. Please try again later."
    except google_exceptions.GoogleAPIError as e:
        # Catch other specific Google API errors
        logger.error(f"A Google API error occurred: {e}")
        return config.default_response
    except Exception as e:
        # Catch any other unexpected errors during the API call or processing
        logger.exception(f"An unexpected error occurred while contacting the Gemini model: {e}")
        return config.default_response
]]>