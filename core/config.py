from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Union
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Forms Anyware API"
    DESCRIPTION: str = "API for managing approval flows and requisition forms"
    VERSION: str = "0.1.0"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["http://localhost:3000", "http://localhost:5000"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/hpha")
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret-key-change-this-in-production")
    JWT_SECRET_KEY: Optional[str] = None  # Add the field but set it to None by default
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT.lower() == "testing"
    
    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    @property
    def refresh_token_expires(self) -> timedelta:
        return timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
    
    @property
    def get_jwt_key(self) -> str:
        """Use JWT_SECRET_KEY if set, otherwise fall back to SECRET_KEY"""
        return self.JWT_SECRET_KEY or self.SECRET_KEY
    
    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore"  # This allows extra fields, but safer to define them
    }

# Create settings instance
settings = Settings()
