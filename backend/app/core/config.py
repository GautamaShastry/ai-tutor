from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    app_name: str = "Telugu AI Tutor"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/telugu_tutor"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Vector Database
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "telugu_content"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # LLM
    llm_provider: str = "gemini"  # gemini or ollama
    gemini_api_key: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    
    # OpenAI (for embeddings)
    openai_api_key: Optional[str] = None
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env


settings = Settings()
