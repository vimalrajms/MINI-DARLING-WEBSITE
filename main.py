import os
import time
import uuid
from collections import deque
from threading import Lock

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="MINI DARLING API",
    description="Backend for the MINI DARLING ESP32 OLED robot",
    version="1.0.0",
)

WEBSITE_ORIGIN = os.getenv("WEBSITE_ORIGIN", "https://mini-darling-web.vercel.app").rstrip("/")
DEVICE_TOKEN = os.getenv("DEVICE_TOKEN", "").strip()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        WEBSITE_ORIGIN,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Device-Token"],
)

message_queue = deque(maxlen=100)
queue_lock = Lock()


class MessageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=200)


class DeviceReply(BaseModel):
    message_id: str = Field(min_length=1, max_length=100)
    reply: str = Field(min_length=1, max_length=200)


def make_reply(message: str) -> str:
    text = message.lower().strip()

    if any(word in text for word in ["hello", "hi", "hey", "vanakkam"]):
        return "Hello! Welcome to Darling!"

    if any(word in text for word in ["how are you", "epdi irukka", "eppadi irukka"]):
        return "Naan super! Nee epdi irukka?"

    if any(word in text for word in ["joke", "funny", "comedy", "jolly"]):
        return "Un smile than enakku battery!"

    if any(word in text for word in ["love", "darling"]):
        return "Darling is here! Stay happy!"

    if any(word in text for word in ["name", "who are you"]):
        return "Naan MINI DARLING!"

    if any(word in text for word in ["bye", "good night"]):
        return "Bye! Meet you again!"

    if any(word in text for word in ["thank", "thanks"]):
        return "You are welcome!"

    return "Message received! Darling is listening!"


def check_device_token(token: str | None) -> None:
    if not DEVICE_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="DEVICE_TOKEN is not configured on the server.",
        )

    if token != DEVICE_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid device token.",
        )


@app.get("/")
def home():
    return {
        "app": "MINI DARLING",
        "status": "online",
        "message": "Darling backend is ready!",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MINI DARLING API",
    }


@app.post("/api/message")
def send_message(request: MessageRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail='Message cannot be empty.')

    message_id = str(uuid.uuid4())
    reply = make_reply(text)
    item = {
        "message_id": message_id,
        "text": text,
        "reply": reply,
        "created_at": time.time(),
    }

    with queue_lock:
        if len(message_queue) >= message_queue.maxlen:
            raise HTTPException(
                status_code=503,
                detail="Message queue is full. Try again later.",
            )
        message_queue.append(item)

    return {
        "status": "queued",
        "message_id": message_id,
        "reply": reply,
        "message": "Message queued for the ESP32.",
    }


@app.get("/api/device/next")
def device_next(x_device_token: str | None = Header(default=None)):
    check_device_token(x_device_token)

    with queue_lock:
        if not message_queue:
            return {"status": "empty", "message": None}
        item = message_queue.popleft()

    return {"status": "message", "message": item}


@app.post("/api/device/reply")
def device_reply(
    request: DeviceReply,
    x_device_token: str | None = Header(default=None),
):
    check_device_token(x_device_token)
    return {
        "status": "received",
        "message_id": request.message_id,
        "reply": request.reply,
    }

