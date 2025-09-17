# src/utils.py
# Utility functions: logging and retry decorator

import logging
import logging.handlers
import time
from functools import wraps
from config import LOG_MAX_BYTES, LOG_BACKUP_COUNT

def get_logger():
    """
    Centralized logger with rotation.
    Logs to 'dashboard.log' and console.
    """
    logger = logging.getLogger("trading_dashboard")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.handlers.RotatingFileHandler(
            'dashboard.log', maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger

def retry_network(max_retries=3, backoff_factor=1):
    """
    Retry decorator for network calls with exponential backoff.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retries >= max_retries:
                        logger = get_logger()
                        logger.error(f"Max retries reached for {func.__name__}: {e}")
                        raise
                    sleep_time = backoff_factor * (2 ** retries)
                    retries += 1
                    time.sleep(sleep_time)
        return wrapper
    return decorator
