import os
from pathlib import Path
import chromadb

from app.parser import flatten_cdm

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "raw"

CHROMA_PATH = Path(
    os.getenv(
        "CHROMA_PATH",
        str(PROJECT_ROOT / "chroma_db")
    )
)


def ingest_cdm(path):
    documents = []

    for json_path in Path(path).rglob("*.json"):
        chunks = flatten_cdm(json_path)

        print(
            f"Ingested {len(chunks)} chunks from {json_path}"
        )

        documents.extend(chunks)

    print(
        f"Ingested {len(documents)} documents from {path}"
    )

    return documents


documents = ingest_cdm(DATA_PATH)

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = chroma_client.get_or_create_collection(
    name="data_model_rag"
)

for index, doc in enumerate(documents):
    collection.add(
        documents=[doc["text"]],
        metadatas=[doc["metadata"]],
        ids=[f"{doc['metadata']['name']}_{index}"],
    )
