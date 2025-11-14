"""UIAutomationCore - Centralized automation framework entry point.

This module provides a unified interface for all automation tasks, managing:
- Browser lifecycle (singleton)
- Logger (singleton with colored output)
- Performance tracking
- Configuration management

Usage:
    # Simple usage - everything is managed automatically
    from core import UIAutomationCore

    with UIAutomationCore(app_name="osc", script_name="my_workflow") as core:
        page = core.page
        logger = core.logger

        logger.info("Starting automation...")
        page.goto("https://example.com")

    # Advanced usage - custom configuration
    core = UIAutomationCore(
        app_name="osc",
        script_name="my_workflow",
        headless=False,
        enable_performance_tracking=True,
        enable_tracing=False
    )

    with core:
        # Your automation code
        pass

    # Access performance report
    report = core.get_performance_report()
"""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import time

from playwright.sync_api import Page, BrowserContext

from core.browser import BrowserManager
from core.logger import get_logger
from core.config import settings
from core.ui import Ui


class UIAutomationCore:
    """Central automation framework manager.

    Provides unified access to:
    - Browser (singleton) with automatic lifecycle management
    - Logger (singleton) with colored terminal output
    - Performance tracking
    - UI helpers

    Designed to eliminate boilerplate and simplify automation workflows.
    """

    # Class-level singleton instances
    _browser_manager: Optional[BrowserManager] = None
    _logger_instance: Optional[Any] = None
    _app_name: str = "automation"
    _performance_enabled: bool = False
    _current_session = None

    def __init__(
        self,
        app_name: str = "automation",
        script_name: Optional[str] = None,
        headless: Optional[bool] = None,
        enable_performance_tracking: bool = True,
        enable_tracing: bool = False,
        viewport: Optional[Dict[str, int]] = None,
        user_profile_dir: Optional[str] = None,
        incognito: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize UIAutomationCore.

        Args:
            app_name: Application name for logging and organization
            script_name: Script/workflow name for performance tracking
            headless: Override headless mode (None = use config default)
            enable_performance_tracking: Enable detailed performance metrics
            enable_tracing: Enable Playwright trace collection
            viewport: Custom viewport size {"width": 1920, "height": 1080}
            user_profile_dir: Path to persistent browser profile
            incognito: Override incognito mode (None = use config default)
            metadata: Custom metadata for performance tracking
        """
        self._app_name = app_name
        self._script_name = script_name or f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self._enable_performance = enable_performance_tracking
        self._enable_tracing = enable_tracing
        self._viewport = viewport
        self._user_profile_dir = user_profile_dir
        self._incognito = incognito
        self._metadata = metadata or {}

        # Override settings if specified
        if headless is not None:
            settings.headless = headless
        if enable_tracing:
            settings.trace_enabled = True

        # Initialize logger (singleton)
        if UIAutomationCore._logger_instance is None:
            UIAutomationCore._logger_instance = get_logger(app_name)

        self._logger = UIAutomationCore._logger_instance

        # Browser and page instances (created on demand)
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._ui: Optional[Ui] = None

        # Performance session
        self._performance_session = None
        self._session_context_manager = None

        # Timer for tracking execution duration
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None

        self._logger.info(f"UIAutomationCore initialized | app={app_name}, script={self._script_name}")

    @property
    def logger(self):
        """Get the singleton logger instance."""
        return self._logger

    @property
    def browser(self) -> BrowserManager:
        """Get the singleton browser manager (lazy initialization)."""
        if UIAutomationCore._browser_manager is None:
            UIAutomationCore._browser_manager = BrowserManager(
                enable_performance_tracking=self._enable_performance
            )
            UIAutomationCore._browser_manager.launch()
        return UIAutomationCore._browser_manager

    @property
    def page(self) -> Page:
        """Get the current page (creates if needed)."""
        if self._page is None:
            self._context = self.browser.new_context(
                user_profile_dir=self._user_profile_dir,
                incognito=self._incognito,
                viewport=self._viewport
            )
            self._page = self.browser.new_page(self._context)
            self._logger.info("Browser page created and ready")
        return self._page

    @property
    def ui(self) -> Ui:
        """Get UI helper instance (wraps page for enhanced operations)."""
        if self._ui is None:
            self._ui = Ui(self.page)
        return self._ui

    @property
    def config(self):
        """Get global settings."""
        return settings

    def start_performance_tracking(self, tags: Optional[list] = None, notes: Optional[str] = None):
        """Manually start performance tracking session.

        Args:
            tags: Optional tags for categorizing the run
            notes: Optional notes about the run
        """
        if not self._enable_performance:
            self._logger.warning("Performance tracking is disabled")
            return

        try:
            from core.performance_decorators import PerformanceSession
            from core.performance import RunMetadata

            metadata = RunMetadata(
                script_name=self._script_name,
                environment=settings.env,
                browser_type="chromium",
                headless=settings.headless,
                viewport_size=f"{self._viewport.get('width', 1920)}x{self._viewport.get('height', 1080)}" if self._viewport else "1920x1080",
                tags=tags,
                notes=notes
            )

            self._session_context_manager = PerformanceSession(
                script_name=self._script_name,
                metadata=metadata
            )
            self._session_context_manager.__enter__()
            self._logger.info("Performance tracking session started")

        except Exception as e:
            self._logger.error(f"Failed to start performance tracking: {e}")

    def stop_performance_tracking(self):
        """Manually stop performance tracking session."""
        if self._session_context_manager:
            try:
                self._session_context_manager.__exit__(None, None, None)
                self._logger.info("Performance tracking session stopped")
            except Exception as e:
                self._logger.error(f"Failed to stop performance tracking: {e}")
            finally:
                self._session_context_manager = None

    def get_performance_report(self, format: str = "summary") -> Optional[str]:
        """Generate performance report for the current or last run.

        Args:
            format: Report format - 'summary', 'detailed', 'json'

        Returns:
            Formatted performance report or None if tracking disabled
        """
        if not self._enable_performance:
            self._logger.warning("Performance tracking is disabled")
            return None

        try:
            from core.performance_reporter import PerformanceReporter
            reporter = PerformanceReporter()

            if format == "summary":
                return reporter.generate_summary_report()
            elif format == "detailed":
                return reporter.generate_detailed_report()
            elif format == "json":
                return reporter.generate_json_report()
            else:
                self._logger.warning(f"Unknown report format: {format}")
                return None

        except Exception as e:
            self._logger.error(f"Failed to generate performance report: {e}")
            return None

    def take_screenshot(self, name: str = "screenshot", full_page: bool = True) -> Path:
        """Take a screenshot of the current page.

        Args:
            name: Screenshot file name (without extension)
            full_page: Capture full page or just viewport

        Returns:
            Path to saved screenshot
        """
        screenshots_dir = Path.cwd() / "screenshots" / self._app_name
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = screenshots_dir / f"{name}_{timestamp}.png"

        self.page.screenshot(path=str(screenshot_path), full_page=full_page)
        self._logger.info(f"Screenshot saved: {screenshot_path}")

        return screenshot_path

    def __enter__(self):
        """Context manager entry - automatically start performance tracking."""
        # Record start time
        self._start_time = time.time()
        start_datetime = datetime.fromtimestamp(self._start_time)

        # Print start banner with colored output
        print("\n" + "="*80)
        print(f"🚀 AUTOMATION STARTED")
        print("="*80)
        print(f"Script:     {self._script_name}")
        print(f"Started At: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")

        if self._enable_performance:
            self.start_performance_tracking()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup and generate reports."""
        try:
            # Record end time
            self._end_time = time.time()
            end_datetime = datetime.fromtimestamp(self._end_time)

            # Calculate duration
            if self._start_time:
                duration_seconds = self._end_time - self._start_time
                duration_minutes = duration_seconds / 60
                duration_hours = duration_minutes / 60

                # Format duration nicely
                if duration_hours >= 1:
                    duration_str = f"{int(duration_hours)}h {int(duration_minutes % 60)}m {duration_seconds % 60:.2f}s"
                elif duration_minutes >= 1:
                    duration_str = f"{int(duration_minutes)}m {duration_seconds % 60:.2f}s"
                else:
                    duration_str = f"{duration_seconds:.2f}s"
            else:
                duration_str = "N/A"

            # Stop performance tracking
            if self._enable_performance:
                self.stop_performance_tracking()

            # Generate performance report
            if self._enable_performance:
                report = self.get_performance_report(format="summary")
                if report:
                    self._logger.info("\n" + "="*80 + "\nPERFORMANCE REPORT\n" + "="*80 + "\n" + report)

            # Close browser (singleton will be reused if needed)
            if self._page:
                self._page.close()
                self._page = None

            if self._context:
                self._context.close()
                self._context = None

            self._logger.info("UIAutomationCore context closed")

            # Print end banner with timing info
            status = "✓ COMPLETED SUCCESSFULLY" if exc_type is None else "✗ FAILED"
            status_color = "green" if exc_type is None else "red"

            print("\n" + "="*80)
            print(f"🏁 AUTOMATION {status}")
            print("="*80)
            print(f"Script:     {self._script_name}")
            print(f"Ended At:   {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Duration:   {duration_str}")
            print("="*80 + "\n")

        except Exception as e:
            self._logger.error(f"Error during cleanup: {e}")

        return False

    @classmethod
    def cleanup_all(cls):
        """Cleanup all singleton resources (browser, logger).

        Call this at the end of your script to ensure proper cleanup.
        """
        if cls._browser_manager:
            cls._browser_manager.close()
            cls._browser_manager = None

        if cls._logger_instance:
            cls._logger_instance.info("UIAutomationCore cleanup completed")


# Convenience function for quick automation tasks
def quick_automation(
    app_name: str = "automation",
    script_name: str = "quick_script",
    headless: bool = False
) -> UIAutomationCore:
    """Quick automation setup with sensible defaults.

    Usage:
        with quick_automation("my_app") as core:
            core.page.goto("https://example.com")
            core.logger.info("Done!")

    Args:
        app_name: Application name
        script_name: Script name
        headless: Run in headless mode

    Returns:
        UIAutomationCore instance
    """
    return UIAutomationCore(
        app_name=app_name,
        script_name=script_name,
        headless=headless,
        enable_performance_tracking=True
    )
