from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Message
from app.store.memory import new_conversation, append_message, set_frame, get_all
from app.services.llm import complete
from app.services.debate_engine import build_messages
from app.core.config import settings
import re, asyncio

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

def _extract_frame(first_message: str) -> tuple[str, str]:
    """Heuristic extractor for topic and stance from the first message."""
    m = re.search(r"(?:debate|argue|take the side)\s+that\s+(.*?)\s+(?:about|on|regarding)\s+(.*)", first_message, re.I)
    if m:
        return (m.group(2).strip(), m.group(1).strip())
    return (first_message.strip(), "as specified (pro)")

@router.post("/webhook", response_model=ChatResponse)
async def webhook(body: ChatRequest):
    if not body.message or not body.message.strip():
        raise HTTPException(status_code=400, detail="message is required")

    if body.conversation_id is None:
        cid = new_conversation()
        topic, stance = _extract_frame(body.message)
        set_frame(cid, topic, stance)
    else:
        cid = body.conversation_id

    append_message(cid, "user", body.message)

    try:
        resp = await complete(
            messages=build_messages(cid, body.message),
            timeout_s=settings.request_timeout_seconds
        )
        bot_text = resp.choices[0].message.content.strip()
    except asyncio.TimeoutError:
        bot_text = "I need a moment, but to stay within time I’ll keep it brief: I maintain my stance—here’s the core point..."
    except Exception:
        bot_text = "I hit a snag generating a response. I still stand by my position and will elaborate next turn."

    append_message(cid, "bot", bot_text)

    full = get_all(cid)
    last10 = full[-10:] if len(full) > 10 else full
    return ChatResponse(
        conversation_id=cid,
        message=[Message(**m) for m in last10]
    )
