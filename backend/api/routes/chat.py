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

    # Convert previous messages into dictionaries
    history = [
        message.model_dump()
        for message in request.history
    ]

    # Pass BOTH question and conversation history
    answer = pipeline(question, history)

    return ChatResponse(answer=answer)