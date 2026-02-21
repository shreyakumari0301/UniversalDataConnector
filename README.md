
# Universal Data Connector

## 🎯 Assignment Overview

Build a production-quality **Universal Data Connector** using FastAPI that provides a unified interface for an LLM to access different data sources through function calling. The connector must be intelligent enough to identify data types, apply business rules, and optimize responses for voice conversations where bandwidth and latency matter.

### Business Context
You're building this for a SaaS company where customers need to query their data (CRM, support tickets, analytics) through voice conversations with an AI assistant. The key constraints are:
- Voice conversations require quick, concise responses (not massive data dumps)
- Data must be contextually relevant and filtered
- The LLM needs metadata to understand how to use each data source
- Multiple data sources should have a consistent interface

---

## 📋 Requirements

### Core Functionality
1. **FastAPI Server** with health checks and proper error handling
2. **Multiple Data Connectors** (at least 3 types):
   - Customer CRM data
   - Support ticket system
   - Analytics/metrics data
3. **Intelligent Data Filtering**:
   - Automatic pagination for large datasets
   - Business rules engine to filter data appropriately
   - Smart summarization for voice contexts
4. **LLM Function Calling Interface**:
   - OpenAPI schema generation for function calling
   - Clear parameter validation
   - Structured responses with metadata
5. **Data Type Detection & Handling**:
   - Identify whether data is tabular, time-series, hierarchical, etc.
   - Apply appropriate transformations
   - Include data freshness/staleness indicators

### Technical Requirements
- Python 3.11+
- FastAPI with Pydantic v2 models
- Proper logging and error handling
- Type hints throughout
- Configuration management (environment variables)
- Mock data generators included
- Docker deployment ready

### Voice-Optimized Business Rules
Implement rules like:
- **Limit results**: Default max 10 items for voice
- **Prioritization**: Return most recent/relevant first
- **Summarization**: Aggregate metrics instead of raw data when appropriate
- **Context awareness**: Include helpful metadata (e.g., "showing 3 of 47 results")
- **Freshness indicators**: "Data as of 2 hours ago"

---

## 🏗️ Architecture

