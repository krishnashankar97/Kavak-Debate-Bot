import json, uuid
from typing import List, Dict, Any, Tuple
import redis
from app.core.config import settings

r = redis.from_url(settings.redis_url, decode_responses=True)

def new_conversation() -> str:
    return str(uuid.uuid4())

def _key(cid: str) -> str:
    return f"conv:{cid}"

def append_message(conversation_id: str, role: str, message: str) -> None:
    r.rpush(_key(conversation_id), json.dumps({"role": role, "message": message}))

def get_all(conversation_id: str) -> List[Dict[str, Any]]:
    raw = r.lrange(_key(conversation_id), 0, -1)
    return [json.loads(x) for x in raw]

def last_n_pairs(conversation_id: str, n_pairs: int) -> List[Dict[str, Any]]:
    raw = r.lrange(_key(conversation_id), -2*n_pairs, -1)
    return [json.loads(x) for x in raw] if raw else []

def set_frame(conversation_id: str, topic: str, stance: str) -> None:
    r.hset(_key(conversation_id)+":frame", mapping={"topic": topic, "stance": stance})

def get_frame(conversation_id: str) -> Tuple[str, str]:
    d = r.hgetall(_key(conversation_id)+":frame")
    return d.get("topic", ""), d.get("stance", "")
