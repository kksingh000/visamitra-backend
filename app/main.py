from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, visa, chat, tracker, health

app = FastAPI(
    title="VisaMitra API",
    description="AI-powered visa requirement navigator",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to Vercel domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(visa.router, prefix="/api/visa", tags=["visa"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(tracker.router, prefix="/api/tracker", tags=["tracker"])
