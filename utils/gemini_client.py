"""
utils/gemini_client.py
-----------------------
Thin, reusable wrapper around Google's Gemini API. All Gemini calls in the
application go through `GeminiClient.generate()` so retry logic, error
handling and model configuration live in exactly one place.
"""

import time
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL_NAME, GEMINI_TEMPERATURE, GEMINI_MAX_OUTPUT_TOKENS


class GeminiClientError(Exception):
    """Raised when the Gemini API cannot fulfil a request."""


class GeminiClient:
    """Wraps google-generativeai with sane defaults and retry behaviour."""

    _configured = False

    def __init__(self):
        if not GEMINI_API_KEY:
            raise GeminiClientError(
                "GEMINI_API_KEY is not set. Add it to your .env file or "
                "Streamlit secrets before using AI features."
            )
        if not GeminiClient._configured:
            genai.configure(api_key=GEMINI_API_KEY)
            GeminiClient._configured = True

        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    def generate(self, prompt: str, temperature: float = None, max_retries: int = 3) -> str:
        """Send a prompt to Gemini and return the plain text response."""
        temperature = GEMINI_TEMPERATURE if temperature is None else temperature
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": GEMINI_MAX_OUTPUT_TOKENS,
        }

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = self.model.generate_content(
                    prompt, generation_config=generation_config
                )
                text = getattr(response, "text", None)
                if not text:
                    raise GeminiClientError("Empty response received from Gemini.")
                return text.strip()
            except Exception as exc:  # noqa: BLE001 - external SDK can raise many types
                last_error = exc
                if attempt < max_retries:
                    time.sleep(1.5 * attempt)
                    continue
        raise GeminiClientError(f"Gemini API request failed after {max_retries} attempts: {last_error}")


_client_instance = None


def get_gemini_client() -> GeminiClient:
    """Return a lazily-instantiated singleton GeminiClient."""
    global _client_instance
    if _client_instance is None:
        _client_instance = GeminiClient()
    return _client_instance
