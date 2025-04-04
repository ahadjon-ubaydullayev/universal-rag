import logging
import sys
from pathlib import Path
import os
from logging.handlers import RotatingFileHandler

BACKEND_DIR = Path(__file__).parent.absolute()

logs_dir = BACKEND_DIR / "logs"
logs_dir.mkdir(exist_ok=True)

def setup_logger():
    logger = logging.getLogger("rag_chatbot.app")
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )

        log_file = logs_dir / "app.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG) 
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO) 
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.propagate = False

        logger.info(f"Logger initialized. Log file location: {log_file}")
    
    return logger

app_logger = setup_logger()

uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.setLevel(logging.INFO)

uvicorn_error_logger = logging.getLogger("uvicorn.error")
uvicorn_error_logger.setLevel(logging.INFO)

slowapi_logger = logging.getLogger("slowapi")
slowapi_logger.setLevel(logging.DEBUG) 

app_logger.info("Logger setup completed successfully") 