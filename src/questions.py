from typing import List, Dict, Optional

ABBREVIATIONS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",
}


def normalize_text(text: str) -> str:
    """
    Normalize text:
    - lowercase
    - remove punctuation
    - expand common abbreviations
    """
    import re

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    words = text.split()
    expanded_words = [
        ABBREVIATIONS.get(word, word)
        for word in words
    ]
    return " ".join(expanded_words)


# Question bank organized by domain
QUESTION_BANK: Dict[str, List[Dict[str, str]]] = {
    "machine_learning": [
        {
            "question": "What is Machine Learning?",
            "ideal_answer": """
Machine learning is a subset of artificial intelligence where algorithms
learn patterns from data and improve their performance over time without
being explicitly programmed.
""",
        },
        {
            "question": "What is the difference between supervised and unsupervised learning?",
            "ideal_answer": """
Supervised learning uses labeled data where the correct output is known
during training. Unsupervised learning works with unlabeled data and
tries to discover hidden patterns or groupings in the data.
""",
        },
        {
            "question": "What is overfitting in machine learning?",
            "ideal_answer": """
Overfitting occurs when a machine learning model learns the training data
too well, including noise and random fluctuations. This causes the model
to perform poorly on unseen data.
""",
        },
        {
            "question": "What is underfitting?",
            "ideal_answer": """
Underfitting happens when a model is too simple to capture the underlying
patterns in the data, resulting in poor performance on both training and
testing datasets.
""",
        },
        {
            "question": "What is the bias-variance tradeoff?",
            "ideal_answer": """
The bias-variance tradeoff describes the balance between a model's ability
to generalize and its complexity. High bias leads to underfitting, while
high variance leads to overfitting. A good model balances both.
""",
        },
        {
            "question": "What is cross validation?",
            "ideal_answer": """
Cross validation is a technique used to evaluate the performance of a
machine learning model by splitting the dataset into multiple training
and validation subsets to ensure the model generalizes well.
""",
        },
        {
            "question": "What is gradient descent?",
            "ideal_answer": """
Gradient descent is an optimization algorithm used to minimize the loss
function by iteratively updating model parameters in the direction of the
negative gradient.
""",
        },
    ],
    "deep_learning": [
        {
            "question": "What is deep learning?",
            "ideal_answer": """
Deep learning is a subset of machine learning that uses neural networks
with many layers to automatically learn hierarchical feature representations
from data.
""",
        },
        {
            "question": "What is a convolutional neural network?",
            "ideal_answer": """
A convolutional neural network (CNN) is a type of deep learning model
designed to process grid-like data such as images using convolutional
layers to automatically learn spatial features.
""",
        },
    ],
    "nlp": [
        {
            "question": "What is natural language processing?",
            "ideal_answer": """
Natural language processing is a field of artificial intelligence that
focuses on enabling computers to understand, interpret, and generate human
language.
""",
        },
        {
            "question": "What is tokenization in NLP?",
            "ideal_answer": """
Tokenization is the process of splitting text into smaller units such as
words, subwords, or characters so that they can be processed by NLP models.
""",
        },
    ],
    "data_science": [
        {
            "question": "What does a data scientist do?",
            "ideal_answer": """
A data scientist collects, cleans, analyzes, and models data to generate
insights and support decision making, often using statistics, machine
learning, and domain knowledge.
""",
        },
    ],
    "data_analytics": [
        {
            "question": "What is the difference between data analytics and data science?",
            "ideal_answer": """
Data analytics focuses on exploring and visualizing existing data to answer
specific business questions. Data science is broader and often involves
building predictive models and machine learning solutions.
""",
        },
    ],
    "web_development": [
        {
            "question": "What is the difference between frontend and backend development?",
            "ideal_answer": """
Frontend development focuses on the part of a website or application that
users see and interact with in the browser. Backend development deals with
servers, databases, and application logic that support the frontend.
""",
        },
        {
            "question": "What is REST API?",
            "ideal_answer": """
A REST API is an architectural style for designing networked applications.
It uses HTTP methods like GET, POST, PUT, and DELETE to operate on resources
identified by URLs, usually returning JSON or XML.
""",
        },
    ],
}


def get_domains() -> List[str]:
    """Return the list of available domains/tracks."""
    return list(QUESTION_BANK.keys())


def get_questions(domain: str) -> List[str]:
    """Return only the question texts for a given domain."""
    domain = domain.lower()
    if domain not in QUESTION_BANK:
        return []

    return [q["question"] for q in QUESTION_BANK[domain]]


def get_ideal_answer(domain: str, question: str) -> Optional[str]:
    """
    Return the ideal answer for a question inside a domain.
    Uses normalized comparison for robustness.
    """
    domain = domain.lower()
    if domain not in QUESTION_BANK:
        return None

    normalized_input = normalize_text(question)

    for q in QUESTION_BANK[domain]:
        stored_question = normalize_text(q["question"])
        if stored_question == normalized_input:
            return q["ideal_answer"]

    return None