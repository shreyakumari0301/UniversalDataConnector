from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    APP_NAME: str = "Universal Data Connector"
    MAX_RESULTS: int = 10

settings = Settings()
