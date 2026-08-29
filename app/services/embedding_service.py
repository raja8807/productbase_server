from sentence_transformers import SentenceTransformer


model = None


def get_model():
    global model

    if model is None:
        print("Loading embedding model...")

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("Embedding model loaded.")

    return model


def create_embedding(text: str) -> list[float]:
    model = get_model()

    embedding = model.encode(text)

    return embedding.tolist()