```
universal-data-connector/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── common.py           # Shared models
│   │   ├── crm.py              # CRM data models
│   │   ├── support.py          # Support ticket models
│   │   └── analytics.py        # Analytics models
│   ├── connectors/
│   │   ├── __init__.py
│   │   ├── base.py             # Base connector interface
│   │   ├── crm_connector.py    # CRM data connector
│   │   ├── support_connector.py
│   │   └── analytics_connector.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_identifier.py  # Identifies data types
│   │   ├── business_rules.py   # Business rules engine
│   │   └── voice_optimizer.py  # Voice-specific optimizations
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── data.py             # Data access endpoints
│   └── utils/
│       ├── __init__.py
│       ├── mock_data.py        # Mock data generators
│       └── logging.py          # Logging configuration
├── tests/
│   ├── __init__.py
│   ├── test_connectors.py
│   ├── test_business_rules.py
│   └── test_api.py
├── data/
│   ├── customers.json          # Sample CRM data
│   ├── support_tickets.json    # Sample support data
│   └── analytics.json          # Sample metrics
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🎓 Learning Objectives

By completing this exercise, you will demonstrate:
1. **API Design**: Creating clean, RESTful APIs with FastAPI
2. **Type Safety**: Using Pydantic models and Python type hints
3. **Abstraction**: Building reusable base classes and interfaces
4. **Business Logic**: Implementing smart filtering and rules
5. **LLM Integration**: Understanding function calling patterns
6. **Production Readiness**: Logging, error handling, configuration
7. **Voice UX Considerations**: Optimizing for conversational AI

---

## ✅ Evaluation Criteria

### Code Quality (30%)
- Clean, readable code with proper structure
- Type hints and Pydantic models used correctly
- Comprehensive error handling
- Logging throughout

### Functionality (30%)
- All endpoints working correctly
- Business rules properly implemented
- Data filtering and optimization working
- Mock data realistic and useful

### LLM Integration (20%)
- OpenAPI schema properly generated
- Function calling examples work
- Responses optimized for voice
- Good parameter validation

### Documentation (20%)
- Clear README with setup instructions
- Inline code comments where needed
- API documentation (auto-generated + custom)
- Example usage scenarios

---

## 🚀 Getting Started

### Phase 1: Setup (Day 1)
1. Set up project structure
2. Create base models and connector interface
3. Implement mock data generators
4. Get FastAPI running with health check

### Phase 2: Core Connectors (Days 2-3)
1. Implement CRM connector
2. Implement support ticket connector
3. Implement analytics connector
4. Add data type identification

### Phase 3: Business Rules (Day 4)
1. Build business rules engine
2. Implement voice optimizations
3. Add pagination and filtering
4. Test with sample queries

### Phase 4: LLM Integration (Day 5)
1. Create function calling schemas
2. Test with LLM (Claude or OpenAI)
3. Optimize response formats
4. Add metadata and context

### Phase 5: Polish (Day 6)
1. Add comprehensive logging
2. Write tests
3. Create Docker setup
4. Write documentation

---

## 📝 Submission Requirements

1. **GitHub Repository** with:
   - All source code
   - README with setup instructions
   - Sample .env file
   - Working Docker Compose setup

2. **Demo Video** (5 minutes max):
   - Show the API running
   - Demonstrate 3-4 example queries
   - Show LLM function calling integration
   - Explain one interesting technical decision

3. **Written Summary** (1 page):
   - Challenges faced and solutions
   - Design decisions and tradeoffs
   - What you'd improve with more time
   - What you learned

---

## 💡 Tips for Success

1. **Start Simple**: Get one connector working end-to-end before adding complexity
2. **Use Type Hints**: Let your IDE help you catch bugs early
3. **Test as You Go**: Don't wait until the end to test
4. **Think About the User**: Would this response make sense in a voice conversation?
5. **Document Your Thinking**: Add comments explaining "why" not just "what"
6. **Ask Questions**: If requirements are unclear, make reasonable assumptions and document them

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Tool Use Documentation](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

---

## 🎉 Bonus Challenges (Optional)

If you finish early and want to go further:
1. Add caching layer (Redis) for frequently accessed data
2. Implement rate limiting per data source
3. Add streaming responses for large datasets
4. Create a web UI to test the API
5. Add authentication and API key management
6. Implement webhook support for real-time data updates
7. Add data export functionality (CSV, Excel)

Good luck! We're excited to see what you build. 🚀

## Setup

```bash
python -m venv venv
# Windows: venv\Scripts\activate  |  Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional: edit HOST, PORT, MAX_RESULTS
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

(Optional: `--host 0.0.0.0 --port 8000` for network access.)

### Mock data generators

To regenerate sample data in `data/`:

```bash
python -m app.utils.mock_data
```

Creates/overwrites `data/customers.json`, `data/support_tickets.json`, and `data/analytics.json`.

## Docker

```bash
docker-compose up --build
```

Visit: http://localhost:8000/docs

### Voice assistant demo (browser, STT + Chat + TTS)

