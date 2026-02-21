from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, data, llm, chat
from app.utils.logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Universal Data Connector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__},
    )


@app.get("/", response_class=HTMLResponse)
def root():
    """Landing page with links to docs, health, chat, and demo."""
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>Universal Data Connector</title></head>
    <body style="font-family: system-ui; max-width: 560px; margin: 2rem auto; padding: 0 1rem;">
    <h1>Universal Data Connector</h1>
    <p>One API for CRM, support tickets, and analytics. Voice-optimized responses and LLM tool definitions.</p>
    <ul>
    <li><a href="/docs">API docs (Swagger)</a></li>
    <li><a href="/health">Health check</a></li>
    <li><a href="/llm/tools?format=openai">LLM tools (OpenAI)</a></li>
    <li>Chat: <code>POST /chat</code> with <code>{"message": "..."}</code></li>
    <li>Voice demo: <a href="http://localhost:8080/demo.html">http://localhost:8080/demo.html</a> (run <code>./start_demo.sh</code> first)</li>
    <li><strong>Company (tenant):</strong> send <code>X-Company-ID: acme_corp</code> or <code>beta_inc</code>, <code>gamma_ltd</code>, etc. to scope data. Or set <code>API_KEYS_JSON</code> in .env and use <code>X-API-Key</code>.</li>
    </ul>
    </body>
    </html>
    """


app.include_router(health.router)
app.include_router(data.router)
app.include_router(llm.router)
app.include_router(chat.router)
