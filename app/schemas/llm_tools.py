"""
Function-calling tool definitions for LLMs (OpenAI and Anthropic).
Use these with the API base URL: GET /llm/tools?format=openai|anthropic
"""

OPENAI_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_crm_customers",
            "description": "Get top customers by revenue. Use for questions about customers, revenue, or orders. Results are sorted by revenue descending and limited for voice.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Filter by customer ID, e.g. acme_corp, beta_inc, gamma_ltd",
                    },
                    "top": {
                        "type": "integer",
                        "description": "Number of top customers to return (max 10)",
                        "default": 10,
                    },
                    "period": {
                        "type": "string",
                        "enum": ["all", "week", "month"],
                        "description": "Filter by last order period: week (7 days), month (30 days), or all",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_support_tickets",
            "description": "Get support tickets. Use for open/closed tickets, priority, or per-customer tickets. Sorted by most recent first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Filter by customer ID",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["open", "closed"],
                        "description": "Filter by ticket status",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["high", "low"],
                        "description": "Filter by priority",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max tickets to return (default 10)",
                        "default": 10,
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_analytics_metrics",
            "description": "Get analytics metrics (revenue, orders) over time. Use for trends, totals, or time-range queries. Returns summary for voice when many points.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Filter by customer ID",
                    },
                    "from": {
                        "type": "string",
                        "description": "Start date ISO (e.g. 2026-02-01)",
                    },
                    "to": {
                        "type": "string",
                        "description": "End date ISO (e.g. 2026-02-18)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max data points (default 100)",
                        "default": 100,
                    },
                },
                "required": [],
            },
        },
    },
]

ANTHROPIC_TOOLS = [
    {
        "name": "get_crm_customers",
        "description": "Get top customers by revenue. Use for questions about customers, revenue, or orders. Results are sorted by revenue descending and limited for voice.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Filter by customer ID, e.g. acme_corp, beta_inc, gamma_ltd",
                },
                "top": {
                    "type": "integer",
                    "description": "Number of top customers to return (max 10)",
                    "default": 10,
                },
                "period": {
                    "type": "string",
                    "enum": ["all", "week", "month"],
                    "description": "Filter by last order period: week (7 days), month (30 days), or all",
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_support_tickets",
        "description": "Get support tickets. Use for open/closed tickets, priority, or per-customer tickets. Sorted by most recent first.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "Filter by customer ID"},
                "status": {
                    "type": "string",
                    "enum": ["open", "closed"],
                    "description": "Filter by ticket status",
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "low"],
                    "description": "Filter by priority",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max tickets to return (default 10)",
                    "default": 10,
                },
            },
            "required": [],
        },
    },
    {
        "name": "get_analytics_metrics",
        "description": "Get analytics metrics (revenue, orders) over time. Use for trends, totals, or time-range queries. Returns summary for voice when many points.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "Filter by customer ID"},
                "from": {
                    "type": "string",
                    "description": "Start date ISO (e.g. 2026-02-01)",
                },
                "to": {
                    "type": "string",
                    "description": "End date ISO (e.g. 2026-02-18)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max data points (default 100)",
                    "default": 100,
                },
            },
            "required": [],
        },
    },
]

TOOL_TO_ENDPOINT = {
    "get_crm_customers": {"method": "GET", "path": "/data/crm/customers"},
    "get_support_tickets": {"method": "GET", "path": "/data/support/tickets"},
    "get_analytics_metrics": {"method": "GET", "path": "/data/analytics/metrics"},
}
