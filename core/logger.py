"""
Automation Framework Logging System

Provides a comprehensive logging solution with:
- Singleton pattern for consistent logging across the framework
- Dual output: console (colored) and file (structured)
- Rich terminal formatting for enhanced readability
- Environment-aware log levels
- Automatic log file rotation
- Thread-safe operations
- Cross-platform Unicode support (Windows cp1252 compatible)

Usage:
    from core.logger import get_logger, log_success, log_step

    logger = get_logger("my_app")
    logger.info("Starting automation")

    # Rich formatted output
    log_step("Navigating to login page")
    log_success("Login completed successfully")
    log_metric("Response Time", 1.23, "seconds")
"""

import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, List, Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.table import Table
from rich.theme import Theme

from core.utils import ensure_dir, get_env


def _is_windows_limited_encoding() -> bool:
    """Check if on Windows with limited console encoding."""
    if sys.platform != "win32":
        return False
    try:
        encoding = sys.stdout.encoding or "utf-8"
        return encoding.lower() in ("cp1252", "ascii", "cp437", "cp850")
    except Exception:
        return True


# Custom theme for consistent coloring
AUTOMATION_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "critical": "bold white on red",
    "success": "bold green",
    "debug": "dim cyan",
    "step": "bold magenta",
    "metric": "bold blue",
    "section": "bold cyan",
})


class AutomationLogger:
    """
    Singleton logger for automation framework.

    Provides:
    - Structured logging to files (in RunContext folder when available)
    - Rich formatted console output
    - Automatic log rotation
    - Environment-aware configuration
    """

    _instance: Optional[logging.Logger] = None
    _console: Optional[Console] = None
    _log_dir: Optional[Path] = None
    _log_file: Optional[Path] = None
    _initialized: bool = False

    @classmethod
    def get_logger(cls, app_name: str = "automation", log_file: Optional[Path] = None) -> logging.Logger:
        """
        Get or create singleton logger instance.

        Args:
            app_name: Application name for log file organization
            log_file: Optional explicit log file path (from RunContext)

        Returns:
            Configured logging.Logger instance
        """
        if cls._instance is None:
            cls._instance = cls._create_logger(app_name, log_file)
            cls._console = Console(theme=AUTOMATION_THEME)
            cls._initialized = True
        return cls._instance
    
    @classmethod
    def reconfigure_file_handler(cls, log_file: Path) -> None:
        """Reconfigure the logger to write to a new log file.
        
        Used when RunContext is initialized after logger creation.
        
        Args:
            log_file: New log file path
        """
        if cls._instance is None:
            return
            
        # Remove existing file handlers
        handlers_to_remove = [h for h in cls._instance.handlers 
                             if isinstance(h, (logging.FileHandler, RotatingFileHandler))]
        for handler in handlers_to_remove:
            handler.close()
            cls._instance.removeHandler(handler)
        
        # Add new file handler
        cls._log_file = log_file
        cls._log_dir = log_file.parent
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8',  # Ensure UTF-8 for cross-platform Unicode support
        )
        
        env = get_env("ENV", "prod").lower()
        # Use DEBUG for dev/qa, INFO for prod
        log_level = logging.DEBUG if env in ("dev", "qa") else logging.INFO
        file_handler.setLevel(log_level)
        
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        cls._instance.addHandler(file_handler)
        
        cls._instance.info(f"Log file switched to: {log_file}")

    @classmethod
    def get_console(cls) -> Console:
        """Get the rich console instance for custom formatting."""
        if cls._console is None:
            cls._console = Console(
                theme=AUTOMATION_THEME,
                force_terminal=True,
                legacy_windows=_is_windows_limited_encoding(),
            )
        return cls._console

    @classmethod
    def _create_logger(cls, app_name: str, log_file: Optional[Path] = None) -> logging.Logger:
        """
        Create and configure logger with console and file handlers.

        Args:
            app_name: Application name for log organization
            log_file: Optional explicit log file path (from RunContext)

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger("automation")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        # Clear any existing handlers
        logger.handlers.clear()

        # Determine log level from environment
        env = get_env("ENV", "prod").lower()
        # Use DEBUG for dev/qa, INFO for prod
        log_level = logging.DEBUG if env in ("dev", "qa") else logging.INFO

        # Rich console handler for beautiful terminal output
        # Use force_terminal on Windows for better compatibility
        console = Console(
            theme=AUTOMATION_THEME,
            force_terminal=True,
            legacy_windows=_is_windows_limited_encoding(),  # ASCII fallback on old Windows consoles
        )
        console_handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_level=True,
            show_path=False,
            markup=True,
            log_time_format="[%Y-%m-%d %H:%M:%S]"
        )
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)

        # File handler with structured formatting and rotation
        # Use provided log_file or fall back to legacy path structure
        if log_file is not None:
            cls._log_file = log_file
            cls._log_dir = log_file.parent
        else:
            # Legacy fallback (will be overwritten when RunContext is initialized)
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%I_%M_%p")
            log_dir = Path.cwd() / "logs" / app_name / date_str
            ensure_dir(log_dir)
            cls._log_dir = log_dir
            cls._log_file = log_dir / f"{app_name}_{time_str}.log"

        ensure_dir(cls._log_dir)
        file_handler = RotatingFileHandler(
            cls._log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8',  # Ensure UTF-8 for cross-platform Unicode support
        )
        file_handler.setLevel(log_level)

        # Structured formatter for file (no colors, plain text)
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        logger.info(
            f"[bold cyan]Logger initialized[/] | App: [yellow]{app_name}[/] | "
            f"Level: [green]{logging.getLevelName(log_level)}[/] | "
            f"File: [blue]{cls._log_file}[/]",
            extra={"markup": True}
        )

        return logger

    @classmethod
    def get_log_dir(cls) -> Optional[Path]:
        """Get the current log directory path."""
        return cls._log_dir
    
    @classmethod
    def get_log_file(cls) -> Optional[Path]:
        """Get the current log file path."""
        return cls._log_file

    @classmethod
    def success(cls, message: str):
        """Log a success message with green styling."""
        console = cls.get_console()
        console.print(f"✓ {message}", style="success")

    @classmethod
    def step(cls, message: str):
        """Log a step message with magenta styling."""
        console = cls.get_console()
        console.print(f"➜ {message}", style="step")

    @classmethod
    def metric(cls, name: str, value: Any, unit: str = ""):
        """Log a metric with blue styling."""
        console = cls.get_console()
        console.print(f"📊 {name}: [bold]{value}[/] {unit}", style="metric")

    @classmethod
    def section(cls, title: str):
        """Print a section header with consistent styling."""
        console = cls.get_console()
        console.print(f"\n[bold cyan]{'='*80}[/]")
        console.print(f"[bold cyan]{title.upper()}[/]")
        console.print(f"[bold cyan]{'='*80}[/]\n")

    @classmethod
    def panel(cls, content: str, title: str = "", style: str = "cyan"):
        """Display content in a rich panel."""
        console = cls.get_console()
        console.print(Panel(content, title=title, style=style, border_style=style))

    @classmethod
    def table(cls, title: str, columns: List[str], rows: List[List[Any]]):
        """
        Display data in a formatted table.

        Args:
            title: Table title
            columns: List of column names
            rows: List of row data (each row is a list of values)
        """
        console = cls.get_console()
        table = Table(title=title, show_header=True, header_style="bold magenta")

        for col in columns:
            table.add_column(col)

        for row in rows:
            table.add_row(*[str(cell) for cell in row])

        console.print(table)

    @classmethod
    def progress_bar(cls, description: str = "Processing..."):
        """
        Create a progress bar context manager.

        Usage:
            with AutomationLogger.progress_bar("Loading...") as progress:
                task = progress.add_task("[cyan]Loading...", total=100)
                for i in range(100):
                    progress.update(task, advance=1)
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=cls.get_console()
        )


