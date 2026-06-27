from pathlib import Path

def load_knowledge():
    knowledge_dir = Path("knowledge")
    documents = []

    for file in knowledge_dir.glob("*.md"):
        documents.append({
            "source": file.name,
            "content": file.read_text(encoding="utf-8")
        })

    return documents


def search_knowledge(question, documents):
    results = []

    for doc in documents:
        if any(word.lower() in doc["content"].lower() for word in question.split()):
            results.append(doc)

    return results[:3]