from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.services.chat_service import stream_chat

router = APIRouter()


@router.post("/stream")
async def chat_stream(body: ChatRequest):
    return StreamingResponse(
        stream_chat(body.message, body.corridor, [m.dict() for m in body.history]),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
