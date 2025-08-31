from pydantic import BaseModel
import os

class Settings(BaseModel):
    env: str = os.getenv("ENV", "development")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
    max_history_pairs: int = int(os.getenv("MAX_HISTORY_PAIRS", "5"))  # 5 pairs -> last 10 msgs
    temperature: float = float(os.getenv("TEMPERATURE", "0.5"))
    length_policy: str = os.getenv("LENGTH_POLICY", "auto")
    min_paragraphs: int = int(os.getenv("MIN_PARAGRAPHS", "1"))
    max_paragraphs: int = int(os.getenv("MAX_PARAGRAPHS", "5"))

settings = Settings()
