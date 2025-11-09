"""Browser lifecycle management with Playwright."""

from pathlib import Path
from typing import Optional

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from core.config import settings
from core.logger import Logger
from core.utils import ensure_dir


class BrowserManager:
    """Manages browser lifecycle, contexts, and pages.

    Handles browser launch, context creation with profiles/incognito,
    and trace collection based on global settings.
    """

    def __init__(self) -> None:
        """Initialize browser manager."""
        self._playwright = None
        self._browser: Browser | None = None
        self._contexts: list[BrowserContext] = []
        self._logger = Logger.get()

    def launch(self) -> None:
        """Launch browser with configured settings.

        Uses Chromium by default with settings from core.config.
        """
        self._logger.info(
            f"Launching browser | headless={settings.headless}, slow_mo={settings.slow_mo_ms}ms"
        )

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=settings.headless, slow_mo=settings.slow_mo_ms
        )

        self._logger.info("Browser launched successfully")

    def new_context(
        self,
        user_profile_dir: Optional[str] = None,
        incognito: Optional[bool] = None,
        viewport: Optional[dict] = None,
    ) -> BrowserContext:
        """Create new browser context with optional profile or incognito mode.

        Args:
            user_profile_dir: Path to user profile directory (persistent context)
            incognito: Override default incognito setting from config
            viewport: Custom viewport size (default: maximized 1920x1080)

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

        # Default to maximized viewport
        if viewport is None:
            viewport = {"width": 1920, "height": 1080}

        context_kwargs = {
            "viewport": viewport,
            "accept_downloads": True,
        }

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

    def new_page(self, context: BrowserContext) -> Page:
        """Create new page in given context.

        Args:
            context: BrowserContext to create page in

        Returns:
            New Page instance
        """
        self._logger.debug("Creating new page in context")
        page = context.new_page()

        # Set default timeouts from settings
        page.set_default_timeout(settings.default_timeout_ms)
        page.set_default_navigation_timeout(settings.nav_timeout_ms)

        return page

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
