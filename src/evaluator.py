from typing import Dict

from sklearn.metrics.pairwise import cosine_similarity

from src.embeddings import get_embedding
from src.questions import normalize_text


def _label_from_score(score: float) -> str:
    if score > 85:
        return "Excellent Answer"
    if score > 70:
        return "Good Answer"
    if score > 50:
        return "Average Answer"
    return "Needs Improvement"


def generate_feedback(score: float) -> str:
    """
    Generate feedback based on the similarity score.
    """
    if score > 85:
        return "Excellent answer. Very close to the ideal explanation."
    elif score > 70:
        return "Good answer. You covered most important concepts but could add more details."
    elif score > 50:
        return "Fair answer. Some key concepts are missing. Try to explain the idea more clearly."
    else:
        return "Poor answer. The explanation is quite different from the expected answer."


def evaluate_answer(question: str, candidate_answer: str, ideal_answer: str | None) -> Dict[str, float | str]:
    """
    Evaluate candidate answer against the ideal answer.
    Returns a dict with score, label, and feedback.
    """
    if ideal_answer is None:
        return {
            "score": 0.0,
            "label": "Question Not Found",
            "feedback": "Question not found in the question bank.",
        }

    normalized_candidate = normalize_text(candidate_answer)

    candidate_embedding = get_embedding(normalized_candidate)
    ideal_embedding = get_embedding(ideal_answer)

    similarity = cosine_similarity(
        [candidate_embedding],
        [ideal_embedding],
    )[0][0]

    score = round(float(similarity * 100), 2)
    label = _label_from_score(score)
    feedback = generate_feedback(score)

    return {
        "score": score,
        "label": label,
        "feedback": feedback,
    }