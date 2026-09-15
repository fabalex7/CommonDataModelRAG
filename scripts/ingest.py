import sys
from pathlib import Path

import chromadb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.parser import flatten_cdm

DATA_PATH = PROJECT_ROOT / "data" / "raw"

def ingest_cdm(path):
    documents = []
    for json_path in Path(path).rglob("*.json"):
        chunks = flatten_cdm(json_path)
        print(f"Ingested {len(chunks)} chunks from {json_path}")
        documents.extend(chunks)
    print(f"Ingested {len(documents)} documents from {path}")
    return documents

documents = ingest_cdm(DATA_PATH)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="data_model_rag")

for index, doc in enumerate(documents):
    collection.add(
        documents=[doc["text"]],
        metadatas=[doc["metadata"]],
        ids=[f"{doc['metadata']['name']}_{index}"],
    )