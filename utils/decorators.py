"""
Automation decorators for common functionality
"""

import time
import functools
from typing import Callable, Any
from utils.logger import get_logger

logger = get_logger(__name__)


def timeit(func: Callable) -> Callable:
    """Track execution time of automation steps"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} completed in {duration:.2f}s")
        return result
    return wrapper


def retry(attempts: int = 3, delay: float = 1.0):
    """Retry automation steps on failure"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == attempts - 1:
                        logger.error(f"{func.__name__} failed after {attempts} attempts: {e}")
                        raise
                    time.sleep(delay)
            return False
        return wrapper
    return decorator


def log_step(func: Callable) -> Callable:
    """Minimal logging for automation steps"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f"Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper