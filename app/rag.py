import os

import chromadb
from ollama import Client


class RAGPipeline:
    def __init__(self):
        chroma_path = os.getenv(
            "CHROMA_PATH",
            "./chroma_db"
        )

        ollama_host = os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434"
        )

        self.chroma_client = chromadb.PersistentClient(
            path=chroma_path
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name="data_model_rag"
        )

        self.ollama_client = Client(
            host=ollama_host
        )

    def retrieve_context(self, question: str):

        results = self.collection.query(
            query_texts=[question],
            n_results=5,
        )

        context = "\n\n".join(
            doc
            for docs in results["documents"]
            for doc in docs
        )

        return context

    def generate_answer(
        self,
        question: str,
        context: str
    ):

        prompt = f"""
        You are a Common Data Model expert.

        Answer ONLY using the supplied context.

        If the answer cannot be found in the context,
        say so.

        Context:

        {context}

        Question:

        {question}
        """

        response = self.ollama_client.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    def ask(self, question: str):
        context = self.retrieve_context(question)
        answer = self.generate_answer(question, context)

        return {
            "question": question,
            "answer": answer
        }
