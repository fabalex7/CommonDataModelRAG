from unittest.mock import MagicMock

from app.rag import RAGPipeline


def test_retrieve_context_flattens_documents_and_queries_collection():
    collection = MagicMock()

    collection.query.return_value = {
        "documents": [
            [
                "Account represents a customer account.",
                "Account has an account number.",
            ],
            [
                "Organization represents a business.",
            ]
        ]
    }

    pipeline = RAGPipeline(collection=collection)

    context = pipeline.retrieve_context(
        "What are the core Account attributes?"
    )

    assert context == (
        "Account represents a customer account.\n\n"
        "Account has an account number.\n\n"
        "Organization represents a business."
    )

    collection.query.assert_called_once_with(
        query_texts=["What are the core Account attributes?"],
        n_results=5,
    )


def test_retrieve_context_returns_empty_string_when_no_documents_are_found():
    collection = MagicMock()
    collection.query.return_value = {"documents": [[]]}

    pipeline = RAGPipeline(collection=collection)

    context = pipeline.retrieve_context("Unknown entity")

    assert context == ""