from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="EduGenie AI",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# ============================================================
# JINJA2 TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ============================================================
# REQUEST MODELS
# ============================================================

class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )


class QuizRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=10,
        max_length=30000
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


class LearningPathRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=2,
        max_length=500
    )

    level: str = "beginner"

    weeks: int = Field(
        default=6,
        ge=1,
        le=52
    )


# ============================================================
# HOME PAGE
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie AI",
        "version": "1.0.0"
    }


# ============================================================
# QUESTION & ANSWER
# ============================================================

@app.post("/qa")
async def qa(request: QuestionRequest):

    try:

        result = answer_question(
            request.question
        )

        return {
            "success": True,
            "answer": result
        }

    except Exception as exc:

        return {
            "success": False,
            "answer": f"Error: {str(exc)}"
        }


# ============================================================
# EXPLAIN TOPIC
# ============================================================

@app.post("/explain")
async def explain(request: TextRequest):

    try:

        result = explain_topic(
            request.text
        )

        return {
            "success": True,
            "explanation": result
        }

    except Exception as exc:

        return {
            "success": False,
            "explanation": f"Error: {str(exc)}"
        }


# ============================================================
# GENERATE QUIZ
# ============================================================

@app.post("/quiz")
async def quiz(request: QuizRequest):

    try:

        result = generate_quiz(
            request.text,
            request.count
        )

        return {
            "success": True,
            "quiz": result
        }

    except Exception as exc:

        return {
            "success": False,
            "quiz": [],
            "error": str(exc)
        }


# ============================================================
# SUMMARIZE TEXT
# ============================================================

@app.post("/summarize")
async def summarize(request: TextRequest):

    try:

        result = summarize_text(
            request.text
        )

        return {
            "success": True,
            "summary": result
        }

    except Exception as exc:

        return {
            "success": False,
            "summary": f"Error: {str(exc)}"
        }


# ============================================================
# PERSONALIZED LEARNING PATH
# ============================================================

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: LearningPathRequest
):

    try:

        result = get_learning_recommendations(
            request.topic,
            request.level,
            request.weeks
        )

        return {
            "success": True,
            "recommendations": result
        }

    except TypeError:

        # Compatibility with a learning_path.py
        # that accepts only topic and level.

        try:

            result = get_learning_recommendations(
                request.topic,
                request.level
            )

            return {
                "success": True,
                "recommendations": result
            }

        except Exception as exc:

            return {
                "success": False,
                "recommendations": f"Error: {str(exc)}"
            }

    except Exception as exc:

        return {
            "success": False,
            "recommendations": f"Error: {str(exc)}"
        }


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )