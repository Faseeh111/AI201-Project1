import os

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "data/chroma"
COLLECTION_NAME = "climbing_guide_chunks"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"
TOP_K = 3

load_dotenv()

print("Loading embedding model...")
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

print("Loading ChromaDB...")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma_client.get_collection(name=COLLECTION_NAME)

print("Ready!")


def retrieve_chunks(question, top_k=TOP_K):
    query_embedding = embedding_model.encode([question]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []

    for doc, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": doc,
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "distance": distance
        })

    return chunks


def build_context(chunks):
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']} | Chunk {chunk['chunk_index']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n---\n\n".join(context_parts)


def generate_answer(question, chunks):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env file")

    client = Groq(api_key=api_key)

    context = build_context(chunks)

    prompt = f"""
You are answering questions for a beginner rock climbing guide.

Use ONLY the retrieved context below to answer the question.
Do not use outside knowledge.

If the context does not contain enough information to answer, say exactly:
"I don't have enough information in the provided sources to answer that."

Question:
{question}

Retrieved context:
{context}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded RAG assistant. "
                    "Answer only from the provided context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


def ask(question):
    chunks = retrieve_chunks(question)

    answer = generate_answer(question, chunks)

    sources = sorted(set(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


def main():
    test_questions = [
        "What type of climbing shoes are good for beginners?",
        "Can I start hangboarding if I started climbing this week?",
        "What does 5.12a mean?",
        "What is the best protein powder for climbing?"
    ]

    for question in test_questions:
        print("\n" + "=" * 90)
        print(f"QUESTION: {question}")
        print("=" * 90)

        result = ask(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        for source in result["sources"]:
            print(f"- {source}")


if __name__ == "__main__":
    main()