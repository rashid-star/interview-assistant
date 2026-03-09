import os

from dotenv import load_dotenv
from groq import Groq


# Load variables from .env file into environment (once at import time)
load_dotenv()


def _get_client() -> Groq:
    """
    Create a Groq client using API key from environment.
    Supports GROQ_API_KEY or groq_api_key in .env / env.
    """
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("groq_api_key")

    if not api_key:
        raise RuntimeError(
            "Groq API key not found. Please set GROQ_API_KEY or groq_api_key in your environment or .env file."
        )

    return Groq(api_key=api_key)


def _get_model() -> str:
    return os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def get_concept_answer(domain: str, message: str) -> str:
    """
    Call Groq LLM to answer conceptual interview questions.
    """
    client = _get_client()

    system_prompt = (
        "You are an expert technical interview mentor. "
        "You explain concepts clearly and concisely for beginners, "
        "and give short bullet‑point tips on how to answer in an interview."
    )

    user_prompt = (
        f"Domain: {domain}\n"
        f"User question: {message}\n\n"
        "Explain the concept in simple language and include 3‑5 bullet points on how to answer this in an interview."
    )

    # Use a currently supported Groq chat model.
    # If this model name ever changes, update it from your Groq console.
    completion = client.chat.completions.create(
        model=_get_model(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=512,
    )

    return completion.choices[0].message.content.strip()


def generate_practice_coaching(
    domain: str,
    question: str,
    candidate_answer: str,
    ideal_answer: str | None,
    score: float,
) -> dict:
    """
    Return rich coaching feedback for practice mode.
    Output is a dict with keys: feedback, improved_answer, next_question (optional).
    """
    client = _get_client()

    system_prompt = (
        "You are a strict but helpful technical interviewer and coach. "
        "You give actionable feedback, point out missing concepts, and provide a better answer."
    )

    ideal_block = ideal_answer.strip() if ideal_answer else "(No ideal answer available.)"

    user_prompt = f"""
Domain: {domain}
Interview question: {question}

Candidate answer:
{candidate_answer}

Reference / ideal answer:
{ideal_block}

Similarity score (0-100): {score}

Now do this:
1) Give feedback in 3-6 bullet points (what's correct, what's missing, what to improve).
2) Provide an improved answer (6-12 lines max).
3) If score >= 85: propose one harder follow-up question.
   If score < 70: propose one simpler follow-up question.

Format exactly as:
FEEDBACK:
<bullets>

IMPROVED_ANSWER:
<text>

FOLLOW_UP_QUESTION:
<one question>
""".strip()

    completion = client.chat.completions.create(
        model=_get_model(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=700,
    )

    text = completion.choices[0].message.content.strip()

    # Very lightweight parsing (robust enough for our fixed format).
    def _section(name: str) -> str:
        start = text.find(f"{name}:\n")
        if start == -1:
            start = text.find(f"{name}:")
            if start == -1:
                return ""
            start = start + len(f"{name}:")
            if start < len(text) and text[start] == "\n":
                start += 1
        else:
            start += len(f"{name}:\n")

        # Find next section header
        next_headers = ["FEEDBACK:", "IMPROVED_ANSWER:", "FOLLOW_UP_QUESTION:"]
        end = len(text)
        for h in next_headers:
            if h == f"{name}:":
                continue
            idx = text.find("\n\n" + h)
            if idx != -1 and idx > start:
                end = min(end, idx)
        return text[start:end].strip()

    feedback = _section("FEEDBACK")
    improved_answer = _section("IMPROVED_ANSWER")
    follow_up = _section("FOLLOW_UP_QUESTION")

    return {
        "feedback": feedback or text,
        "improved_answer": improved_answer or None,
        "follow_up_question": follow_up or None,
    }


def generate_interview_question(domain: str, difficulty: str = "medium") -> str:
    """
    Generate one interview question for a given domain and difficulty.
    """
    client = _get_client()
    difficulty = (difficulty or "medium").lower()
    if difficulty not in {"easy", "medium", "hard"}:
        difficulty = "medium"

    system_prompt = "You are a technical interviewer. Output only the question text."
    user_prompt = (
        f"Generate ONE {difficulty} difficulty interview question for the domain: {domain}.\n"
        "Rules: Output a single question only. No numbering, no quotes, no extra text."
    )

    completion = client.chat.completions.create(
        model=_get_model(),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.6,
        max_tokens=120,
    )

    q = completion.choices[0].message.content.strip().strip('"').strip()
    # Remove accidental numbering like "1) ..."
    if len(q) > 2 and (q[0].isdigit() and q[1] in {".", ")", ":"}):
        q = q[2:].strip()
    return q
