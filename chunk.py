import json
import random
import re
from pathlib import Path

RAW_DIR = Path("data/raw")
CHUNKS_DIR = Path("data/chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE = 300
OVERLAP_SENTENCES = 1

JUNK_LINES = {
    "Skip to content",
    "Close menu",
    "Products",
    "Instagram",
    "Facebook",
    "YouTube",
    "Twitter",
    "Log in",
    "Search",
    "Share",
    "Save",
    "Print",
    "Pinterest",
    "top of page",
    "bottom of page",
}


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)

    cleaned_lines = []
    for line in text.splitlines():
        line = line.strip()

        if not line:
            cleaned_lines.append("")
            continue

        if line in JUNK_LINES:
            continue

        if line.lower().startswith("shop "):
            continue

        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_into_blocks(text):
    blocks = []

    # First try normal paragraph splitting.
    rough_blocks = re.split(r"\n\s*\n", text)

    for block in rough_blocks:
        block = block.strip()

        if not block:
            continue

        # If a block is still huge, split it by sentence.
        if len(block.split()) > CHUNK_SIZE:
            sentences = split_into_sentences(block)
            blocks.extend(sentences)
        else:
            blocks.append(block)

    return blocks


def split_into_sentences(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def make_chunks(text, chunk_size=CHUNK_SIZE):
    blocks = split_into_blocks(text)

    chunks = []
    current = []
    current_words = 0
    previous_last_sentence = ""

    for block in blocks:
        block_words = len(block.split())

        if current_words + block_words > chunk_size and current:
            chunk_text = "\n\n".join(current)
            chunks.append(chunk_text)

            if previous_last_sentence:
                current = [previous_last_sentence, block]
                current_words = len(previous_last_sentence.split()) + block_words
            else:
                current = [block]
                current_words = block_words
        else:
            current.append(block)
            current_words += block_words

        sentences = split_into_sentences(block)
        if sentences:
            previous_last_sentence = sentences[-1]

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def chunk_file(path):
    text = path.read_text(encoding="utf-8")
    text = clean_text(text)

    chunk_texts = make_chunks(text)

    chunks = []
    for i, chunk_text in enumerate(chunk_texts):
        chunks.append({
            "id": f"{path.stem}_chunk_{i}",
            "source": path.name,
            "chunk_index": i,
            "word_count": len(chunk_text.split()),
            "text": chunk_text
        })

    return chunks


def main():
    all_chunks = []
    txt_files = sorted(RAW_DIR.glob("*.txt"))

    if not txt_files:
        print("No .txt files found in data/raw")
        return

    for path in txt_files:
        file_chunks = chunk_file(path)
        all_chunks.extend(file_chunks)
        print(f"{path.name}: {len(file_chunks)} chunks")

    output_path = CHUNKS_DIR / "chunks.json"
    output_path.write_text(
        json.dumps(all_chunks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print()
    print(f"Saved chunks to {output_path}")
    print(f"Total chunks: {len(all_chunks)}")

    print()
    print("===== 5 RANDOM SAMPLE CHUNKS =====")

    for chunk in random.sample(all_chunks, min(5, len(all_chunks))):
        print("\n" + "-" * 80)
        print(f"ID: {chunk['id']}")
        print(f"Source: {chunk['source']}")
        print(f"Word count: {chunk['word_count']}")
        print()
        print(chunk["text"][:1200])


if __name__ == "__main__":
    main()