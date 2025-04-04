from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv
from logger import app_logger
import json
from pydantic import field_validator

load_dotenv()

app_logger.debug(f"Current working directory: {os.getcwd()}")
app_logger.debug(f"API_KEY from environment: {os.getenv('API_KEY')}")
app_logger.debug(f"API_KEY_HEADER from environment: {os.getenv('API_KEY_HEADER')}")
app_logger.debug(f"CORS_ORIGINS from environment: {os.getenv('CORS_ORIGINS')}")

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEVELOPMENT_MODE: bool = ENVIRONMENT == "development"
    
    API_KEY: str = os.getenv("API_KEY", "")
    API_KEY_HEADER: str = "X-API-Key"
    
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    
    MAX_REQUEST_SIZE: int = int(os.getenv("MAX_REQUEST_SIZE", "1048576"))  # 1MB default
    MAX_QUESTION_LENGTH: int = int(os.getenv("MAX_QUESTION_LENGTH", "500"))
    
    RATE_LIMIT_GENERATE: str = os.getenv("RATE_LIMIT_GENERATE", "3/minute")
    RATE_LIMIT_CHAT: str = os.getenv("RATE_LIMIT_CHAT", "3/minute")
    RATE_LIMIT_HEALTH: str = os.getenv("RATE_LIMIT_HEALTH", "30/minute")
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")

    @field_validator("CORS_ORIGINS")
    def parse_cors_origins(cls, v: str) -> List[str]:
        """Parse CORS origins from string."""
        if not v:
            return ["http://localhost:5173"]
        
        try:
            v = v.strip().strip('"').strip("'")
            
            if v.startswith('[') and v.endswith(']'):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [str(origin).strip() for origin in parsed if origin]
                    app_logger.warning("CORS_ORIGINS JSON is not a list, falling back to comma-separated parsing")
                except json.JSONDecodeError:
                    app_logger.warning("Failed to parse CORS_ORIGINS as JSON, falling back to comma-separated parsing")
            
            origins = [origin.strip() for origin in v.split(',')]
            origins = [origin for origin in origins if origin]
            
            if not origins:
                app_logger.warning("No valid origins found in CORS_ORIGINS, using default")
                return ["http://localhost:5173"]
                
            return origins
            
        except Exception as e:
            app_logger.error(f"Error parsing CORS_ORIGINS: {str(e)}")
            app_logger.info("Using default CORS_ORIGINS due to parsing error")
            return ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore" 

try:
    settings = Settings()
    app_logger.info(f"Settings loaded successfully. Environment: {settings.ENVIRONMENT}")
    app_logger.debug(f"Settings API_KEY: {settings.API_KEY}")
    app_logger.debug(f"Settings API_KEY_HEADER: {settings.API_KEY_HEADER}")
    app_logger.debug(f"Settings CORS_ORIGINS: {settings.CORS_ORIGINS}")
    app_logger.debug(f"Development Mode: {settings.DEVELOPMENT_MODE}")
except Exception as e:
    app_logger.error(f"Error creating Settings instance: {str(e)}")
    raise 