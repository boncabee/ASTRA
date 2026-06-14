from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ASTRA"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./astra.db"
    
    # JWT Authentication
    JWT_SECRET_KEY: str = "supersecretkey_please_override_in_env"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Correlation Engine Constants
    CORRELATION_SCORE_MULTIPLIER: int = 5
    CORRELATION_SCORE_MAX: int = 100
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
