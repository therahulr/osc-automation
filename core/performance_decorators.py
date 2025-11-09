"""
Performance Tracking Decorators and Context Managers

Enhanced decorators and context managers for comprehensive automation performance tracking:
- @performance_step: Track individual functions/methods with detailed metrics
- @track_actions: Auto-track Playwright actions (clicks, typing, navigation)
- PerformanceSession: Context manager for complete workflow tracking
- StepContext: Context manager for individual step tracking

All integrations are backward compatible and optional.
"""

import functools
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional, List
from datetime import datetime

from core.performance import performance_tracker, RunMetadata, StepMetrics


class PerformanceSession:
    """Context manager for tracking complete automation workflows"""
    
    def __init__(self, script_name: str, **metadata):
        """
        Initialize performance session
        
        Args:
            script_name: Name of the automation script
            **metadata: Optional metadata (environment, browser_type, headless, etc.)
        """
        self.metadata = RunMetadata(
            script_name=script_name,
            environment=metadata.get('environment'),
            browser_type=metadata.get('browser_type'),
            headless=metadata.get('headless'),
            viewport_size=metadata.get('viewport_size'),
            user_agent=metadata.get('user_agent'),
            tags=metadata.get('tags'),
            notes=metadata.get('notes')
        )
        self.session_id = None
        self.started_at = None
        
    def __enter__(self):
        """Start performance tracking session"""
        self.started_at = time.time()
        self.session_id = performance_tracker.start_session(self.metadata)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End performance tracking session"""
        status = 'failed' if exc_type else 'success'
        performance_tracker.end_session(status)
        
    def step(self, step_name: str, step_type: str = 'action', **kwargs):
        """Create a step context within this session"""
        return StepContext(step_name, step_type, **kwargs)


class StepContext:
    """Context manager for tracking individual automation steps"""
    
    def __init__(self, step_name: str, step_type: str = 'action', **metadata):
        """
        Initialize step context
        
        Args:
            step_name: Descriptive name for this step
            step_type: Type of step (action, verification, navigation, wait)
            **metadata: Optional step metadata
        """
        self.step_name = step_name
        self.step_type = step_type
        self.metadata = metadata
        self.started_at = None
        self.step_id = None
        
    def __enter__(self):
        """Start step timing"""
        self.started_at = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End step timing and record metrics"""
        duration = time.time() - self.started_at
        status = 'failed' if exc_type else 'success'
        error_message = str(exc_val) if exc_val else None
        
        metrics = StepMetrics(
            step_name=self.step_name,
            step_type=self.step_type,
            duration=duration,
            status=status,
            error_message=error_message,
            page_url=self.metadata.get('page_url'),
            element_selector=self.metadata.get('element_selector'),
            screenshot_path=self.metadata.get('screenshot_path'),
            metadata=self.metadata
        )
        
        self.step_id = performance_tracker.track_step(metrics)
        
    def track_action(self, action_type: str, target: str, success: bool = True, **kwargs):
        """Track a micro-level action within this step"""
        if self.step_id:
            performance_tracker.track_action(
                self.step_id, action_type, target, 
                kwargs.get('duration', 0.0), success, **kwargs
            )


