from fastapi import FastAPI
from pydantic import BaseModel

from src.questions import get_questions
from src.evaluator import evaluate_answer

app = FastAPI(title="AI Interview Assistant")


class AnswerRequest(BaseModel):
    question: str
    answer: str


@app.get("/questions")
def list_questions():
    """
    Return available interview questions.
    """
    return {"questions": get_questions()}


@app.post("/evaluate")
def evaluate(request: AnswerRequest):
    """
    Evaluate a candidate answer.
    """

    result = evaluate_answer(request.question, request.answer)

    return {
        "question": request.question,
        "score": result["score"],
        "feedback": result["feedback"]
    }