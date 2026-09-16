import os
from pathlib import Path

import chromadb


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CHROMA_PATH = Path(
    os.getenv(
        "CHROMA_PATH",
        str(PROJECT_ROOT / "chroma_db"),
    )
)


client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = client.get_collection(
    name="data_model_rag"
)

result = collection.get(
    include=["documents", "metadatas"]
)

for i, document in enumerate(result["documents"]):
    print("=" * 80)
    print(f"CHUNK {i}")
    print("=" * 80)
    print(document)

    if result["metadatas"]:
        print("\nMETADATA:")
        print(result["metadatas"][i])

    print()
