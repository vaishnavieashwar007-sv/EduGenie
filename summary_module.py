from gemini_client import generate_text


def summarize_text(
    text: str
) -> str:

    prompt = f"""
Summarize the following educational text
for a student.

Requirements:

- Preserve the important facts.
- Preserve the original meaning.
- Remove unnecessary repetition.
- Use simple language.
- Prefer a short heading followed by bullets.
- Do not introduce information
  that does not exist in the source.

Educational text:

{text}
"""

    return generate_text(
        prompt
    )