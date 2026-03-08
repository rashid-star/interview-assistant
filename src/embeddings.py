from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    """
    Convert text into a vector embedding.
    """
    return model.encode(text)