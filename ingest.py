import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def fetch_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=45)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)

    return "\n".join(lines)

def main():
    with open("documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)

    for doc in documents:
        print(f"Fetching: {doc['title']}")

        try:
            text = fetch_text(doc["url"])
        except Exception as e:
            print(f"FAILED: {doc['title']}")
            print(e)
            continue

        output_path = RAW_DIR / f"{doc['id']}.txt"
        output_path.write_text(text, encoding="utf-8")

        print(f"Saved {output_path} ({len(text)} characters)")

if __name__ == "__main__":
    main()