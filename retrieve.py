import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "data/chroma"
COLLECTION_NAME = "climbing_guide_chunks"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3

def retrieve(query, top_k=TOP_K):
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    model = SentenceTransformer(EMBEDDING_MODEL)
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results


def print_results(query, results):
    print("\n" + "=" * 90)
    print(f"QUERY: {query}")
    print("=" * 90)

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, distance) in enumerate(zip(docs, metas, distances), start=1):
        print(f"\n--- Result {i} ---")
        print(f"Source: {meta['source']}")
        print(f"Chunk index: {meta['chunk_index']}")
        print(f"Distance: {distance:.4f}")
        print()
        print(doc[:1200])


def main():
    test_queries = [
        "What type of climbing shoes are good for beginners?",
        "Can I start hangboarding if I started climbing this week?",
        "What does 5.12a mean?"
    ]

    for query in test_queries:
        results = retrieve(query)
        print_results(query, results)


if __name__ == "__main__":
    main()