"""Browser lifecycle management with Playwright and Performance Tracking."""

from pathlib import Path
from typing import Optional
import time
import sqlite3
from datetime import datetime

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from core.config import settings
from core.logger import get_logger
from core.utils import ensure_dir


class BrowserManager:
    """Manages browser lifecycle, contexts, and pages.

    Handles browser launch, context creation with profiles/incognito,
    and trace collection based on global settings.
    """

    def __init__(self, enable_performance_tracking: bool = True) -> None:
        """Initialize browser manager.
        
        Args:
            enable_performance_tracking: Enable automatic performance tracking
        """
        self._playwright = None
        self._browser: Browser | None = None
        self._contexts: list[BrowserContext] = []
        self._logger = get_logger()
        self._performance_tracking = enable_performance_tracking

    def launch(self) -> None:
        """Launch browser with configured settings.

        Uses Chromium by default with settings from core.config.
        """
        launch_start = time.time()
        
        self._logger.info(
            f"Launching browser | headless={settings.headless}, slow_mo={settings.slow_mo_ms}ms"
        )

        self._playwright = sync_playwright().start()
        
        # Launch with maximized window (--start-maximized doesn't work reliably on Mac)
        # We'll set viewport to screen size in new_context instead
        self._browser = self._playwright.chromium.launch(
            headless=settings.headless, 
            slow_mo=settings.slow_mo_ms,
            args=['--start-maximized'] if not settings.headless else []
        )

        launch_duration = time.time() - launch_start
        self._logger.info(f"Browser launched successfully in {launch_duration:.2f}s")
        
        # Track browser launch performance if performance tracking is enabled
        if self._performance_tracking:
            try:
                from core.performance import performance_tracker
                session = performance_tracker.get_current_session()
                if session:
                    with sqlite3.connect(performance_tracker.db_path) as conn:
                        conn.execute("""
                            INSERT INTO browser_metrics (
                                run_id, session_id, recorded_at, page_load_time, 
                                viewport_size
                            ) VALUES (?, ?, ?, ?, ?)
                        """, (
                            session['run_id'], session['session_id'],
                            datetime.now(), launch_duration,
                            f"{settings.viewport_width}x{settings.viewport_height}" if hasattr(settings, 'viewport_width') else None
                        ))
            except Exception as e:
                self._logger.debug(f"Could not track browser launch performance: {e}")

    def _get_screen_viewport(self) -> dict:
        """Get appropriate viewport size for the browser window.
        
        Works on macOS, Windows, and Linux.
        
        Returns:
            Dictionary with width and height for a properly sized browser
        """
        import platform
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                from AppKit import NSScreen
                screen = NSScreen.mainScreen()
                visible = screen.visibleFrame()  # Excludes dock and menu bar
                width = int(visible.size.width)
                height = int(visible.size.height)
                self._logger.info(f"macOS screen visible area: {width}x{height}")
                return {"width": width, "height": height}
                
            elif system == "Windows":
                import ctypes
                user32 = ctypes.windll.user32
                # Get work area (excludes taskbar)
                from ctypes import wintypes
                class RECT(ctypes.Structure):
                    _fields_ = [("left", wintypes.LONG), ("top", wintypes.LONG),
                                ("right", wintypes.LONG), ("bottom", wintypes.LONG)]
                rect = RECT()
                # SPI_GETWORKAREA = 0x0030
                ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0)
                width = rect.right - rect.left
                height = rect.bottom - rect.top
                self._logger.info(f"Windows screen work area: {width}x{height}")
                return {"width": width, "height": height}
                
            elif system == "Linux":
                import subprocess
                # Try xrandr for Linux
                result = subprocess.run(['xrandr'], capture_output=True, text=True, timeout=5)
                import re
                match = re.search(r'(\d+)x(\d+)\+0\+0', result.stdout)
                if match:
                    width = int(match.group(1))
                    height = int(match.group(2)) - 50  # Account for taskbar
                    self._logger.info(f"Linux screen: {width}x{height}")
                    return {"width": width, "height": height}
                    
        except ImportError as e:
            self._logger.debug(f"Screen detection library not available: {e}")
        except Exception as e:
            self._logger.debug(f"Could not detect screen size: {e}")
        
        # Fallback: Use standard resolution that works on most screens
        self._logger.info("Using default viewport: 1280x800")
        return {"width": 1280, "height": 800}

    def new_context(
        self,
        user_profile_dir: Optional[str] = None,
        incognito: Optional[bool] = None,
        viewport: Optional[dict] = None,
        record_video: bool = False,
        video_dir: Optional[Path] = None,
    ) -> BrowserContext:
        """Create new browser context with optional profile or incognito mode.

        Args:
            user_profile_dir: Path to user profile directory (persistent context)
            incognito: Override default incognito setting from config
            viewport: Custom viewport size (default: screen size)
            record_video: Enable video recording for this context
            video_dir: Directory to save videos (required if record_video=True)

        Returns:
            New BrowserContext instance

        Raises:
            RuntimeError: If browser not launched
        """
        if self._browser is None:
            raise RuntimeError("Browser not launched. Call launch() first.")

        use_incognito = incognito if incognito is not None else settings.incognito

        # Prepare downloads directory
        downloads_path = ensure_dir(settings.downloads_dir)

        # Get screen size for maximized viewport (like Selenium's maximize_window)
        if viewport is None:
            viewport = self._get_screen_viewport()

        context_kwargs = {
            "viewport": viewport,
            "accept_downloads": True,
        }
        
        # Add video recording if enabled
        if record_video and video_dir:
            context_kwargs["record_video_dir"] = str(video_dir)
            context_kwargs["record_video_size"] = viewport
            self._logger.info(f"Video recording enabled | dir={video_dir}")

        # Persistent context (user profile) OR standard context
        if user_profile_dir:
            self._logger.info(f"Creating persistent context | profile={user_profile_dir}")
            context = self._playwright.chromium.launch_persistent_context(
                user_data_dir=user_profile_dir,
                headless=settings.headless,
                slow_mo=settings.slow_mo_ms,
                **context_kwargs,
            )
        else:
            mode = "incognito" if use_incognito else "standard"
            self._logger.info(f"Creating new context | mode={mode}")
            context = self._browser.new_context(**context_kwargs)

        # Enable tracing if configured
        if settings.trace_enabled:
            trace_dir = ensure_dir("traces")
            self._logger.debug(f"Starting trace collection | dir={trace_dir}")
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

        self._contexts.append(context)
        return context

    def position_window(self, page: Page, context: BrowserContext = None) -> bool:
        """Position a page window at top-left corner with screen-fit size.
        
        Call this method when switching to a new tab/popup to ensure
        consistent window positioning.
        
        Args:
            page: Page to position
            context: BrowserContext (uses page's context if not provided)
            
        Returns:
            bool: True if positioning succeeded, False otherwise
        """
        try:
            ctx = context or page.context
            viewport = self._get_screen_viewport()
            cdp = ctx.new_cdp_session(page)
            
            # Get window ID first
            window_info = cdp.send("Browser.getWindowForTarget")
            window_id = window_info.get("windowId")
            
            if window_id:
                # Set window bounds: position at (0, 0) and set size
                cdp.send("Browser.setWindowBounds", {
                    "windowId": window_id,
                    "bounds": {
                        "left": 0,
                        "top": 0,
                        "width": viewport["width"],
                        "height": viewport["height"],
                        "windowState": "normal"
                    }
                })
                self._logger.debug(f"Window positioned at (0, 0) with size {viewport['width']}x{viewport['height']}")
                return True
        except Exception as e:
            self._logger.debug(f"Could not position window via CDP: {e}")
        return False

    def new_page(self, context: BrowserContext) -> Page:
        """Create new page in given context with performance tracking.

        Args:
            context: BrowserContext to create page in

        Returns:
            New Page instance with optional performance monitoring
        """
        self._logger.debug("Creating new page in context")
        page_start = time.time()
        
        page = context.new_page()

        # Set default timeouts from settings
        page.set_default_timeout(settings.default_timeout_ms)
        page.set_default_navigation_timeout(settings.nav_timeout_ms)
        
        # Position window at top-left corner (0, 0) using CDP
        self.position_window(page, context)
        self._logger.info(f"Window positioned at (0, 0) with screen-fit size")
        
        page_creation_time = time.time() - page_start
        self._logger.debug(f"Page created in {page_creation_time:.3f}s")

        # Add performance tracking hooks if enabled
        if self._performance_tracking:
            self._add_performance_hooks(page)

        return page
    
    def _add_performance_hooks(self, page: Page):
        """Add performance tracking hooks to page object"""
        try:
            from core.performance import performance_tracker
            
            # Only add hooks if we have an active performance session
            session = performance_tracker.get_current_session()
            if not session:
                return
            
            # Store original methods
            original_goto = page.goto
            original_wait_for_selector = page.wait_for_selector
            original_click = page.click
            original_fill = page.fill
            
            def tracked_goto(url, **kwargs):
                start_time = time.time()
                try:
                    result = original_goto(url, **kwargs)
                    duration = time.time() - start_time
                    self._track_page_navigation(url, duration, True)
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self._track_page_navigation(url, duration, False, str(e))
                    raise
            
            def tracked_wait_for_selector(selector, **kwargs):
                start_time = time.time()
                try:
                    result = original_wait_for_selector(selector, **kwargs)
                    duration = time.time() - start_time
                    self._track_element_wait(selector, duration, True)
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self._track_element_wait(selector, duration, False, str(e))
                    raise
            
            def tracked_click(selector, **kwargs):
                start_time = time.time()
                try:
                    result = original_click(selector, **kwargs)
                    duration = time.time() - start_time
                    self._track_element_action('click', selector, duration, True)
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self._track_element_action('click', selector, duration, False, error=str(e))
                    raise
            
            def tracked_fill(selector, value, **kwargs):
                start_time = time.time()
                try:
                    result = original_fill(selector, value, **kwargs)
                    duration = time.time() - start_time
                    self._track_element_action('fill', selector, duration, True, value=value)
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self._track_element_action('fill', selector, duration, False, value=value, error=str(e))
                    raise
            
            # Apply tracking wrappers
            page.goto = tracked_goto
            page.wait_for_selector = tracked_wait_for_selector
            page.click = tracked_click
            page.fill = tracked_fill
            
        except Exception as e:
            self._logger.debug(f"Could not add performance hooks: {e}")
    
    def _track_page_navigation(self, url: str, duration: float, success: bool, error: str = None):
        """Track page navigation performance"""
        try:
            from core.performance import performance_tracker
            session = performance_tracker.get_current_session()
            if session:
                with sqlite3.connect(performance_tracker.db_path) as conn:
                    conn.execute("""
                        INSERT INTO browser_metrics (
                            run_id, session_id, recorded_at, page_load_time, page_url
                        ) VALUES (?, ?, ?, ?, ?)
                    """, (session['run_id'], session['session_id'], datetime.now(), duration, url))
        except Exception as e:
            self._logger.debug(f"Could not track navigation: {e}")
    
    def _track_element_wait(self, selector: str, duration: float, success: bool, error: str = None):
        """Track element wait performance"""
        try:
            from core.performance import performance_tracker
            session = performance_tracker.get_current_session()
            if session:
                # This would ideally be linked to a current step, but for now just log it
                self._logger.debug(f"Element wait: {selector} took {duration:.3f}s, success: {success}")
        except Exception as e:
            self._logger.debug(f"Could not track element wait: {e}")
    
    def _track_element_action(self, action: str, selector: str, duration: float, success: bool, **kwargs):
        """Track element action performance"""
        try:
            from core.performance import performance_tracker
            session = performance_tracker.get_current_session()
            if session:
                # This would ideally be linked to a current step, but for now just log it
                self._logger.debug(f"Element {action}: {selector} took {duration:.3f}s, success: {success}")
        except Exception as e:
            self._logger.debug(f"Could not track element action: {e}")

    def get_page(
        self,
        user_profile_dir: Optional[str] = None,
        incognito: Optional[bool] = None,
        viewport: Optional[dict] = None,
    ) -> Page:
        """Get a ready-to-use page with automatic browser setup.
        
        This is a convenience method that handles the full browser lifecycle:
        launch -> new_context -> new_page
        
        Args:
            user_profile_dir: Path to user profile directory (persistent context)
            incognito: Override default incognito setting from config
            viewport: Custom viewport size (default: maximized 1920x1080)
            
        Returns:
            New Page instance ready for automation
        """
        if self._browser is None:
            self.launch()
        
        context = self.new_context(user_profile_dir, incognito, viewport)
        return self.new_page(context)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically close browser."""
        self.close()
        return False

    def close(self) -> None:
        """Close all contexts, browser, and cleanup resources.

        Saves traces if enabled before closing.
        """
        self._logger.info("Closing browser and all contexts")

        # Stop and save traces
        if settings.trace_enabled:
            trace_dir = ensure_dir("traces")
            for idx, context in enumerate(self._contexts):
                try:
                    trace_file = trace_dir / f"trace_{idx}.zip"
                    self._logger.debug(f"Saving trace | file={trace_file}")
                    context.tracing.stop(path=str(trace_file))
                except Exception as e:
                    self._logger.warning(f"Failed to save trace {idx}: {e}")

        # Close contexts
        for context in self._contexts:
            try:
                context.close()
            except Exception as e:
                self._logger.warning(f"Error closing context: {e}")

        self._contexts.clear()

        # Close browser
        if self._browser:
            self._browser.close()
            self._browser = None

        # Stop playwright
        if self._playwright:
            self._playwright.stop()
            self._playwright = None

        self._logger.info("Browser cleanup completed")
