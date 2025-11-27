"""
Run Context - Unified output folder management for each automation run.

Provides a single source of truth for all output paths during a test run:
- Log files
- Screenshots  
- Traces
- Videos (for future)
- Any exported files

Folder Structure:
    artifacts/
    └── {app_name}/
        └── {YYYY-MM-DD}/
            └── {HH_MM_SS_AM_PM}/
                ├── run.log
                ├── run_info.json
                ├── screenshots/
                │   ├── 001_login.png
                │   └── 002_form.png
                ├── traces/
                ├── videos/
                └── exports/

Usage:
    # Automatically initialized by UIAutomationCore - no manual setup needed!
    
    with UIAutomationCore(app_name="osc", script_name="create_merchant") as core:
        core.take_screenshot("login")  # Auto-saved to artifacts folder
        
        # If you need custom export:
        path = core.run_context.get_export_path("data.csv")
"""

from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import threading
import json


class RunContext:
    """Singleton context manager for a single automation run.
    
    Manages all output paths and ensures everything for one run
    stays in a single folder. Automatically created by UIAutomationCore.
    """
    
    _instance: Optional['RunContext'] = None
    _lock = threading.Lock()
    
    def __init__(
        self,
        app_name: str,
        script_name: str,
        base_dir: Optional[Path] = None
    ):
        """Initialize run context (use RunContext.initialize() instead).
        
        Args:
            app_name: Application name (e.g., "osc")
            script_name: Script/workflow name for identification
            base_dir: Base directory for artifacts (default: cwd/artifacts)
        """
        self._app_name = app_name
        self._script_name = script_name
        self._start_time = datetime.now()
        
        # Build folder structure: artifacts/{app}/{date}/{time}/
        # Include seconds to avoid collisions: "11_56_30_AM"
        base = base_dir or (Path.cwd() / "artifacts")
        date_str = self._start_time.strftime("%Y-%m-%d")
        time_str = self._start_time.strftime("%I_%M_%S_%p")
        
        self._run_dir = base / app_name / date_str / time_str
        self._run_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self._screenshots_dir = self._run_dir / "screenshots"
        self._screenshots_dir.mkdir(exist_ok=True)
        
        self._traces_dir = self._run_dir / "traces"
        self._traces_dir.mkdir(exist_ok=True)
        
        self._videos_dir = self._run_dir / "videos"
        self._videos_dir.mkdir(exist_ok=True)
        
        self._exports_dir = self._run_dir / "exports"
        self._exports_dir.mkdir(exist_ok=True)
        
        # Log file path
        self._log_file = self._run_dir / "run.log"
        
        # Screenshot counter for sequential naming
        self._screenshot_counter = 0
        
        # Write run info metadata
        self._write_run_info()
    
    def _write_run_info(self):
        """Write metadata about this run to run_info.json"""
        import platform
        info = {
            "app_name": self._app_name,
            "script_name": self._script_name,
            "started_at": self._start_time.isoformat(),
            "run_dir": str(self._run_dir),
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "python_version": platform.python_version()
            },
            "status": "running"
        }
        info_file = self._run_dir / "run_info.json"
        with open(info_file, "w") as f:
            json.dump(info, f, indent=2)
    
    def update_status(self, status: str, error: Optional[str] = None):
        """Update the run status in run_info.json
        
        Args:
            status: New status (e.g., "completed", "failed")
            error: Optional error message if failed
        """
        info_file = self._run_dir / "run_info.json"
        if info_file.exists():
            with open(info_file, "r") as f:
                info = json.load(f)
            
            info["status"] = status
            info["ended_at"] = datetime.now().isoformat()
            if error:
                info["error"] = error
            
            with open(info_file, "w") as f:
                json.dump(info, f, indent=2)
    
    @classmethod
    def initialize(
        cls,
        app_name: str,
        script_name: str,
        base_dir: Optional[Path] = None
    ) -> 'RunContext':
        """Initialize the singleton run context.
        
        Called automatically by UIAutomationCore.
        
        Args:
            app_name: Application name (e.g., "osc")
            script_name: Script/workflow name
            base_dir: Optional custom base directory
            
        Returns:
            The initialized RunContext instance
        """
        with cls._lock:
            cls._instance = cls(app_name, script_name, base_dir)
            return cls._instance
    
    @classmethod
    def get_current(cls) -> Optional['RunContext']:
        """Get the current run context.
        
        Returns:
            Current RunContext or None if not initialized
        """
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the singleton (for testing or new runs)."""
        with cls._lock:
            cls._instance = None
    
    # ----- Properties for accessing paths -----
    
    @property
    def app_name(self) -> str:
        """Application name."""
        return self._app_name
    
    @property
    def script_name(self) -> str:
        """Script/workflow name."""
        return self._script_name
    
    @property
    def start_time(self) -> datetime:
        """Run start timestamp."""
        return self._start_time
    
    @property
    def run_dir(self) -> Path:
        """Root directory for this run's artifacts."""
        return self._run_dir
    
    @property
    def log_file(self) -> Path:
        """Path to the log file for this run."""
        return self._log_file
    
    @property
    def screenshots_dir(self) -> Path:
        """Directory for screenshots."""
        return self._screenshots_dir
    
    @property
    def traces_dir(self) -> Path:
        """Directory for Playwright traces."""
        return self._traces_dir
    
    @property
    def videos_dir(self) -> Path:
        """Directory for video recordings."""
        return self._videos_dir
    
    @property
    def exports_dir(self) -> Path:
        """Directory for exported files (CSVs, reports, etc.)."""
        return self._exports_dir
    
    # ----- Helper methods for generating paths -----
    
    def get_screenshot_path(self, name: str, auto_number: bool = True) -> Path:
        """Get path for a screenshot file.
        
        Args:
            name: Screenshot name (without extension)
            auto_number: If True, prefix with sequential number
            
        Returns:
            Full path to screenshot file
        """
        if auto_number:
            self._screenshot_counter += 1
            filename = f"{self._screenshot_counter:03d}_{name}.png"
        else:
            filename = f"{name}.png"
        return self._screenshots_dir / filename
    
    def get_export_path(self, filename: str) -> Path:
        """Get path for an export file.
        
        Args:
            filename: Name of the export file (with extension)
            
        Returns:
            Full path to export file
        """
        return self._exports_dir / filename
    
    def get_trace_path(self, name: str = "trace") -> Path:
        """Get path for a Playwright trace file.
        
        Args:
            name: Trace name (without extension)
            
        Returns:
            Full path to trace file
        """
        return self._traces_dir / f"{name}.zip"
    
    def get_video_path(self, name: str = "recording") -> Path:
        """Get path for a video recording file.
        
        Args:
            name: Video name (without extension)
            
        Returns:
            Full path to video file
        """
        return self._videos_dir / f"{name}.webm"
    
    def get_file_path(self, filename: str) -> Path:
        """Get path for any file in the run directory.
        
        Args:
            filename: Name of the file (with extension)
            
        Returns:
            Full path to file in run directory
        """
        return self._run_dir / filename
    
    def __repr__(self) -> str:
        return f"RunContext(app={self._app_name}, script={self._script_name}, dir={self._run_dir})"
