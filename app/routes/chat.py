from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from app.models.conversation import Message, get_db
from app.services.classifier import classify_statement
from app.services.bird_noises import stream_bird_response
from app.services.rate_limiter import rate_limiter

router = APIRouter()


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/chat")
async def chat(request: Request):
    client_ip = get_client_ip(request)
    rate_limiter.check_rate_limit(client_ip)

    form = await request.form()
    message = form.get("message", "")

    db = next(get_db())

    user_msg = Message(role="user", content=message)
    db.add(user_msg)
    db.commit()

    statement_type = classify_statement(message)

    async def generate():
        bird_response = ""
        async for char in stream_bird_response():
            bird_response += char
            yield f"data: {char}\n\n"

        assistant_msg = Message(
            role="assistant", content=bird_response, statement_type=statement_type
        )
        db.add(assistant_msg)
        db.commit()
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/history")
async def history():
    db = next(get_db())
    messages = db.query(Message).order_by(Message.created_at).all()

    html = ""
    for msg in messages:
        if msg.role == "user":
            html += f'<div class="flex justify-end mb-4"><div class="bg-blue-600 text-white rounded-lg px-4 py-2 max-w-md">{msg.content}</div></div>'
        else:
            html += f'<div class="flex justify-start mb-4"><div class="bg-gray-700 text-gray-100 rounded-lg px-4 py-2 max-w-md">{msg.content}</div></div>'

    return HTMLResponse(html)


@router.post("/clear")
async def clear_chat():
    db = next(get_db())
    db.query(Message).delete()
    db.commit()
    return HTMLResponse("")
