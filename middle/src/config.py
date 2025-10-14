from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BACKEND_URL: str
    API_KEY: str | None = None
    ENVIRONMENT: str = "development"

config = Config()
