def answer_question(question: str) -> str:

    question_lower = question.lower().strip()

    if "photosynthesis" in question_lower:

        return """Photosynthesis is the process by which green plants make their own food using sunlight, carbon dioxide, and water.

Chlorophyll helps plants absorb sunlight.

During photosynthesis, plants produce glucose as food and release oxygen.

Example:
Sunlight + Carbon Dioxide + Water → Glucose + Oxygen"""


    if "what is python" in question_lower:

        return """Python is a high-level programming language that is easy to read and learn.

It is commonly used for:
- Web development
- Artificial intelligence
- Data science
- Automation

Example:
print("Hello World")"""


    if (
        "what is ai" in question_lower
        or "what is artificial intelligence" in question_lower
    ):

        return """Artificial Intelligence (AI) is technology that allows computers to perform tasks that normally require human intelligence.

Examples include:
- Understanding language
- Recognizing images
- Answering questions
- Making predictions

Chatbots are an example of AI applications."""


    return f"""EduGenie Demo Answer

Your question was:

{question}

Gemini API quota is currently unavailable.

The EduGenie backend is working correctly.
Try one of the supported demo questions such as:

- What is photosynthesis?
- What is Python?
- What is Artificial Intelligence?"""