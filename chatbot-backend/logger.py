import logging
import sys
from pathlib import Path
import os
from logging.handlers import RotatingFileHandler
import re

BACKEND_DIR = Path(__file__).parent.absolute()

logs_dir = BACKEND_DIR / "logs"
logs_dir.mkdir(exist_ok=True)

def setup_logger():
    # Create a custom formatter that masks sensitive information
    class SensitiveDataFormatter(logging.Formatter):
        def format(self, record):
            # Get the original message
            message = super().format(record)
            
            # List of sensitive patterns to mask
            sensitive_patterns = [
                r'api[-_]?key["\']?\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                r'openai[-_]?key["\']?\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                r'secret["\']?\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                r'token["\']?\s*[:=]\s*["\']?([^"\'\s]+)["\']?',
                r'sk-[a-zA-Z0-9]{32,}',
                r'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
            ]
            
            # Mask each sensitive pattern
            for pattern in sensitive_patterns:
                message = re.sub(pattern, '***MASKED***', message, flags=re.IGNORECASE)
            
            return message

    # Create logger
    logger = logging.getLogger("rag_chatbot.app")
    logger.setLevel(logging.DEBUG)

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    formatter = SensitiveDataFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    logger.info("Logger initialized")
    
    return logger

app_logger = setup_logger()

# Configure other loggers
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.setLevel(logging.INFO)

uvicorn_error_logger = logging.getLogger("uvicorn.error")
uvicorn_error_logger.setLevel(logging.INFO)

slowapi_logger = logging.getLogger("slowapi")
slowapi_logger.setLevel(logging.DEBUG)

app_logger.info("Logger setup completed successfully") 