from gemini_client import generate_text
from utils import parse_json_response


# ---------------------------------------------------------
# Validate Quiz
# ---------------------------------------------------------

def _validate_quiz(data, count: int):

    if not isinstance(data, list):
        raise ValueError(
            "Quiz response must be a JSON list."
        )

    validated = []

    for index, item in enumerate(data, start=1):

        if not isinstance(item, dict):
            continue

        question = str(
            item.get("question", "")
        ).strip()

        options = item.get("options")

        answer = str(
            item.get("correct_answer", "")
        ).strip()

        if not question:
            continue

        if not isinstance(options, list):
            continue

        if len(options) != 4:
            continue

        options = [
            str(option).strip()
            for option in options
        ]

        if any(not option for option in options):
            continue

        # Make sure correct answer matches an option.
        if answer not in options:

            # Sometimes Gemini returns A/B/C/D instead
            # of the actual option text.
            answer_map = {
                "A": options[0],
                "B": options[1],
                "C": options[2],
                "D": options[3],
            }

            if answer.upper() in answer_map:
                answer = answer_map[answer.upper()]
            else:
                continue

        validated.append({
            "question": question,
            "options": options,
            "correct_answer": answer
        })

        if len(validated) >= count:
            break

    if len(validated) < count:
        raise ValueError(
            f"Expected {count} valid questions "
            f"but received {len(validated)}."
        )

    return validated[:count]


# ---------------------------------------------------------
# Fallback Quiz
# ---------------------------------------------------------

def _fallback_quiz(passage: str, count: int):

    text = passage.strip()

    if not text:
        text = "This is a sample educational passage."

    # Safe local fallback so the application does not crash
    # when Gemini quota is unavailable or returns invalid JSON.

    questions = []

    templates = [
        {
            "question": "What is the main topic discussed in the passage?",
            "options": [
                "The main idea of the passage",
                "An unrelated topic",
                "A completely different subject",
                "None of the above"
            ],
            "correct_answer": "The main idea of the passage"
        },
        {
            "question": "What can be understood from the passage?",
            "options": [
                "The information presented in the passage",
                "Information that is not mentioned",
                "An unrelated fact",
                "None of the above"
            ],
            "correct_answer": "The information presented in the passage"
        },
        {
            "question": "Which statement best represents the passage?",
            "options": [
                "It explains the subject described in the passage",
                "It discusses an unrelated subject",
                "It contains no useful information",
                "None of the above"
            ],
            "correct_answer": "It explains the subject described in the passage"
        }
    ]

    for item in templates[:count]:
        questions.append(item)

    return questions


# ---------------------------------------------------------
# Generate Quiz
# ---------------------------------------------------------

def generate_quiz(
    passage: str,
    count: int = 3
):

    # Safety check
    if count < 1:
        count = 1

    if count > 10:
        count = 10

    prompt = f"""
Create exactly {count} educational
multiple-choice questions from the passage below.

IMPORTANT:

- Return EXACTLY {count} questions.
- Return ONLY valid JSON.
- Do NOT use Markdown.
- Do NOT use ```json.
- Do NOT add explanations before or after the JSON.
- Every question must contain exactly 4 options.
- There must be exactly one correct answer.
- The correct_answer value MUST exactly match
  one of the four option strings.
- Questions must be based ONLY on the passage.
- Questions should test understanding.

Use this exact JSON structure:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option A"
  }}
]

Passage:

{passage}
"""

    try:

        raw = generate_text(
            prompt,
            temperature=0.2,
            max_output_tokens=3000
        )

        # -------------------------------------------------
        # Detect Gemini quota fallback
        # -------------------------------------------------

        if (
            "EduGenie Demo Response" in raw
            or "Gemini API quota" in raw
            or "live Gemini response available" in raw
        ):
            return _fallback_quiz(
                passage,
                count
            )

        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        data = parse_json_response(raw)

        return _validate_quiz(
            data,
            count
        )

    except Exception as exc:

        # -------------------------------------------------
        # Do not crash the API.
        # Return a safe fallback quiz.
        # -------------------------------------------------

        print(
            "Quiz generation warning:",
            exc
        )

        return _fallback_quiz(
            passage,
            count
        )