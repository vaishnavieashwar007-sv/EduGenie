import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load values from .env
load_dotenv()


@dataclass(frozen=True)
class Settings:
    # Gemini API configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

    # Gemini model
    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    # Explanation model
    explanation_model: str = os.getenv(
        "EXPLANATION_MODEL",
        "gemini-2.5-flash"
    )

    # Local explanation settings
    use_local_explanation: bool = (
        os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true"
    )

    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    # Generation settings
    max_output_tokens: int = int(
        os.getenv("MAX_OUTPUT_TOKENS", "2048")
    )

    temperature: float = float(
        os.getenv("TEMPERATURE", "0.3")
    )


# Create global settings object
settings = Settings()


def require_api_key() -> str:
    """
    Return Gemini API key.
    Raise an error if the key is missing.
    """

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add GEMINI_API_KEY to the .env file."
        )

    return settings.gemini_api_key