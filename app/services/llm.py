# app/services/llm.py
from openai import OpenAI
from app.core.config import settings
import asyncio

client = OpenAI(api_key=settings.openai_api_key)

async def complete(messages, timeout_s: int):
    # OpenAI .create(...) is synchronous -> run it in a thread
    def _call():
        return client.chat.completions.create(
            model=settings.model_name,
            messages=messages,
            temperature=settings.temperature,
        )

    return await asyncio.wait_for(asyncio.to_thread(_call), timeout=timeout_s)
