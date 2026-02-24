from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.models.conversation import init_db
from app.routes import chat

app = FastAPI(title="SquakGPT")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(chat.router)


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
