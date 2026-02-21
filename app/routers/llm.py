from fastapi import APIRouter, Query
from typing import Literal

from app.schemas.llm_tools import OPENAI_TOOLS, ANTHROPIC_TOOLS, TOOL_TO_ENDPOINT

router = APIRouter(prefix="/llm", tags=["LLM"])


@router.get("/tools")
def get_llm_tools(
    format: Literal["openai", "anthropic"] = Query(
        "openai",
        description="Tool schema format: openai (OpenAI API) or anthropic (Claude)",
    ),
):
    """
    Return function-calling tool definitions for LLM APIs.
    - OpenAI: use response as `tools` in Chat Completions.
    - Anthropic: use each item as a tool with `name`, `description`, `input_schema`.
    """
    if format == "anthropic":
        return {"tools": ANTHROPIC_TOOLS}
    return {"tools": OPENAI_TOOLS}


@router.get("/tools/endpoints")
def get_tool_endpoints():
    """Return mapping of tool names to API method and path (for building requests)."""
    return {"tool_endpoints": TOOL_TO_ENDPOINT}
