"""
Application Configuration Settings
Loads settings from environment variables or .env file with production-ready defaults.
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agentic Layer for Fintech Operations in Hospitality Services"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # Database: Supports PostgreSQL (default local port 9876 or 5432) or SQLite fallback
    # If POSTGRES_URL is provided, it takes precedence. Otherwise falls back to sqlite:///./data/hospitality.db
    DATABASE_URL: str = Field(
        default="sqlite:///./data/hospitality.db",
        env="DATABASE_URL"
    )
    
    # Source Datasets Directory
    SOURCE_DATA_DIR: str = Field(
        default="./data/raw",
        env="SOURCE_DATA_DIR"
    )
    
    # Event Streaming (Kafka)
    KAFKA_BOOTSTRAP_SERVERS: str = Field(default="localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_ENABLED: bool = Field(default=False, env="KAFKA_ENABLED")
    
    # Vector DB (Qdrant)
    QDRANT_URL: str = Field(default="http://localhost:6333", env="QDRANT_URL")
    QDRANT_COLLECTION: str = Field(default="hospitality_knowledge", env="QDRANT_COLLECTION")
    QDRANT_ENABLED: bool = Field(default=False, env="QDRANT_ENABLED")
    
    # AI / LLM Configuration
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    LLM_MODEL: str = Field(default="gpt-4o-mini", env="LLM_MODEL")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-small", env="EMBEDDING_MODEL")
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
