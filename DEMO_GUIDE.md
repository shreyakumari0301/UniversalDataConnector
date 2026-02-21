# 5–6 Minute Demo Guide

## 1. Minutes 0–2: Data flow (diagram)

Draw this on a whiteboard or in Excalidraw.

**High-level flow**

```
[User / Voice UI]  →  [Your app or LLM]  →  [This API]  →  [Connectors]  →  [Data files]
                              ↑                    ↓
                         Tool schemas          Business rules
                         (/llm/tools)          + voice optimizer
```

**Step-by-step (what to label in the diagram)**

1. **User** – Speaks or types a query (e.g. “Top 3 customers”).
2. **Client / LLM layer** – Gets tool definitions from `GET /llm/tools`, sends user message to OpenAI/Claude with those tools.
3. **LLM** – Returns a tool call, e.g. `get_crm_customers(top=3)`.
4. **Client** – Calls **this API**: `GET /data/crm/customers?top=3`.
5. **This API** – **Router** → **Business rules** (limit, sort, period filter) → **Connector** (CRM/Support/Analytics) → reads **JSON data**.
6. **Response** – `{ data: [...], metadata: { total_results, returned_results, data_freshness } }` back to client.
7. **Client** – Passes JSON to LLM; LLM speaks the answer (or your app does TTS).

**Three data paths to show**

- **CRM**: `customers.json` → CRM connector → business rules (revenue sort, period, max 10) → response.
- **Support**: `support_tickets.json` → Support connector → business rules (created_at sort, limit) → response.
- **Analytics**: `analytics.json` → Analytics connector → business rules + voice optimizer (summary if >5 points) → response.

---

## 2. Minutes 2–4: Run and demonstrate

**Before starting**

- Terminal 1: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- `.env` must include `OPENAI_API_KEY` for the chat and voice assistant.
- Optional: open `demo.html` in Chrome for the full voice assistant (STT → /chat → TTS).

**Demo script (about 2 minutes)**

| Time   | Action | What to say |
|--------|--------|-------------|
| 0:00   | Open http://localhost:8000/docs | “This is the unified API: one place for CRM, support, and analytics.” |
| 0:15   | `GET /health` → Execute | “Health check; API is up.” |
| 0:25   | `GET /data/crm/customers` → top=3 → Execute | “Top 3 customers by revenue. Response has data plus metadata: total vs returned, freshness.” |
| 0:45   | `GET /data/support/tickets` → customer_id=acme_corp, status=open → Execute | “Support tickets for one customer, open only. Same response shape.” |
| 1:05   | `POST /chat` → body `{"message": "Who are my top 3 customers?"}` → Execute | “Chat uses OpenAI with our data as tools; reply is concise for voice.” |
| 1:25   | Optional: demo.html, click Speak | “Voice assistant: I speak (STT), browser sends to POST /chat, server uses OpenAI + data tools, reply spoken aloud (TTS).” |

**Voice assistant (STT + Chat + TTS)**

- **demo.html** in Chrome/Edge: click **Speak**, ask e.g. “Who are my top 3 customers?” or “Any open tickets for acme?”
- Flow: **Speech recognition (STT)** → transcript to **POST /chat** → backend uses OpenAI + our data tools → short reply → **SpeechSynthesis (TTS)** reads it aloud.
- Requires `OPENAI_API_KEY` in `.env`. CORS is enabled so the page can call the API.

**One-liner**

“One API, three data sources, shared response format and metadata, plus tool schemas so an LLM can query it safely and we keep answers short for voice.”

---

## 3. Minutes 4–6: Scalability – “Would this support 10,000 users?”

**Short answer:** As-is, **no**. For “10,000 users” (high concurrency or total load), you need a few targeted changes.

**Current limits**

| Area | Current | Why it doesn’t scale to 10k |
|------|--------|----------------------------|
| **Data** | JSON files read on every request | Disk I/O and parsing on each call; no indexing, no connection pooling. |
| **Process** | Single uvicorn process | One CPU bound; no horizontal scaling. |
| **State** | No cache | Same data re-read for identical queries. |
| **Concurrency** | Default async but file I/O is blocking | Under load, file reads block the event loop. |
| **Deployment** | One container / one host | No load spreading, single point of failure. |

**What “10,000 users” usually means**

- Either **10k registered users** with low concurrency → current design might survive with small tweaks (e.g. more workers, caching).
- Or **high concurrency** (hundreds of simultaneous requests) or **high QPS** → need the changes below.

**Specific changes to support scale**

1. **Move off JSON files**
   - Use a **database** (e.g. PostgreSQL) for CRM, support, analytics.
   - Connectors query the DB (with connection pooling, e.g. asyncpg or SQLAlchemy).
   - Enables indexing, filtering, and concurrent reads without re-parsing files.

2. **Cache hot data**
   - Put a **Redis** (or similar) cache in front of read-heavy endpoints.
   - Cache key = e.g. `crm:customers:top=3`; TTL 1–5 minutes.
   - Reduces DB and CPU load for repeated “top customers” / “open tickets” queries.

3. **Multiple workers / instances**
   - Run **multiple uvicorn workers**: `uvicorn app.main:app --workers 4` (or use Gunicorn + Uvicorn).
   - Or run **multiple containers** behind a **load balancer** (e.g. Nginx, or Kubernetes Ingress).
   - So one process isn’t the bottleneck.

4. **Non-blocking I/O**
   - Ensure all I/O is async: **async DB driver**, **async Redis**, no blocking file reads in request path.
   - If you keep files temporarily, read them in a thread pool so the event loop isn’t blocked.

5. **Rate limiting and protection**
   - Add **rate limiting** (e.g. per API key or per IP) so one client can’t overwhelm the API.
   - Use **timeouts** and **connection limits** so one slow client doesn’t tie up workers.

6. **Observability**
   - **Logging** (already in place) + **metrics** (e.g. Prometheus) + **tracing** (e.g. OpenTelemetry).
   - So you can see which endpoints and connectors are slow under load.

**Summary for the talk**

“Out of the box this is a single-service, file-backed API, so it won’t support 10,000 users at high concurrency. To get there we’d add: a database and connection pooling, Redis cache for hot reads, multiple workers or replicas behind a load balancer, and full async I/O. Rate limiting and metrics would complete the picture for production.”
