import logging
import httpx  # Use httpx for async requests
from json import JSONDecodeError # Import JSONDecodeError for specific exception handling
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
    headers = {'Content-Type': 'application/json'}
    json_data = {
"input": prompt}
    # Use an async client for the request
    async with httpx.AsyncClient(timeout=30.0) as client: # Increased timeout to 30
        try:
            response = await client.post(config.model_url, headers=headers, json=json_data)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Safely parse JSON and access the key
            try:
                response_data = response.json()
                if "model_url_response" in response_data:
                    return response_data["model_url_response"]
                else:
                    logger.error(f"AI model response missing 'model_url_response' key. Response: {response_data}")
                    return config.default_response
            except JSONDecodeError:
                logger.error(f"Failed to decode JSON response from AI model. Response text: {response.text}")
                return config.default_response

        except httpx.RequestError as e:
            # Handles connection errors, timeouts, etc.
            logger.error(f"Error connecting to AI model at {config.model_url}: {e}")
            return config.default_response
        except httpx.HTTPStatusError as e:
            # Handles non-2xx status codes
            logger.error(f"AI model returned an error status {e.response.status_code}: {e.response.text}")
            return config.default_response
        except Exception as e:
            # Catch any other unexpected errors during the request/processing
            logger.exception(f"An unexpected error occurred while contacting the AI model: {e}")
            return config.default_response
        return config.default_response