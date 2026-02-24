# SquakGPT

A simple FastAPI + HTMX web app with a ChatGPT-like interface for sentiment analysis.

## Setup

1. Install dependencies with uv:
```bash
uv sync
```

2. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your-api-key-here
```

## Run

```bash
uv run uvicorn app.main:app --reload
```

Open http://localhost:8000 in your browser.

## Architecture

- **FastAPI** - Backend API with streaming SSE responses
- **HTMX** - Frontend interactivity without JavaScript framework
- **Tailwind CSS** - Styling via CDN
- **SQLite** - Conversation history persistence
- **OpenAI API** - Sentiment analysis
