from fastapi import FastAPI
from pydantic import BaseModel

from src.questions import get_domains, get_questions, get_ideal_answer
from src.evaluator import evaluate_answer
from fastapi import HTTPException
from src.llm_groq import (
    get_concept_answer,
    generate_interview_question,
    generate_practice_coaching,
)


app = FastAPI(title="AI Interview Assistant")


class EvaluateRequest(BaseModel):
    domain: str
    question: str
    answer: str


class EvaluateResponse(BaseModel):
    domain: str
    question: str
    score: float
    label: str
    basic_feedback: str
    ideal_answer: str | None = None
    coach_feedback: str | None = None
    improved_answer: str | None = None
    follow_up_question: str | None = None


class ChatRequest(BaseModel):
    domain: str
    message: str


class ChatResponse(BaseModel):
    domain: str
    message: str
    answer: str


class GenerateQuestionRequest(BaseModel):
    domain: str
    difficulty: str = "medium"  # easy | medium | hard


class GenerateQuestionResponse(BaseModel):
    domain: str
    difficulty: str
    question: str


@app.get("/domains")
def list_domains():
    """
    Return available interview domains/tracks.
    """
    return {"domains": get_domains()}


@app.get("/questions")
def list_questions(domain: str):
    """
    Return available interview questions for a given domain.
    """
    return {
        "domain": domain,
        "questions": get_questions(domain),
    }


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(request: EvaluateRequest):
    """
    Evaluate a candidate answer for a given domain and question.
    """
    ideal_answer = get_ideal_answer(request.domain, request.question)

    result = evaluate_answer(
        question=request.question,
        candidate_answer=request.answer,
        ideal_answer=ideal_answer,
    )

    coach_feedback = None
    improved_answer = None
    follow_up_question = None

    # Groq coaching is optional: if anything fails, keep the local score working.
    try:
        coaching = generate_practice_coaching(
            domain=request.domain,
            question=request.question,
            candidate_answer=request.answer,
            ideal_answer=ideal_answer,
            score=float(result["score"]),
        )
        coach_feedback = coaching.get("feedback")
        improved_answer = coaching.get("improved_answer")
        follow_up_question = coaching.get("follow_up_question")
    except Exception:
        pass

    return EvaluateResponse(
        domain=request.domain,
        question=request.question,
        score=result["score"],
        label=result["label"],
        basic_feedback=result["feedback"],
        ideal_answer=ideal_answer,
        coach_feedback=coach_feedback,
        improved_answer=improved_answer,
        follow_up_question=follow_up_question,
    )

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = get_concept_answer(request.domain, request.message)

        return ChatResponse(
            domain=request.domain,
            message=request.message,
            answer=answer,
        )

    except Exception as e:
        print("CHAT ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = get_concept_answer(request.domain, request.message)

    return ChatResponse(
        domain=request.domain,
        message=request.message,
        answer=answer,
    )