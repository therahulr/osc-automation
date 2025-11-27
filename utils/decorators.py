"""Automation decorators for common functionality

Enhanced decorators that integrate with performance tracking when available,
but fall back to original behavior for backward compatibility.
"""

import time
import functools
from typing import Callable, Any


def _get_logger():
    """Get the singleton logger from core (lazy import to avoid circular deps)."""
    try:
        from core.logger import get_logger
        return get_logger("automation")
    except Exception:
        import logging
        return logging.getLogger(__name__)


def timeit(func: Callable) -> Callable:
    """Track execution time of automation steps
    
    Enhanced version that integrates with performance tracking when available.
    Falls back to original behavior if no performance session is active.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Try to use performance tracking if available
        try:
            from core.performance import performance_tracker
            from core.performance_decorators import performance_step
            
            session = performance_tracker.get_current_session()
            if session:
                # Use performance tracking
                return performance_step(
                    step_name=func.__name__.replace('_', ' ').title(),
                    step_type='action'
                )(func)(*args, **kwargs)
        except ImportError:
            pass  # Performance tracking not available
        
        # Fall back to original timeit behavior
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        _get_logger().info(f"{func.__name__} completed in {duration:.2f}s")
        return result
    
    return wrapper


def retry(attempts: int = 3, delay: float = 1.0):
    """Retry automation steps on failure
    
    Enhanced version that integrates with performance tracking.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(attempts):
                try:
                    # Track retry attempts if performance tracking is available
                    try:
                        from core.performance import performance_tracker
                        session = performance_tracker.get_current_session()
                        if session and attempt > 0:
                            _get_logger().info(f"{func.__name__} retry attempt {attempt + 1}/{attempts}")
                    except ImportError:
                        pass
                    
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == attempts - 1:
                        _get_logger().error(f"{func.__name__} failed after {attempts} attempts: {e}")
                        raise
                    time.sleep(delay)
            
            return False
        return wrapper
    return decorator


def log_step(func: Callable) -> Callable:
    """Minimal logging for automation steps
    
    Enhanced version that integrates with performance tracking when available.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Try to use performance tracking if available
        try:
            from core.performance import performance_tracker
            from core.performance_decorators import performance_step
            
            session = performance_tracker.get_current_session()
            if session:
                # Use performance tracking with logging
                return performance_step(
                    step_name=func.__name__.replace('_', ' ').title(),
                    step_type='action',
                    capture_page_info=True
                )(func)(*args, **kwargs)
        except ImportError:
            pass  # Performance tracking not available
        
        # Fall back to original log_step behavior
        _get_logger().info(f"Executing: {func.__name__}")
        return func(*args, **kwargs)
    
    return wrapper