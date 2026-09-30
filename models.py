from typing import List

from pydantic import BaseModel, Field, field_validator


def clean_value(value: str) -> str:
    value = value.strip()

    if not value:
        raise ValueError("Input cannot be empty.")

    return value


class QARequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=10000
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value):
        return clean_value(value)


class ExplainRequest(BaseModel):
    topic: str = Field(
        min_length=2,
        max_length=10000
    )

    level: str = Field(
        default="beginner",
        max_length=40
    )

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value):
        return clean_value(value)


class QuizRequest(BaseModel):
    text: str = Field(
        min_length=20,
        max_length=30000
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        return clean_value(value)


class SummaryRequest(BaseModel):
    text: str = Field(
        min_length=30,
        max_length=30000
    )

    style: str = Field(
        default="concise",
        max_length=40
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value):
        return clean_value(value)


class LearningPathRequest(BaseModel):
    topic: str = Field(
        min_length=2,
        max_length=3000
    )

    level: str = Field(
        default="beginner",
        max_length=40
    )

    weeks: int = Field(
        default=6,
        ge=1,
        le=52
    )

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, value):
        return clean_value(value)


class TextResponse(BaseModel):
    result: str


class QuizQuestion(BaseModel):
    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str = ""


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]


class LearningPathResponse(BaseModel):
    result: str


class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
    local_explainer_enabled: bool
    gemini_model: str
