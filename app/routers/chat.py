from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.config import settings
from app.auth import get_company_id
from app.services.openai_chat import run_chat

router = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
def post_chat(body: ChatRequest, company_id: str = Depends(get_company_id)):
    """Send a message; OpenAI uses our data tools scoped to your company and returns a concise reply."""
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not set. Add it to .env to use the chat endpoint.",
        )
    try:
        reply = run_chat(body.message.strip() or "Hello", company_id=company_id)
        return ChatResponse(reply=reply)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {e}")
