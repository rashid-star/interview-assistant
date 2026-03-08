from sklearn.metrics.pairwise import cosine_similarity
from src.embeddings import get_embedding
from src.questions import get_ideal_answer
from src.questions import normalize_question 

def generate_feedback(score):
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


def evaluate_answer(question, candidate_answer):
    """
    Evaluate candidate answer against the ideal answer.
    """

    ideal_answer = get_ideal_answer(question)

    ideal_answer = get_ideal_answer(question)

    if ideal_answer is None:
        return {
            "score": 0,
            "feedback": "Question not found in the question bank."
        }

    candidate_answer = normalize_question(candidate_answer)
    candidate_embedding = get_embedding(candidate_answer)
    ideal_embedding = get_embedding(ideal_answer)

    similarity = cosine_similarity(
        [candidate_embedding],
        [ideal_embedding]
    )[0][0]

    score = round(float(similarity * 100), 2)

    feedback = generate_feedback(score)

    return {
        "score": score,
        "feedback": feedback
    }