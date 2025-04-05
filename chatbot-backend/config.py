from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv
from logger import app_logger
import json
from pydantic import field_validator, Field

# Load environment variables
load_dotenv()

# Debug logging for environment variables
app_logger.debug("Current working directory: %s", os.getcwd())
app_logger.debug("Environment variables:")
for key in ['OPENAI_API_KEY', 'API_KEY']:
    value = os.getenv(key)
    app_logger.debug(f"{key}: {'***MASKED***' if value else 'Not set'}")

class Settings(BaseSettings):
    API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    API_KEY_HEADER: str = "X-API-Key"
    
    CORS_ORIGINS: str = "http://localhost:5173"
    
    MAX_REQUEST_SIZE: int = 1024 * 1024  # 1MB
    MAX_QUESTION_LENGTH: int = 1000
    
    RATE_LIMIT_GENERATE: str = "10/minute"
    RATE_LIMIT_CHAT: str = "30/minute"
    RATE_LIMIT_HEALTH: str = "60/minute"

    DEVELOPMENT_MODE: bool = True

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

    @field_validator("RATE_LIMIT_GENERATE", "RATE_LIMIT_CHAT", "RATE_LIMIT_HEALTH")
    def parse_rate_limit(cls, v: str) -> str:
        """Parse rate limit string to ensure it's in the correct format."""
        if not v:
            return "10/minute"
        
        try:
            v = v.strip()
            parts = v.split('/')
            if len(parts) != 2:
                app_logger.warning(f"Invalid rate limit format: {v}, using default")
                return "10/minute"
            try:
                int(parts[0])
            except ValueError:
                app_logger.warning(f"Invalid number in rate limit: {v}, using default")
                return "10/minute"
            if parts[1].lower() not in ['second', 'minute', 'hour', 'day']:
                app_logger.warning(f"Invalid unit in rate limit: {v}, using default")
                return "10/minute"
            return v
            
        except Exception as e:
            app_logger.error(f"Error parsing rate limit: {str(e)}")
            app_logger.info("Using default rate limit due to parsing error")
            return "10/minute"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app_logger.debug(f"CORS_ORIGINS: {self.CORS_ORIGINS}")
        app_logger.debug(f"MAX_REQUEST_SIZE: {self.MAX_REQUEST_SIZE}")
        app_logger.debug(f"MAX_QUESTION_LENGTH: {self.MAX_QUESTION_LENGTH}")
        app_logger.debug(f"RATE_LIMIT_GENERATE: {self.RATE_LIMIT_GENERATE}")
        app_logger.debug(f"RATE_LIMIT_CHAT: {self.RATE_LIMIT_CHAT}")
        app_logger.debug(f"RATE_LIMIT_HEALTH: {self.RATE_LIMIT_HEALTH}")
        app_logger.debug(f"DEVELOPMENT_MODE: {self.DEVELOPMENT_MODE}")
        # sensitive information
        app_logger.debug("API_KEY: ***MASKED***")
        app_logger.debug(f"API_KEY_HEADER: {self.API_KEY_HEADER}")

try:
    settings = Settings()
    app_logger.info("Settings loaded successfully")
    app_logger.debug(f"Settings API_KEY: {settings.API_KEY}")
    app_logger.debug(f"Settings API_KEY_HEADER: {settings.API_KEY_HEADER}")
    app_logger.debug(f"Settings CORS_ORIGINS: {settings.CORS_ORIGINS}")
except Exception as e:
    app_logger.error(f"Error creating Settings instance: {str(e)}")
    raise 