"""
Chat with OpenAI using our data API as tools.
Executes tool calls in-process (connectors + business_rules).
"""
import json
import logging
from typing import Any, Optional

from app.config import settings
from app.schemas.llm_tools import OPENAI_TOOLS
from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.connectors.analytics_connector import AnalyticsConnector
from app.services.business_rules import apply_rules

logger = logging.getLogger(__name__)

def _system_message(company_id: Optional[str] = None) -> str:
    base = (
        "You are a helpful voice assistant with access to the company's data. "
        "When the user asks about customers, support tickets, or analytics, use the provided tools. "
        "Keep answers concise and suitable for voice (short sentences, key numbers)."
    )
    if company_id:
        base += (
            f" The user is verified for company {company_id} only. "
            "Only use data for this company. If they ask about another company's data (e.g. beta_inc, gamma_ltd), "
            f"politely say you can only provide information for their own company ({company_id})."
        )
    return base


def execute_tool(name: str, arguments: dict, company_id: Optional[str] = None) -> str:
    """Run the named tool with given args; company_id scopes data to that tenant."""
    args = arguments or {}
    cid = company_id or args.get("customer_id")
    try:
        if name == "get_crm_customers":
            raw = CRMConnector().get_data({"customer_id": None, "top": None, "period": "all"})
            params = {"customer_id": args.get("customer_id") or cid, "top": args.get("top", 10), "period": args.get("period", "all")}
            response = apply_rules("crm", raw, params)
        elif name == "get_support_tickets":
            raw = SupportConnector().get_data({
                "customer_id": args.get("customer_id") or cid,
                "status": args.get("status"),
                "priority": args.get("priority"),
            })
            response = apply_rules("support", raw, {"limit": args.get("limit", 10)})
        elif name == "get_analytics_metrics":
            raw = AnalyticsConnector().get_data({
                "customer_id": args.get("customer_id") or cid,
                "from": args.get("from"),
                "to": args.get("to"),
                "limit": args.get("limit", 100),
            })
            response = apply_rules("analytics", raw, {"limit": args.get("limit", 100)})
        else:
            return json.dumps({"error": f"Unknown tool: {name}"})
        return response.model_dump_json()
    except Exception as e:
        logger.exception("Tool %s failed: %s", name, e)
        return json.dumps({"error": str(e)})


def run_chat(user_message: str, company_id: Optional[str] = None) -> str:
    """
    Send user message to OpenAI with our tools; execute any tool calls and loop until done.
    Returns the final assistant reply text.
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in .env")

    from openai import OpenAI

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    messages = [
        {"role": "system", "content": _system_message(company_id)},
        {"role": "user", "content": user_message},
    ]
    max_rounds = 5
    for _ in range(max_rounds):
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=OPENAI_TOOLS,
            tool_choice="auto",
        )
        choice = resp.choices[0]
        msg = choice.message
        if not msg.tool_calls:
            return (msg.content or "").strip()
        messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": [{"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in msg.tool_calls]})
        for tc in msg.tool_calls:
            name = tc.function.name
            try:
                arguments = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                arguments = {}
            result = execute_tool(name, arguments, company_id=company_id)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
    return "I hit the reply limit. Please try a shorter question."
