from fastapi import Request, HTTPException, status
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import re
from config import settings
from logger import app_logger
import time

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        app_logger.debug(f"Processing request from IP: {request.client.host}")
        app_logger.debug(f"Request path: {request.url.path}")
        app_logger.debug(f"Request headers: {dict(request.headers)}")
        app_logger.debug(f"Expected API key header: {settings.API_KEY_HEADER}")
        app_logger.debug(f"API key present: {settings.API_KEY is not None and len(settings.API_KEY) > 0}")

        try:
            content_length = request.headers.get('content-length')
            if content_length and int(content_length) > settings.MAX_REQUEST_SIZE:
                app_logger.warning(f"Request size exceeded from IP: {request.client.host}")
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail={
                        "error": "Request too large",
                        "max_size": settings.MAX_REQUEST_SIZE,
                        "requested_size": int(content_length)
                    }
                )

            # Skip API key check for health endpoint
            if request.url.path == "/":
                app_logger.debug("Skipping API key check for health endpoint")
                response = await call_next(request)
                return response

            # Skip API key check for development mode
            if settings.DEVELOPMENT_MODE:
                app_logger.debug("Development mode: Skipping API key check")
                response = await call_next(request)
                return response

            # Check API key
            api_key = request.headers.get(settings.API_KEY_HEADER)
            if not api_key:
                app_logger.warning(f"Missing API key from IP: {request.client.host}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "error": "API key is required",
                        "header": settings.API_KEY_HEADER
                    }
                )
            
            if api_key != settings.API_KEY:
                app_logger.warning(f"Invalid API key from IP: {request.client.host}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "error": "Invalid API key",
                        "header": settings.API_KEY_HEADER
                    }
                )

            app_logger.debug("API key validation successful")
            response = await call_next(request)
            
            # Log request duration
            duration = time.time() - start_time
            app_logger.debug(f"Request completed in {duration:.2f} seconds")
            
            return response
            
        except HTTPException as e:
            # Log the error with more details
            app_logger.error(f"HTTP Exception: {e.detail}")
            raise
        except Exception as e:
            # Log unexpected errors
            app_logger.error(f"Unexpected error in security middleware: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred"
                }
            )

def sanitize_input(text: str) -> str:
    """
    Sanitize input text to prevent potential security issues.
    
    Args:
        text (str): Input text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
        
    text = re.sub(r'<[^>]+>', '', text)
    
    text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', text)
    
    text = re.sub(r'[<>{}()\[\]\\/]', '', text)
    
    text = text.strip()
    
    if len(text) > settings.MAX_QUESTION_LENGTH:
        text = text[:settings.MAX_QUESTION_LENGTH]
        app_logger.warning(f"Input text truncated to {settings.MAX_QUESTION_LENGTH} characters")
    
    return text 