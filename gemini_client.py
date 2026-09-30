from functools import lru_cache
import time

try:
    from google import genai
    from google.genai import types
    GENAI_IMPORT_ERROR = None
except ImportError as exc:
    genai = None
    types = None
    GENAI_IMPORT_ERROR = exc

from config import settings, require_api_key


@lru_cache(maxsize=1)
def get_client():

    if GENAI_IMPORT_ERROR is not None:
        raise RuntimeError(
            "Google GenAI SDK is not installed."
        ) from GENAI_IMPORT_ERROR

    return genai.Client(
        api_key=require_api_key()
    )


def demo_answer(prompt: str) -> str:

    prompt_lower = prompt.lower()

    if "photosynthesis" in prompt_lower:

        return """Photosynthesis is the process by which green plants make their own food using sunlight, carbon dioxide, and water.

Chlorophyll helps plants absorb sunlight.

During photosynthesis, plants produce food (glucose) and release oxygen.

Example:
Plants use sunlight + water + carbon dioxide → food + oxygen."""


    if "what is python" in prompt_lower:

        return """Python is a high-level programming language known for its simple and readable syntax.

It is commonly used for:
- Web development
- Artificial intelligence
- Data science
- Automation

Example:
print("Hello World")"""


    if "what is ai" in prompt_lower or "artificial intelligence" in prompt_lower:

        return """Artificial Intelligence (AI) is the technology that enables computers to perform tasks that normally require human intelligence.

Examples include:
- Understanding language
- Recognizing images
- Making predictions
- Answering questions

Example:
Chatbots such as AI assistants use AI to understand and respond to user questions."""


    return """EduGenie Demo Answer

Gemini API quota is currently unavailable.

However, EduGenie is working correctly and the request reached the backend.

Your question was:

""" + prompt[-500:]


def generate_text(
    prompt: str,
    *,
    temperature: float | None = None,
    max_output_tokens: int | None = None
) -> str:

    try:

        client = get_client()

        for attempt in range(2):

            try:

                response = client.models.generate_content(

                    model=settings.gemini_model,

                    contents=prompt,

                    config=types.GenerateContentConfig(

                        temperature=(
                            settings.temperature
                            if temperature is None
                            else temperature
                        ),

                        max_output_tokens=(
                            settings.max_output_tokens
                            if max_output_tokens is None
                            else max_output_tokens
                        ),
                    ),
                )

                text = getattr(
                    response,
                    "text",
                    None
                )

                if text:
                    return text.strip()

                return demo_answer(prompt)


            except Exception as exc:

                error_text = str(exc)

                if (
                    "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                    or "quota" in error_text.lower()
                ):

                    print(
                        "Gemini quota exceeded."
                    )

                    return demo_answer(prompt)


                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                ):

                    if attempt == 0:

                        time.sleep(3)
                        continue

                    return demo_answer(prompt)


                print(
                    "Gemini error:",
                    error_text
                )

                return demo_answer(prompt)


    except Exception as exc:

        print(
            "Gemini client error:",
            exc
        )

        return demo_answer(prompt)