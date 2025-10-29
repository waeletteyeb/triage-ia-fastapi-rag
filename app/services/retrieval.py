# app/services/retrieval.py
import chromadb
from app.services.embeddings import BioGPTEmbeddingFunction
from app.config import CHROMA_PATH, CHROMA_COLLECTION

# ChromaDB persistent client & collection (same as original)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
embedding_fn = BioGPTEmbeddingFunction()
collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=embedding_fn,
)
