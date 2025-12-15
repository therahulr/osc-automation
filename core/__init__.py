"""Core automation utilities - app-agnostic, reusable components.

This module provides a comprehensive automation framework with:
- UIAutomationCore: Centralized automation management
- Browser management with automatic lifecycle
- Enhanced colored logging
- Performance tracking and reporting
- Reusable UI components
- Advanced configuration system

Quick Start:
    from core import UIAutomationCore

    with UIAutomationCore(app_name="my_app") as core:
        core.page.goto("https://example.com")
        core.logger.info("Page loaded!")
"""

# Core automation framework
from core.automation_core import UIAutomationCore, quick_automation

# Browser and UI
from core.browser import BrowserManager
from core.ui import Ui

# Logging
from core.logger import (
    AutomationLogger,
    get_logger,
    setup_logging,
    log_success,
    log_step,
    log_metric,
    log_section,
    log_panel,
    log_table,
)

# Configuration
from core.config import settings

# Performance tracking and reporting
from core.performance import performance_tracker, RunMetadata, StepMetrics
from core.performance_decorators import (
    PerformanceSession,
    StepContext,
    performance_step,
    track_playwright_actions,
)
from core.performance_reporter import PerformanceReporter

# Reusable components
from core.components import (
    BaseComponent,
    FormComponent,
    TableComponent,
    ModalComponent,
)

# AI and ML
from core.gemini_client import (
    GeminiClient,
    GeminiResponse,
    create_gemini_client,
)


__all__ = [
    # Core framework
    "UIAutomationCore",
    "quick_automation",
    # Browser and UI
    "BrowserManager",
    "Ui",
    # Logging
    "AutomationLogger",
    "get_logger",
    "setup_logging",
    "log_success",
    "log_step",
    "log_metric",
    "log_section",
    "log_panel",
    "log_table",
    # Configuration
    "settings",
    # Performance
    "performance_tracker",
    "RunMetadata",
    "StepMetrics",
    "PerformanceSession",
    "StepContext",
    "performance_step",
    "track_playwright_actions",
    "PerformanceReporter",
    # Components
    "BaseComponent",
    "FormComponent",
    "TableComponent",
    "ModalComponent",
    # AI and ML
    "GeminiClient",
    "GeminiResponse",
    "create_gemini_client",
]

