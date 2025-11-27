"""Browser configuration loader.

Loads browser-related settings from config/browser.config.yaml
with environment variable override support.
"""

from pathlib import Path
from typing import Any, Dict, Optional
import os

import yaml


class BrowserConfig:
    """Browser configuration loaded from YAML with environment override support."""
    
    _instance: Optional['BrowserConfig'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        """Singleton pattern - only one config instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        config_path = Path(__file__).parent / "browser.config.yaml"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
        else:
            self._config = {}
    
    def _get_env_override(self, key: str, default: Any = None) -> Any:
        """Get environment variable override if exists."""
        env_key = key.upper().replace(".", "_")
        env_value = os.environ.get(env_key)
        
        if env_value is None:
            return default
        
        # Type conversion based on default value type
        if isinstance(default, bool):
            return env_value.lower() in ('true', '1', 'yes')
        elif isinstance(default, int):
            return int(env_value)
        elif isinstance(default, float):
            return float(env_value)
        return env_value
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get config value by dot-notation path with env override.
        
        Args:
            path: Dot-notation path like 'browser.headless' or 'screenshots.format'
            default: Default value if not found
            
        Returns:
            Config value or default
        """
        # Check environment override first
        env_value = self._get_env_override(path)
        if env_value is not None:
            return env_value
        
        # Navigate config dict
        keys = path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value if value is not None else default
    
    # Browser Settings
    @property
    def browser_type(self) -> str:
        return self.get('browser.type', 'chromium')
    
    @property
    def headless(self) -> bool:
        return self.get('browser.headless', False)
    
    @property
    def incognito(self) -> bool:
        return self.get('browser.incognito', True)
    
    @property
    def slow_mo_ms(self) -> int:
        return self.get('browser.slow_mo_ms', 0)
    
    @property
    def browser_args(self) -> list:
        return self.get('browser.args', ['--start-maximized'])
    
    # Window Settings
    @property
    def auto_fit_screen(self) -> bool:
        return self.get('window.auto_fit_screen', True)
    
    @property
    def position_top_left(self) -> bool:
        return self.get('window.position_top_left', True)
    
    @property
    def fallback_viewport(self) -> dict:
        return {
            'width': self.get('window.fallback_width', 1280),
            'height': self.get('window.fallback_height', 800)
        }
    
    @property
    def custom_viewport(self) -> dict:
        return {
            'width': self.get('window.custom_width', 1920),
            'height': self.get('window.custom_height', 1080)
        }
    
    # Timeout Settings
    @property
    def default_timeout(self) -> int:
        return self.get('timeouts.default', 30000)
    
    @property
    def navigation_timeout(self) -> int:
        return self.get('timeouts.navigation', 60000)
    
    @property
    def action_timeout(self) -> int:
        return self.get('timeouts.action', 10000)
    
    @property
    def popup_timeout(self) -> int:
        return self.get('timeouts.popup', 60000)
    
    # Screenshot Settings
    @property
    def screenshots_enabled(self) -> bool:
        return self.get('screenshots.enabled', True)
    
    @property
    def screenshot_format(self) -> str:
        return self.get('screenshots.format', 'png')
    
    @property
    def screenshot_quality(self) -> int:
        return self.get('screenshots.quality', 80)
    
    @property
    def screenshot_full_page(self) -> bool:
        return self.get('screenshots.full_page', False)
    
    @property
    def screenshot_disable_animations(self) -> bool:
        return self.get('screenshots.disable_animations', True)
    
    @property
    def screenshot_hide_caret(self) -> bool:
        return self.get('screenshots.hide_caret', True)
    
    @property
    def screenshot_timeout(self) -> int:
        return self.get('screenshots.timeout', 30000)
    
    # Video Settings
    @property
    def video_enabled(self) -> bool:
        return self.get('video.enabled', False)
    
    @property
    def video_format(self) -> str:
        return self.get('video.format', 'webm')
    
    @property
    def video_match_viewport(self) -> bool:
        return self.get('video.match_viewport', True)
    
    @property
    def video_size(self) -> dict:
        return {
            'width': self.get('video.width', 1280),
            'height': self.get('video.height', 720)
        }
    
    # Trace Settings
    @property
    def trace_enabled(self) -> bool:
        return self.get('trace.enabled', False)
    
    @property
    def trace_screenshots(self) -> bool:
        return self.get('trace.screenshots', True)
    
    @property
    def trace_snapshots(self) -> bool:
        return self.get('trace.snapshots', True)
    
    @property
    def trace_sources(self) -> bool:
        return self.get('trace.sources', True)
    
    # Retry Settings
    @property
    def max_retries(self) -> int:
        return self.get('retry.max_retries', 3)
    
    @property
    def retry_delay_ms(self) -> int:
        return self.get('retry.delay_ms', 1000)
    
    # Logging Settings
    @property
    def log_level(self) -> str:
        return self.get('logging.level', 'INFO')
    
    @property
    def colored_output(self) -> bool:
        return self.get('logging.colored_output', True)
    
    # Performance Settings
    @property
    def performance_tracking(self) -> bool:
        return self.get('performance.tracking_enabled', True)
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    def to_dict(self) -> Dict[str, Any]:
        """Return full config as dictionary."""
        return self._config.copy()


# Singleton instance
browser_config = BrowserConfig()
