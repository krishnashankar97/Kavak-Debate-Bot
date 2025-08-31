from typing import List, Dict
from app.core.config import settings
from app.store.memory import last_n_pairs, get_frame
import pathlib

SYSTEM_PROMPT = (pathlib.Path("configuration") / "system_prompt.md").read_text()

def build_messages(conversation_id: str, user_turn: str) -> List[Dict[str, str]]:
    topic, stance = get_frame(conversation_id)
    preface = f"Topic: {topic}\nYour side: {stance}"

    history = last_n_pairs(conversation_id, settings.max_history_pairs)
    msgs: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.append({"role": "system", "content": preface})

    for h in history:
        msgs.append({"role": "user" if h["role"]=="user" else "assistant", "content": h["message"]})

    msgs.append({"role": "user", "content": user_turn})
    return msgs