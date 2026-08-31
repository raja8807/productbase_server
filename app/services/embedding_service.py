# from sentence_transformers import SentenceTransformer


# model = None


# def get_model():
#     global model

#     if model is None:
#         print("Loading embedding model...")

#         model = SentenceTransformer(
#             "sentence-transformers/all-MiniLM-L6-v2"
#         )

#         print("Embedding model loaded.")

#     return model


# def create_embedding(text: str) -> list[float]:
#     model = get_model()

#     embedding = model.encode(text)

#     return embedding.tolist()

import os

from huggingface_hub import InferenceClient


client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_TOKEN"),
)

def create_embedding(text: str) -> list[float]:
    result = client.feature_extraction(
        text,
        model="sentence-transformers/all-MiniLM-L6-v2",
    )

    result = result.squeeze()

    print("Embedding dimensions:", len(result))

    return result.tolist()

