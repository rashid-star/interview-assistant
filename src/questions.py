ABBREVIATIONS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing"
}

def normalize_question(question):
    """
    Normalize user question:
    - lowercase
    - remove punctuation
    - expand abbreviations
    """

    import re

    question = question.lower()

    # remove punctuation
    question = re.sub(r"[^\w\s]", "", question)

    # replace abbreviations
    words = question.split()

    expanded_words = []

    for word in words:
        if word in ABBREVIATIONS:
            expanded_words.append(ABBREVIATIONS[word])
        else:
            expanded_words.append(word)

    return " ".join(expanded_words)
# Question bank for the AI Interview Assistant

QUESTIONS = [
    {
    "question": "What is Machine Learning?",
    "ideal_answer": """
Machine learning is a subset of artificial intelligence where algorithms
learn patterns from data and improve their performance over time without
being explicitly programmed.
"""
},

{
    "question": "What is the difference between supervised and unsupervised learning?",
    "ideal_answer": """
Supervised learning uses labeled data where the correct output is known
during training. Unsupervised learning works with unlabeled data and
tries to discover hidden patterns or groupings in the data.
"""
},

{
    "question": "What is overfitting in machine learning?",
    "ideal_answer": """
Overfitting occurs when a machine learning model learns the training data
too well, including noise and random fluctuations. This causes the model
to perform poorly on unseen data.
"""
},

{
    "question": "What is underfitting?",
    "ideal_answer": """
Underfitting happens when a model is too simple to capture the underlying
patterns in the data, resulting in poor performance on both training and
testing datasets.
"""
},

{
    "question": "What is the bias-variance tradeoff?",
    "ideal_answer": """
The bias-variance tradeoff describes the balance between a model's ability
to generalize and its complexity. High bias leads to underfitting, while
high variance leads to overfitting. A good model balances both.
"""
},

{
    "question": "What is cross validation?",
    "ideal_answer": """
Cross validation is a technique used to evaluate the performance of a
machine learning model by splitting the dataset into multiple training
and validation subsets to ensure the model generalizes well.
"""
},

{
    "question": "What is gradient descent?",
    "ideal_answer": """
Gradient descent is an optimization algorithm used to minimize the loss
function by iteratively updating model parameters in the direction of the
negative gradient.
"""
},

{
    "question": "What is a confusion matrix?",
    "ideal_answer": """
A confusion matrix is a table used to evaluate classification models by
showing true positives, true negatives, false positives, and false negatives.
"""
},

{
    "question": "What is precision and recall?",
    "ideal_answer": """
Precision measures the proportion of correctly predicted positive cases
out of all predicted positives. Recall measures the proportion of correctly
predicted positive cases out of all actual positives.
"""
},

{
    "question": "What is natural language processing?",
    "ideal_answer": """
Natural language processing is a field of artificial intelligence that
focuses on enabling computers to understand, interpret, and generate human
language.
"""
}
]


def get_questions():
    return [q["question"] for q in QUESTIONS]


# def get_ideal_answer(question):
#     for q in QUESTIONS:
#         if q["question"].lower() == question.lower():
#             return q["ideal_answer"]

#     return None

def get_ideal_answer(question):

    normalized_input = normalize_question(question)

    for q in QUESTIONS:

        stored_question = normalize_question(q["question"])

        if stored_question == normalized_input:
            return q["ideal_answer"]

    return None