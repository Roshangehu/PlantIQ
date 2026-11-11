from fastapi import APIRouter

from backend.schemas.chat_schema import (
    ChatRequest,
    ChatResponse
)

from backend.services.query_pipeline import pipeline


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question

    # Pass the question to the AI pipeline
    answer = pipeline(question)

    return ChatResponse(answer=answer)