import json
import shutil
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path("data/chunks/chunks.json")
CHROMA_DIR = Path("data/chroma")
COLLECTION_NAME = "climbing_guide_chunks"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_chunks():
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError("Run chunk.py first. Missing data/chunks/chunks.json")

    with CHUNKS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")

    # Rebuild the database fresh each time to avoid duplicates
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.create_collection(name=COLLECTION_NAME)

    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        ids.append(chunk["id"])
        documents.append(chunk["text"])
        metadatas.append({
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
            "word_count": chunk["word_count"]
        })

    print("Embedding chunks...")
    embeddings = model.encode(documents, show_progress_bar=True).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Saved {len(chunks)} chunks to ChromaDB")
    print(f"Database location: {CHROMA_DIR}")


if __name__ == "__main__":
    main()