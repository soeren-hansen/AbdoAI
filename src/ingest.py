from pathlib import Path
import chromadb

KNOWLEDGE_DIR = Path("knowledge")
CHROMA_DIR = "chroma_db"

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="abdoai_knowledge")


def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def ingest_documents():
    for file in KNOWLEDGE_DIR.glob("*.md"):
        text = file.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            collection.add(
                documents=[chunk],
                metadatas=[{"source": file.name, "chunk": i}],
                ids=[f"{file.stem}_{i}"]
            )

    print("Knowledge base indexed in ChromaDB.")


if __name__ == "__main__":
    ingest_documents()