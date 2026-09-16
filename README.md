# CommanDataModelRAG

A FastAPI-based Retrieval-Augmented Generation (RAG) service for querying the Microsoft Common Data Model (CDM) using natural language.

## Features

- Parses Microsoft CDM Banking Model schemas
- Stores entity definitions in a vector database (ChromaDB)
- Natural language Q&A over CDM entities, attributes, and relationships
- FastAPI REST API
- Unit tests for retrieval logic
- Dockerized deployment

## Example Questions

- What are the core attributes of the Account entity?
- How does Contact relate to Organization?
- What entities exist in the Banking Core Data Model?

## Tech Stack

- FastAPI
- ChromaDB
- Snetence Transofrmer Embeddings
- LLama3
- Pytest
- Docker
