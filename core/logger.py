"""Centralized logging configuration with console and file handlers."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.utils import ensure_dir, get_env


class Logger:
    """Singleton logger factory with structured formatting."""

    _instance: logging.Logger | None = None
    _log_dir: Path | None = None

    @classmethod
    def get(cls, app_name: str = "automation") -> logging.Logger:
        """Get or create singleton logger instance.

        Args:
            app_name: Name of the application for log file path (e.g., 'osc')

        Returns:
            Configured logging.Logger instance
        """
        if cls._instance is None:
            cls._instance = cls._create_logger(app_name)
        return cls._instance

    @classmethod
    def _create_logger(cls, app_name: str) -> logging.Logger:
        """Create and configure logger with console and file handlers.

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

        # Structured formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler under app's logs/ directory
        log_dir = Path.cwd() / "apps" / app_name / "logs"
        ensure_dir(log_dir)
        cls._log_dir = log_dir

        log_file = log_dir / "automation.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info(
            f"Logger initialized for app '{app_name}' | Log level: {logging.getLevelName(log_level)}"
        )

        return logger

    @classmethod
    def get_log_dir(cls) -> Path | None:
        """Get the current log directory.

        Returns:
            Path to log directory or None if logger not initialized
        """
        return cls._log_dir
