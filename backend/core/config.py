from typing import List
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ASTRA"
    ENVIRONMENT: str = "dev"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/astra"
    TEST_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/astra_test"
    
    # JWT Authentication
    JWT_SECRET_KEY: str = "supersecretkey_please_override_in_env"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Correlation Engine Constants
    CORRELATION_SCORE_MULTIPLIER: int = 5
    CORRELATION_SCORE_MAX: int = 100
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.ENVIRONMENT == "prod":
            if self.JWT_SECRET_KEY == "supersecretkey_please_override_in_env":
                raise ValueError("Insecure default JWT_SECRET_KEY is not allowed in production.")
            if "postgres:postgres@localhost" in self.DATABASE_URL or "postgres:postgres@db" in self.DATABASE_URL:
                raise ValueError("Insecure default DATABASE_URL is not allowed in production.")
        return self

settings = Settings()
