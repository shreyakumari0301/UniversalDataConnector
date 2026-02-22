import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, data, llm, chat
from app.utils.logging import configure_logging
import logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Universal Data Connector")


@app.on_event("startup")
def startup_message():
    import sys
    msg = (
        "\n  >>> Open in browser: http://localhost:8000  (do not use 0.0.0.0) <<<\n"
        "  >>> Demo: http://localhost:8000/demo  |  To auto-open browser, run ./docker-start.sh on the host <<<\n"
    )
    logger.info(msg.strip())
    print(msg, file=sys.stderr, flush=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    <head><meta charset="utf-8"><title>Universal Data Connector</title>
    <script>if (window.location.hostname === '0.0.0.0') { window.location.replace('http://localhost:' + (window.location.port || '8000') + window.location.pathname + window.location.search); }</script>
    </head>
    <body style="font-family: system-ui; max-width: 560px; margin: 2rem auto; padding: 0 1rem;">
    <h1>Universal Data Connector</h1>
    <p>One API for CRM, support tickets, and analytics. Voice-optimized responses and LLM tool definitions.</p>
    <ul>
    <li><a href="/docs">API docs (Swagger)</a></li>
    <li><a href="/health">Health check</a></li>
    <li><a href="/llm/tools?format=openai">LLM tools (OpenAI)</a></li>
    <li>Chat: <code>POST /chat</code> with <code>{"message": "..."}</code></li>
    <li>Voice demo: <a href="/demo">/demo</a> (or run <code>./start_demo.sh</code> for local file server)</li>
    <li><strong>Company (tenant):</strong> send <code>X-Company-ID: acme_corp</code> or <code>beta_inc</code>, <code>gamma_ltd</code>, etc. to scope data. Or set <code>API_KEYS_JSON</code> in .env and use <code>X-API-Key</code>.</li>
    </ul>
    </body>
    </html>
    """


DEMO_HTML = os.path.join(os.path.dirname(__file__), "..", "demo.html")


@app.get("/demo", response_class=HTMLResponse)
def demo():
    """Serve the voice chat demo page (used by Docker)."""
    if os.path.isfile(DEMO_HTML):
        return FileResponse(DEMO_HTML, media_type="text/html")
    return HTMLResponse("<p>demo.html not found. Run from project root.</p>", status_code=404)


app.include_router(health.router)
app.include_router(data.router)
app.include_router(llm.router)
app.include_router(chat.router)
