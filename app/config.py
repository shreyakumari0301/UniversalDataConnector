from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    APP_NAME: str = "Universal Data Connector"
    MAX_RESULTS: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
