import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./yoruba_recipes.db"
    SECRET_KEY: str = "change-me"
    ALLOWED_ORIGINS: list[str] = ["*"]
    PROJECT_NAME: str = "Yoruba Recipes API"
    MAILERLITE_API_KEY: str = ""
    MAILERLITE_GROUP_ID: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()