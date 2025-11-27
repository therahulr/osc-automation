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
from core.logger import get_logger, AutomationLogger
from core.config import settings
from core.ui import Ui
from core.run_context import RunContext
from config.browser_config import browser_config


class UIAutomationCore:
    """Central automation framework manager.

    Provides unified access to:
    - Browser (singleton) with automatic lifecycle management
    - Logger (singleton) with colored terminal output
    - RunContext for unified output folder management
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
        enable_tracing: Optional[bool] = None,
        record_video: Optional[bool] = None,
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
            enable_tracing: Enable Playwright trace collection (None = use config default)
            record_video: Enable video recording (None = use config default from browser.config.yaml)
            viewport: Custom viewport size {"width": 1920, "height": 1080}
            user_profile_dir: Path to persistent browser profile
            incognito: Override incognito mode (None = use config default)
            metadata: Custom metadata for performance tracking
        """
        self._app_name = app_name
        self._script_name = script_name or f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self._enable_performance = enable_performance_tracking
        # Use config defaults if not explicitly specified
        self._enable_tracing = enable_tracing if enable_tracing is not None else browser_config.trace_enabled
        self._record_video = record_video if record_video is not None else browser_config.video_enabled
        self._viewport = viewport
        self._user_profile_dir = user_profile_dir
        self._incognito = incognito
        self._metadata = metadata or {}

        # Override settings if specified
        if headless is not None:
            settings.headless = headless
        if self._enable_tracing:
            settings.trace_enabled = True

        # Initialize RunContext FIRST - this sets up the unified output folder
        self._run_context = RunContext.initialize(
            app_name=app_name,
            script_name=self._script_name
        )

        # Initialize logger with RunContext's log file
        if UIAutomationCore._logger_instance is None:
            UIAutomationCore._logger_instance = get_logger(app_name, self._run_context.log_file)
        else:
            # Logger already exists, reconfigure to use RunContext's log file
            AutomationLogger.reconfigure_file_handler(self._run_context.log_file)

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
        self._logger.info(f"Artifacts folder: {self._run_context.run_dir}")

    @property
    def logger(self):
        """Get the singleton logger instance."""
        return self._logger

    @property
    def run_context(self) -> RunContext:
        """Get the current run context for accessing output paths."""
        return self._run_context
    
    @property
    def run_dir(self) -> Path:
        """Get the root directory for this run's artifacts."""
        return self._run_context.run_dir

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
                viewport=self._viewport,
                record_video=self._record_video,
                video_dir=self._run_context.videos_dir if self._record_video else None
            )
            self._page = self.browser.new_page(self._context)
            self._logger.info("Browser page created and ready")
            if self._record_video:
                self._logger.info(f"Video recording started | dir={self._run_context.videos_dir}")
        return self._page

    def position_page(self, page: Page) -> bool:
        """Position a page window at top-left corner with screen-fit size.
        
        Call this method after switching to a new tab/popup to ensure
        consistent window positioning across all pages.
        
        Args:
            page: Page to position (e.g., new tab from popup)
            
        Returns:
            bool: True if positioning succeeded, False otherwise
            
        Example:
            # After handling popup:
            with page.expect_popup() as popup_info:
                page.click(button)
            new_page = popup_info.value
            core.position_page(new_page)  # Position the new tab
        """
        return self.browser.position_window(page, self._context)

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

    def take_screenshot(self, name: str = "screenshot", page: Optional[Page] = None) -> Path:
        """Take a screenshot of the current viewport (visible area only).

        Args:
            name: Screenshot file name (without extension)
            page: Optional specific page to screenshot. If None, uses the active page
                  from the browser context (handles multiple tabs correctly).

        Returns:
            Path to saved screenshot
        """
        # Use RunContext for screenshot path (auto-numbered)
        screenshot_path = self._run_context.get_screenshot_path(name)

        # Use provided page, or get the active page from context
        target_page = page
        if target_page is None:
            # Try to get the most recently active page from context
            if self._context and self._context.pages:
                # Get the last page in the context (most recently opened/active)
                target_page = self._context.pages[-1]
                self._logger.debug(f"Using active page from context: {target_page.url[:50]}...")
            else:
                target_page = self.page
        
        # Take viewport screenshot only (not full page)
        # Use animations="disabled" to prevent flickering during capture
        target_page.screenshot(
            path=str(screenshot_path), 
            full_page=False,
            animations="disabled",  # Prevents CSS animations from causing flicker
            caret="hide"  # Hide text cursor/caret
        )
        self._logger.info(f"Screenshot saved: {screenshot_path.name}")

        return screenshot_path

    def take_full_page_screenshot(self, name: str = "full_page", page: Optional[Page] = None) -> Path:
        """Take a full page screenshot (scrolls through entire page).
        
        Use this for final documentation screenshots after automation completes.
        For step-by-step screenshots during automation, use take_screenshot() instead.

        Args:
            name: Screenshot file name (without extension)
            page: Optional specific page to screenshot. If None, uses the active page
                  from the browser context (handles multiple tabs correctly).

        Returns:
            Path to saved screenshot
        """
        # Use RunContext for screenshot path (auto-numbered)
        screenshot_path = self._run_context.get_screenshot_path(f"{name}_full", auto_number=True)

        # Use provided page, or get the active page from context
        target_page = page
        if target_page is None:
            if self._context and self._context.pages:
                target_page = self._context.pages[-1]
                self._logger.debug(f"Using active page for full screenshot: {target_page.url[:50]}...")
            else:
                target_page = self.page
        
        # Take full page screenshot (scrolls through entire page)
        # Use animations="disabled" to prevent flickering during capture
        target_page.screenshot(
            path=str(screenshot_path), 
            full_page=True,
            animations="disabled",  # Prevents CSS animations from causing flicker
            caret="hide"  # Hide text cursor/caret
        )
        self._logger.info(f"Full page screenshot saved: {screenshot_path.name}")

        return screenshot_path

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
        print(f"Script:      {self._script_name}")
        print(f"Started At:  {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Artifacts:   {self._run_context.run_dir}")
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

            # Update run status in run_info.json
            if exc_type is None:
                self._run_context.update_status("completed")
            else:
                self._run_context.update_status("failed", str(exc_val))

            # Stop performance tracking
            if self._enable_performance:
                self.stop_performance_tracking()

            # Generate performance report
            if self._enable_performance:
                report = self.get_performance_report(format="summary")
                if report:
                    self._logger.info("\n" + "="*80 + "\nPERFORMANCE REPORT\n" + "="*80 + "\n" + report)

            # Save video paths before closing (Playwright saves video on context close)
            # Note: Playwright creates one video per PAGE, so popups/new tabs have separate videos
            video_paths = []
            if self._record_video and self._context:
                try:
                    # Collect videos from all pages in the context
                    for p in self._context.pages:
                        if p.video:
                            video_paths.append(p.video.path())
                except Exception as ve:
                    self._logger.debug(f"Could not get video paths: {ve}")

            # Close browser (singleton will be reused if needed)
            if self._page:
                self._page.close()
                self._page = None

            if self._context:
                self._context.close()
                self._context = None
            
            # Log video paths after context close (videos are finalized on close)
            # Also try to merge videos if ffmpeg is available
            merged_video = None
            if video_paths:
                self._logger.info(f"Videos saved ({len(video_paths)} files):")
                for vp in video_paths:
                    self._logger.info(f"  - {vp}")
                
                # Attempt to merge videos if multiple exist
                if len(video_paths) > 1:
                    merged_video = self._merge_videos(video_paths)

            self._logger.info("UIAutomationCore context closed")

            # Print end banner with timing info
            status = "✓ COMPLETED SUCCESSFULLY" if exc_type is None else "✗ FAILED"

            print("\n" + "="*80)
            print(f"🏁 AUTOMATION {status}")
            print("="*80)
            print(f"Script:     {self._script_name}")
            print(f"Ended At:   {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Duration:   {duration_str}")
            print(f"Artifacts:  {self._run_context.run_dir}")
            if merged_video:
                print(f"Video:      {merged_video}")
            elif video_paths:
                print(f"Videos:     {len(video_paths)} recording(s)")
                for vp in video_paths:
                    print(f"            {vp}")
            print("="*80 + "\n")

        except Exception as e:
            self._logger.error(f"Error during cleanup: {e}")

        return False

    def _merge_videos(self, video_paths: list) -> Optional[Path]:
        """Merge multiple video files into a single video using ffmpeg.
        
        Args:
            video_paths: List of video file paths to merge
            
        Returns:
            Path to merged video if successful, None otherwise
        """
        import subprocess
        import shutil
        
        # Check if ffmpeg is available
        if not shutil.which('ffmpeg'):
            self._logger.debug("ffmpeg not found, skipping video merge")
            return None
        
        try:
            # Create a concat file listing all videos
            concat_file = self._run_context.videos_dir / "concat_list.txt"
            merged_output = self._run_context.videos_dir / f"{self._script_name}_merged.webm"
            
            with open(concat_file, 'w') as f:
                for vp in video_paths:
                    f.write(f"file '{vp}'\n")
            
            # Run ffmpeg to concatenate videos
            cmd = [
                'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',  # Copy without re-encoding for speed
                str(merged_output)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0 and merged_output.exists():
                self._logger.info(f"Videos merged: {merged_output}")
                # Clean up concat file
                concat_file.unlink(missing_ok=True)
                return merged_output
            else:
                self._logger.debug(f"Video merge failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self._logger.debug("Video merge timed out")
        except Exception as e:
            self._logger.debug(f"Video merge error: {e}")
        
        return None

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
