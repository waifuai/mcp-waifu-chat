import logging
import requests  # Import the requests library
from .config import Config # import config
from .utils import dialog_to_json

logger = logging.getLogger(__name__)

# Mock return value, and function to connect to the AI model
async def mock_response(prompt: str) -> str:
    return "The AI model is currently unavailable. Please try again later."


async def generate_response(prompt: str, config: Config) -> str:
    """
    Generates a response from the AI model.

    Args:
        prompt: The prompt to send to the AI model.
        config: The application configuration.

    Returns:
        The AI model's response, or a default error message if the model is unavailable.
    """
    try:
        headers = {
            'Content-Type': 'application/json',
        }
        json_data = {
            "input": prompt,
        }
        response = requests.post(config.model_url, headers=headers, json=json_data, timeout=30)  # Increased timeout to 30
        response.raise_for_status()
        return response.json()["model_url_response"]

    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to AI model: {e}")
        return config.default_response