1. Set `OPENAI_API_KEY` in `.env` (required for the chat endpoint).
2. Start the API: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Open `demo.html` in Chrome or Edge (or run `python -m http.server 8080` and open http://localhost:8080/demo.html). **Or** run `./start_demo.sh` to start uvicorn + file server and open the demo in your browser.
4. Select your **company** (tenant), then **verify**: say or type “I am &lt;name&gt; from &lt;company_id&gt;” (e.g. “I am acme from acme_corp”). Only after verification can you ask questions. Only your company’s data is returned; questions about other companies are refused by the assistant.
5. Click **Speak** or type a question and click **Ask**. The page sends to **POST /chat**; the reply is spoken aloud (TTS). Full loop: **STT → /chat (OpenAI + tools) → TTS**.

## API examples

```bash
# CRM: top customers (max 10), optional filter by customer_id and period
curl "http://localhost:8000/data/crm/customers?top=3"
curl "http://localhost:8000/data/crm/customers?customer_id=acme_corp&period=month"

# Support tickets: filter by customer_id, status, priority
curl "http://localhost:8000/data/support/tickets?customer_id=acme_corp&status=open"
curl "http://localhost:8000/data/support/tickets?priority=high&limit=5"

# Analytics: metrics with optional date range and customer filter
curl "http://localhost:8000/data/analytics/metrics?customer_id=acme_corp&from=2026-02-01&to=2026-02-18"

# Health
curl "http://localhost:8000/health"

# Chat (uses OpenAI + your data as tools; requires OPENAI_API_KEY in .env)
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"message\": \"Who are my top 3 customers by revenue?\"}"
```

### Authentication / company selection

Data is scoped by **company (tenant)** so each client only sees their own data.

- **Without API keys (default):** send header **`X-Company-ID`** to choose which company you are. All data (CRM, support, analytics) is filtered by that company.
  - Example: `X-Company-ID: acme_corp` or `beta_inc`, `gamma_ltd`, `delta_co`, `epsilon_llc`
  - If omitted, defaults to `acme_corp`.
- **With API keys:** set in `.env`: `API_KEYS_JSON='{"key_acme":"acme_corp","key_beta":"beta_inc"}'`. Then send **`X-API-Key: key_acme`**; the key maps to the company. Invalid or missing key returns 401.

```bash
# Scope to beta_inc (no auth)
curl -H "X-Company-ID: beta_inc" "http://localhost:8000/data/crm/customers?top=3"

# With API key auth (after setting API_KEYS_JSON in .env)
curl -H "X-API-Key: key_acme" "http://localhost:8000/data/support/tickets?status=open"
```

---

## LLM integration (function calling)

The API exposes tool schemas for OpenAI and Anthropic so an LLM can call data endpoints via function/tool use.

### 1. Fetch tool definitions

```bash
# OpenAI (Chat Completions "tools" parameter)
curl "http://localhost:8000/llm/tools?format=openai"

# Anthropic (Claude tool definitions)
curl "http://localhost:8000/llm/tools?format=anthropic"
```

### 2. Map tool names to API calls

When the LLM returns a tool call (e.g. `get_crm_customers` with `{"top": 3}`), call the corresponding endpoint:

| Tool name              | API call                                      |
|------------------------|-----------------------------------------------|
| `get_crm_customers`    | `GET /data/crm/customers?top=3`               |
| `get_support_tickets`  | `GET /data/support/tickets?status=open`      |
| `get_analytics_metrics`| `GET /data/analytics/metrics?from=...&to=...`|

Helper: `GET /llm/tools/endpoints` returns this mapping.

### 3. Example flow (OpenAI)

1. Get tools: `GET /llm/tools?format=openai` → use `response.tools` in `chat.completions.create(tools=...)`.
2. User says: "Who are my top 3 customers by revenue?"
3. LLM returns a tool call: `get_crm_customers(top=3)`.
4. Your server calls: `GET {BASE_URL}/data/crm/customers?top=3`.
5. Pass the JSON response back to the LLM as the tool result; the LLM replies in natural language (e.g. for voice).

### 4. Voice-optimized responses

- **Limit**: CRM and support default to max 10 items; analytics can return a summary when there are many points.
- **Metadata**: Every response includes `metadata.total_results`, `metadata.returned_results`, and `metadata.data_freshness` so the LLM can say e.g. "Showing 3 of 47 customers; data as of 2 hours ago."
- **Summaries**: Analytics with many data points return a single summary object (total, avg, trend) suitable for spoken answers.
