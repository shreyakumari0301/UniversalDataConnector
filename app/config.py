import json
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_api_keys(v: Optional[str]) -> dict:
    if not v:
        return {}
    try:
        return json.loads(v)
    except json.JSONDecodeError:
        return {}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    APP_NAME: str = "Universal Data Connector"
    MAX_RESULTS: int = 10
    OPENAI_API_KEY: Optional[str] = None
    # API key -> company_id (tenant). Example: {"key_acme":"acme_corp","key_beta":"beta_inc"}
    # Set via env: API_KEYS_JSON='{"key_acme":"acme_corp"}'
    API_KEYS_JSON: Optional[str] = None

    @property
    def API_KEYS(self) -> dict:
        """When set (via API_KEYS_JSON), auth is required. Otherwise no auth, company defaults to acme_corp."""
        return _parse_api_keys(self.API_KEYS_JSON) if self.API_KEYS_JSON else {}


settings = Settings()
