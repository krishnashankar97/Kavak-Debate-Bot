from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse
from app.routers.chat import router as chat_router
import pathlib

app = FastAPI(
    title="DebateBot API",
    version="1.1.0",
    description="A chatbot API that debates a chosen side and persuades the opponent."
)

# CORS (allow local file/other ports during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static UI
ROOT = pathlib.Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(ROOT / "index.html")

app.include_router(chat_router)

@app.get("/health")
def health():
    return {"ok": True}