# Convenience functions for common logging patterns
def get_logger(app_name: str = "automation", log_file: Optional[Path] = None) -> logging.Logger:
    """
    Get the singleton automation logger.

    Args:
        app_name: Application name for log organization
        log_file: Optional explicit log file path (from RunContext)

    Returns:
        Configured logger instance
    """
    return AutomationLogger.get_logger(app_name, log_file)


def log_success(message: str):
    """Log a success message with green checkmark."""
    AutomationLogger.success(message)


def log_step(message: str):
    """Log a step message with arrow indicator."""
    AutomationLogger.step(message)


def log_metric(name: str, value: Any, unit: str = ""):
    """Log a metric with formatted output."""
    AutomationLogger.metric(name, value, unit)


def log_section(title: str):
    """Log a section header."""
    AutomationLogger.section(title)


def log_panel(content: str, title: str = "", style: str = "cyan"):
    """Log content in a panel."""
    AutomationLogger.panel(content, title, style)


def log_table(title: str, columns: List[str], rows: List[List[Any]]):
    """Log a formatted table."""
    AutomationLogger.table(title, columns, rows)


# Legacy compatibility - alias Logger class to AutomationLogger
Logger = AutomationLogger


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None, console_output: bool = True):
    """
    Backward compatibility function for setup_logging.

    Note: The new AutomationLogger auto-configures itself via get_logger().
    This function is provided for backward compatibility with legacy code.

    Args:
        level: Logging level (ignored - uses ENV variable)
        log_file: Log file path (ignored - auto-configured)
        console_output: Console output flag (ignored - always enabled)
    """
    # Auto-initialize logger if not already done
    # The logger is auto-configured via get_logger() so this is just a no-op
    # for backward compatibility
    pass
