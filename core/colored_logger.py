"""Enhanced colored logger with rich terminal output.

Provides beautiful, colored logging with:
- Color-coded log levels
- Structured formatting
- Progress tracking
- Status indicators
- Rich text support
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

from core.utils import ensure_dir, get_env


# Custom theme for beautiful output
CUSTOM_THEME = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "critical": "bold white on red",
    "success": "bold green",
    "debug": "dim cyan",
    "step": "bold magenta",
    "metric": "bold blue",
})


class ColoredLogger:
    """Enhanced logger with rich colored terminal output."""

    _instance: Optional[logging.Logger] = None
    _console: Optional[Console] = None
    _log_dir: Optional[Path] = None

    @classmethod
    def get(cls, app_name: str = "automation") -> logging.Logger:
        """Get or create singleton colored logger instance.

        Args:
            app_name: Name of the application for log file path

        Returns:
            Configured logging.Logger instance with rich output
        """
        if cls._instance is None:
            cls._instance = cls._create_logger(app_name)
            cls._console = Console(theme=CUSTOM_THEME)
        return cls._instance

    @classmethod
    def get_console(cls) -> Console:
        """Get the rich console instance for advanced formatting."""
        if cls._console is None:
            cls._console = Console(theme=CUSTOM_THEME)
        return cls._console

    @classmethod
    def _create_logger(cls, app_name: str) -> logging.Logger:
        """Create and configure logger with rich console handler.

        Args:
            app_name: Application name for organizing log files

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger("automation")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        # Clear existing handlers
        logger.handlers.clear()

        # Determine log level from environment
        env = get_env("ENV", "prod").lower()
        log_level = logging.DEBUG if env == "dev" else logging.INFO

        # Rich console handler with beautiful formatting
        console_handler = RichHandler(
            console=Console(theme=CUSTOM_THEME),
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

        # File handler with structured formatting
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%I_%M_%p")

        log_dir = Path.cwd() / "logs" / app_name / date_str
        ensure_dir(log_dir)
        cls._log_dir = log_dir

        log_file = log_dir / f"{app_name}_{time_str}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(log_level)

        # Structured formatter for file (no colors)
        file_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        logger.info(
            f"[bold cyan]Colored Logger initialized[/] | App: [yellow]{app_name}[/] | "
            f"Level: [green]{logging.getLevelName(log_level)}[/] | "
            f"Log file: [blue]{log_file}[/]",
            extra={"markup": True}
        )

        return logger

    @classmethod
    def get_log_dir(cls) -> Optional[Path]:
        """Get the current log directory."""
        return cls._log_dir

    @classmethod
    def success(cls, message: str):
        """Log a success message with green color."""
        console = cls.get_console()
        console.print(f"✓ {message}", style="success")

    @classmethod
    def step(cls, message: str):
        """Log a step message with magenta color."""
        console = cls.get_console()
        console.print(f"➜ {message}", style="step")

    @classmethod
    def metric(cls, name: str, value: any, unit: str = ""):
        """Log a metric with blue color."""
        console = cls.get_console()
        console.print(f"📊 {name}: [bold]{value}[/] {unit}", style="metric")

    @classmethod
    def section(cls, title: str):
        """Print a section header."""
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
    def table(cls, title: str, columns: list, rows: list):
        """Display data in a rich table.

        Args:
            title: Table title
            columns: List of column names
            rows: List of row data (list of lists)
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
        """Create a progress bar context manager.

        Usage:
            with ColoredLogger.progress_bar("Loading...") as progress:
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


# Convenience functions
def log_success(message: str):
    """Log a success message."""
    ColoredLogger.success(message)


def log_step(message: str):
    """Log a step message."""
    ColoredLogger.step(message)


def log_metric(name: str, value: any, unit: str = ""):
    """Log a metric."""
    ColoredLogger.metric(name, value, unit)


def log_section(title: str):
    """Log a section header."""
    ColoredLogger.section(title)


def log_panel(content: str, title: str = "", style: str = "cyan"):
    """Log content in a panel."""
    ColoredLogger.panel(content, title, style)


def log_table(title: str, columns: list, rows: list):
    """Log a table."""
    ColoredLogger.table(title, columns, rows)
