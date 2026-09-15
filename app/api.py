from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import RAGPipeline

app = FastAPI()

rag = RAGPipeline()

class QuestionRequest(BaseModel):
    question: str
    
@app.get("/health")
def health():
    return {
        "status": "ok"
    }
    
@app.post("/ask")
def ask(request: QuestionRequest):

    result = rag.ask(
        request.question
    )

    return result