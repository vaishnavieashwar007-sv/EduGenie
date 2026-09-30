from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weeks: int = 6
) -> str:

    prompt = f"""
Create a personalized learning path.

Topic:
{topic}

Learner level:
{level}

Duration:
{weeks} weeks

Create a structured learning path from
foundational concepts to advanced concepts.

Include:

1. Learning goal
2. Prerequisites
3. Stage-by-stage topics
4. Suggested timeline
5. Practice activities
6. Projects
7. Progress checks
8. Suggested resource TYPES

Examples of resource types:

- Official documentation
- Textbook
- Tutorial
- Lecture
- Practice platform

Do not invent URLs.
Do not invent authors.
Do not invent specific resources.

Keep the learning plan practical,
clear and easy to follow.
"""

    return generate_text(
        prompt,
        max_output_tokens=3500
    )
