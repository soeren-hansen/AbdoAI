import chromadb

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "abdoai_knowledge"

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def retrieve_context(question: str, n_results: int = 3) -> str:
    """
    Finds the most relevant knowledge chunks in ChromaDB
    and returns them as plain text context for GPT.
    """

    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for document, metadata in zip(documents, metadatas):
        source = metadata.get("source", "Unknown source")
        chunk = metadata.get("chunk", "Unknown chunk")

        context_parts.append(
            f"Kilde: {source} | Chunk: {chunk}\n"
            f"{document}"
        )

    return "\n\n---\n\n".join(context_parts)


def retrieve(question, n_results=4):
    return retrieve_context(question, n_results=n_results)


if __name__ == "__main__":
    question = "Hvornår må patienten køre bil?"
    context = retrieve_context(question)
    print(context)