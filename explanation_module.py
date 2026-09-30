from config import settings

from gemini_client import generate_text


_local_pipeline = None


# ---------------------------------------------------------
# Local LaMini Explanation
# ---------------------------------------------------------

def _local_explain(
    topic: str
) -> str:

    global _local_pipeline

    try:

        from transformers import pipeline

    except ImportError as exc:

        raise RuntimeError(
            "Local explanation requires "
            "transformers, torch and sentencepiece.\n"
            "Install:\n"
            "pip install -r requirements-local.txt"
        ) from exc

    if _local_pipeline is None:

        _local_pipeline = pipeline(

            "text-generation",

            model=settings.local_explanation_model,

            device=-1
        )

    prompt = (
        "Explain the following educational "
        "topic for a beginner. "
        "Use simple words, a short definition, "
        "key points, and one example.\n\n"
        f"Topic: {topic}"
    )

    result = _local_pipeline(
        prompt,
        max_new_tokens=350,
        do_sample=False
    )

    return result[
        0
    ][
        "generated_text"
    ].strip()


# ---------------------------------------------------------
# Public Explanation Function
# ---------------------------------------------------------

def explain_topic(
    topic: str
) -> str:

    # Optional local model
    if settings.use_local_explanation:

        return _local_explain(
            topic
        )

    # Gemini explanation
    prompt = f"""
Explain the following educational topic
for a beginner.

Topic:

{topic}

Use exactly this structure:

1. Simple definition
2. How it works / main idea
3. Key points
4. One easy example
5. One-line recap

Use simple language.

Avoid unnecessary jargon.

Keep the explanation concise.
"""

    return generate_text(
        prompt
    )