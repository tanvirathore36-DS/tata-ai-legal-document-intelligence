from pathlib import Path

from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings


# ---------------------------------------------------------
# Embedding model
# ---------------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


class SentenceTransformerEmbeddings(Embeddings):

    def embed_documents(self, texts):
        return model.encode(texts).tolist()

    def embed_query(self, text):
        return model.encode(text).tolist()


embedding_function = SentenceTransformerEmbeddings()


# ---------------------------------------------------------
# ChromaDB configuration
# ---------------------------------------------------------

# This is the location where Hariom's/vector team's
# ChromaDB will be available.
VECTOR_DB_PATH = Path("chroma_db")


vector_store = Chroma(
    collection_name="tata_legal_knowledge",
    embedding_function=embedding_function,
    persist_directory=str(VECTOR_DB_PATH)
)


# ---------------------------------------------------------
# Retriever
# ---------------------------------------------------------

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# ---------------------------------------------------------
# Public function used by our backend
# ---------------------------------------------------------

def retrieve_relevant_knowledge(query: str) -> list:
    """
    Retrieve the top relevant legal knowledge chunks
    for a contract clause or legal question.
    """

    if not query or not query.strip():
        return []

    documents = retriever.invoke(query)

    results = []

    for document in documents:

        results.append({
            "content": document.page_content,
            "source": document.metadata.get("source"),
            "page": document.metadata.get("page")
        })

    return results