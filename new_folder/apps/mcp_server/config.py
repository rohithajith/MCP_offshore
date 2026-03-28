import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Maritime Fleet & Cargo MCP Server"
    ENVIRONMENT: str = "local"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///offshore_logistics.db"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()
