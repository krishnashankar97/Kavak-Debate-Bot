from pydantic import BaseModel
from typing import List, Literal, Optional

Role = Literal["user", "bot"]

class Message(BaseModel):
    role: Role
    message: str

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    message: List[Message]  # last 5 pairs, most recent last
