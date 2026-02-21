"""
Authentication: select which company (tenant) you are.
- With auth (API_KEYS_JSON set in .env): send X-API-Key; key maps to company_id.
- Without auth: optionally send X-Company-ID: acme_corp | beta_inc | gamma_ltd | ... to scope data.
"""
import logging
from typing import Optional

from fastapi import Header, HTTPException

from app.config import settings

logger = logging.getLogger(__name__)

ALLOWED_COMPANIES = ("acme_corp", "beta_inc", "gamma_ltd", "delta_co", "epsilon_llc")


def get_company_id(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    x_company_id: Optional[str] = Header(None, alias="X-Company-ID"),
) -> str:
    """
    Resolve to company_id (tenant). Data is scoped to this company.
    - If API_KEYS_JSON is set: X-API-Key required; key -> company_id.
    - Else: optional X-Company-ID to pick company (default acme_corp).
    """
    api_keys = getattr(settings, "API_KEYS", None) or {}
    if api_keys:
        if not x_api_key:
            raise HTTPException(
                status_code=401,
                detail="Missing X-API-Key. Use a valid key to select your company.",
            )
        company_id = api_keys.get(x_api_key)
        if not company_id:
            raise HTTPException(status_code=401, detail="Invalid API key.")
        return company_id
    if x_company_id and x_company_id in ALLOWED_COMPANIES:
        return x_company_id
    return "acme_corp"
