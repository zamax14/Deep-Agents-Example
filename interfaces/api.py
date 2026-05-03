from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent.chat import process_stream_async

app = FastAPI(title="Deep Agent API", version="1.0.0")

# In-memory session store: session_id -> message history
_sessions: dict[str, list] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """Send a message and get a reply from the deep agent."""
    messages = _sessions.get(req.session_id, [])
    messages.append({"role": "user", "content": req.message})

    try:
        updated_messages, final_text = await process_stream_async(messages)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    _sessions[req.session_id] = updated_messages
    return ChatResponse(reply=final_text, session_id=req.session_id)


@app.delete("/chat/{session_id}")
async def clear_session(session_id: str) -> dict:
    """Clear the message history for a session."""
    _sessions.pop(session_id, None)
    return {"cleared": session_id}


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