def performance_step(step_name: Optional[str] = None, step_type: str = 'action', 
                    capture_page_info: bool = True, capture_errors: bool = True):
    """
    Enhanced decorator for tracking function performance with detailed metrics
    
    Args:
        step_name: Custom name for the step (defaults to function name)
        step_type: Type of step (action, verification, navigation, wait)
        capture_page_info: Automatically capture page URL and title
        capture_errors: Capture exception details
    
    Usage:
        @performance_step("User Login", "action")
        def login_user(self, username, password):
            # Function implementation
            pass
            
        @performance_step(capture_page_info=True)
        def verify_dashboard(self):
            # Automatic step naming and page info capture
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Only track if we have an active session
            if not performance_tracker.get_current_session():
                return func(*args, **kwargs)
            
            # Determine step name
            name = step_name or func.__name__.replace('_', ' ').title()
            
            # Prepare metadata
            metadata = {}
            
            # Try to capture page info if requested and we have a page object
            if capture_page_info:
                page = None
                # Look for page in self or args
                if args and hasattr(args[0], 'page'):
                    page = args[0].page
                elif 'page' in kwargs:
                    page = kwargs['page']
                
                if page:
                    try:
                        metadata['page_url'] = page.url
                        metadata['page_title'] = page.title()
                    except Exception:
                        pass  # Page might not be available
            
            # Execute function with step tracking
            with StepContext(name, step_type, **metadata) as step:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if capture_errors:
                        metadata['error_details'] = str(e)
                    raise
                    
        return wrapper
    return decorator


def track_playwright_actions(func: Callable) -> Callable:
    """
    Decorator to automatically track Playwright actions (clicks, typing, navigation)
    
    This decorator wraps Playwright page methods to automatically log micro-actions
    
    Usage:
        @track_playwright_actions
        def click_login_button(self):
            self.page.click("#login-btn")  # Automatically tracked
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Only track if we have an active session
        session = performance_tracker.get_current_session()
        if not session:
            return func(*args, **kwargs)
        
        # Try to get page object for action tracking
        page = None
        if args and hasattr(args[0], 'page'):
            page = args[0].page
        
        if not page:
            return func(*args, **kwargs)
        
        # Monkey patch page methods temporarily to track actions
        original_methods = {}
        tracked_actions = []
        
        def create_action_tracker(method_name, original_method):
            def tracked_method(*method_args, **method_kwargs):
                start_time = time.time()
                success = True
                error = None
                target = str(method_args[0]) if method_args else ''
                
                try:
                    result = original_method(*method_args, **method_kwargs)
                    return result
                except Exception as e:
                    success = False
                    error = str(e)
                    raise
                finally:
                    duration = time.time() - start_time
                    tracked_actions.append({
                        'action_type': method_name,
                        'target': target,
                        'duration': duration,
                        'success': success,
                        'error': error
                    })
            
            return tracked_method
        
        # Track common Playwright actions
        action_methods = ['click', 'fill', 'type', 'goto', 'wait_for_selector', 
                         'wait_for_timeout', 'select_option', 'check', 'uncheck']
        
        # Patch methods
        for method_name in action_methods:
            if hasattr(page, method_name):
                original_methods[method_name] = getattr(page, method_name)
                setattr(page, method_name, create_action_tracker(method_name, original_methods[method_name]))
        
        try:
            # Execute the function
            result = func(*args, **kwargs)
            
            # TODO: Link tracked actions to current step
            # This would require getting the current step context
            
            return result
        finally:
            # Restore original methods
            for method_name, original_method in original_methods.items():
                setattr(page, method_name, original_method)
    
    return wrapper


# Convenience context manager for quick step tracking
@contextmanager
def track_step(step_name: str, step_type: str = 'action', **metadata):
    """
    Convenient context manager for tracking steps
    
    Usage:
        with track_step("Login Process", "action"):
            login_page.complete_login(username, password)
    """
    with StepContext(step_name, step_type, **metadata) as step:
        yield step


# Enhanced version of existing decorators that integrate with performance tracking
def enhanced_timeit(step_name: Optional[str] = None, step_type: str = 'action'):
    """
    Enhanced version of @timeit that integrates with performance tracking
    Falls back to original behavior if no performance session is active
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # If performance tracking is active, use it
            if performance_tracker.get_current_session():
                return performance_step(step_name, step_type)(func)(*args, **kwargs)
            else:
                # Fall back to original timeit behavior
                from utils.decorators import timeit
                return timeit(func)(*args, **kwargs)
        
        return wrapper
    return decorator


def enhanced_log_step(step_name: Optional[str] = None, step_type: str = 'action'):
    """
    Enhanced version of @log_step that integrates with performance tracking
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # If performance tracking is active, use it
            if performance_tracker.get_current_session():
                return performance_step(step_name, step_type)(func)(*args, **kwargs)
            else:
                # Fall back to original log_step behavior
                from utils.decorators import log_step
                return log_step(func)(*args, **kwargs)
        
        return wrapper
    return decorator